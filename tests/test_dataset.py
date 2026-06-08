from audit_tool.core.dataset import load_controls


def test_control_count():
    controls = load_controls()
    assert len(controls) == 18
    assert sum(len(c['safeguards']) for c in controls) == 153
