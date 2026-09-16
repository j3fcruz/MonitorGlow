from core.display_backend import DisplayInfo
from core.display_reconciler import DisplayReconciler
from core.fake_display_backend import FakeDisplayBackend


def test_reconcile_reports_initial_displays_as_added():
    backend = FakeDisplayBackend([DisplayInfo(id="a", name="A")])
    change = DisplayReconciler(backend).reconcile()
    assert [display.id for display in change.added] == ["a"]
    assert change.removed == ()


def test_reconcile_reports_added_and_removed_displays():
    backend = FakeDisplayBackend([DisplayInfo(id="a", name="A")])
    reconciler = DisplayReconciler(backend)
    reconciler.reconcile()

    backend._displays = [DisplayInfo(id="b", name="B")]
    backend._brightness = {"b": 50}
    change = reconciler.reconcile()

    assert [display.id for display in change.added] == ["b"]
    assert [display.id for display in change.removed] == ["a"]
    assert [display.id for display in change.current] == ["b"]
