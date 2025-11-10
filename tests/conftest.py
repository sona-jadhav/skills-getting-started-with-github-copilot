import copy
import pytest
from fastapi.testclient import TestClient

from src import app as app_module

@pytest.fixture
def client():
    return TestClient(app_module.app)

@pytest.fixture(autouse=True)
def isolation():
    """Backup and restore the in-memory activities dict around each test."""
    if hasattr(app_module, "activities"):
        orig = copy.deepcopy(app_module.activities)
    else:
        orig = {}
    try:
        yield
    finally:
        # restore
        if hasattr(app_module, "activities"):
            app_module.activities.clear()
            app_module.activities.update(orig)
