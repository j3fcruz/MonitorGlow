"""Asynchronous, coalescing display command service."""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Lock, Timer

from core.display_backend import DisplayBackend, DisplayInfo


class DisplayCommandService:
    """Keep blocking monitor I/O away from the GUI thread.

    Brightness writes are debounced per display. Repeated slider events replace
    the pending value, so hardware receives the newest value instead of every
    intermediate UI event.
    """

    def __init__(
        self,
        backend: DisplayBackend,
        debounce_seconds: float = 0.1,
        max_workers: int = 2,
    ) -> None:
        self.backend = backend
        self.debounce_seconds = max(0.0, float(debounce_seconds))
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="monitorglow-display",
        )
        self._lock = Lock()
        self._timers: dict[str, Timer] = {}
        self._closed = False

    def list_displays(self) -> Future[list[DisplayInfo]]:
        return self._submit(self.backend.list_displays)

    def get_brightness(self, display_id: str) -> Future[int]:
        return self._submit(self.backend.get_brightness, display_id)

    def set_brightness(
        self,
        display_id: str,
        value: int,
        callback: Callable[[Future[None]], None] | None = None,
    ) -> None:
        value = max(0, min(100, int(value)))
        with self._lock:
            self._ensure_open()
            previous = self._timers.pop(display_id, None)
            if previous is not None:
                previous.cancel()
            timer = Timer(
                self.debounce_seconds,
                self._dispatch_brightness,
                args=(display_id, value, callback),
            )
            timer.daemon = True
            self._timers[display_id] = timer
            timer.start()

    def shutdown(self, wait: bool = True) -> None:
        with self._lock:
            if self._closed:
                return
            self._closed = True
            timers = list(self._timers.values())
            self._timers.clear()
        for timer in timers:
            timer.cancel()
        self._executor.shutdown(wait=wait, cancel_futures=True)

    def _dispatch_brightness(
        self,
        display_id: str,
        value: int,
        callback: Callable[[Future[None]], None] | None,
    ) -> None:
        with self._lock:
            self._timers.pop(display_id, None)
            if self._closed:
                return
        future = self._executor.submit(
            self.backend.set_brightness,
            display_id,
            value,
        )
        if callback is not None:
            future.add_done_callback(callback)

    def _submit(self, function, *args):
        with self._lock:
            self._ensure_open()
            return self._executor.submit(function, *args)

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("DisplayCommandService is shut down")

    def __enter__(self) -> DisplayCommandService:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.shutdown()
