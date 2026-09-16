"""Application-layer controller for workspace display profiles."""

from __future__ import annotations

from core.display_profiles import DisplayProfile, DisplayProfileStore
from core.profile_automation import DisplayProfileRestorer
from core.profile_service import DisplayProfileService, ProfileApplyResult


class DisplayProfileController:
    """Coordinate profile persistence, application, and active restoration."""

    def __init__(
        self,
        store: DisplayProfileStore,
        service: DisplayProfileService,
        restorer: DisplayProfileRestorer,
    ) -> None:
        self.store = store
        self.service = service
        self.restorer = restorer
        self._profiles = self.store.load()
        self._active_name: str | None = None

    @property
    def active_name(self) -> str | None:
        return self._active_name

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._profiles))

    def get(self, name: str) -> DisplayProfile:
        try:
            return self._profiles[name]
        except KeyError as exc:
            raise KeyError(f"unknown display profile: {name}") from exc

    def capture_and_save(self, name: str) -> DisplayProfile:
        profile = self.service.capture(name.strip())
        self._profiles[profile.name] = profile
        self.store.save(self._profiles)
        return profile

    def apply(self, name: str, *, activate: bool = True) -> ProfileApplyResult:
        profile = self.get(name)
        result = self.service.apply(profile)
        if activate:
            self._active_name = profile.name
            self.restorer.set_active_profile(profile)
            self.restorer.mark_current_topology()
        return result

    def delete(self, name: str) -> None:
        if name not in self._profiles:
            raise KeyError(f"unknown display profile: {name}")
        del self._profiles[name]
        self.store.save(self._profiles)
        if self._active_name == name:
            self._active_name = None
            self.restorer.set_active_profile(None)
