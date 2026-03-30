from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


_INITIAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activities before and after each test."""
    activities.clear()
    activities.update(deepcopy(_INITIAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(_INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
