"""Asynchronous display command orchestration.

The service keeps slow hardware I/O off the Qt UI thread and coalesces rapid
brightness updates so slider movement does not flood DDC/CI transports.
"""

from __future__ import annotations

import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from core.display_backend import DisplayBackend

logger = logging.getLogger(__name__)


class DisplayCommandService:
    """Serialize and coalesce display writes on a background worker."""

    def __init__(self, backend: DisplayBackend, debounce_seconds: float = 0.08):
        self.backend = backend
        self.debounce_seconds = max(0.0, debounce_seconds)
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="monitorglow-display")
        self._lock = threading.Lock()
        self._pending: dict[str, int] = {}
        self._timers: dict[str, threading.Timer] = {}
        self._closed = False

    def set_brightness(
        self,
        display_id: str,
        value: int,
        on_success: Callable[[int], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> None:
        value = max(0, min(100, int(value)))
        with self._lock:
            if self._closed:
                return
            self._pending[display_id] = value
            previous = self._timers.pop(display_id, None)
            if previous is not None:
                previous.cancel()
            timer = threading.Timer(
                self.debounce_seconds,
                self._submit_latest,
                args=(display_id, on_success, on_error),
            )
            timer.daemon = True
            self._timers[display_id] = timer
            timer.start()

    def _submit_latest(self, display_id, on_success, on_error):
        with self._lock:
            if self._closed:
                return
            value = self._pending.pop(display_id, None)
            self._timers.pop(display_id, None)
        if value is None:
            return
        self._executor.submit(self._write, display_id, value, on_success, on_error)

    def _write(self, display_id, value, on_success, on_error):
        try:
            self.backend.set_brightness(display_id, value)
        except Exception as exc:
            logger.warning("Asynchronous brightness write failed for %s: %s", display_id, exc)
            if on_error is not None:
                on_error(exc)
        else:
            if on_success is not None:
                on_success(value)

    def close(self) -> None:
        with self._lock:
            self._closed = True
            timers = list(self._timers.values())
            self._timers.clear()
            self._pending.clear()
        for timer in timers:
            timer.cancel()
        self._executor.shutdown(wait=False, cancel_futures=True)
