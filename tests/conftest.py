import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as initial_activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Arrange: reset in-memory activities state before each test."""
    from src import app as app_module

    app_module.activities = copy.deepcopy(initial_activities)
    yield


@pytest.fixture
def client():
    """Provides a TestClient for endpoint interaction (Act)."""
    return TestClient(app)
