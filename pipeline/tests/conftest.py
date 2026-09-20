"""Shared fixtures for the test suite."""

import numpy as np
import pytest
from models.volume import CanonicalVolume


@pytest.fixture
def simple_volume():
    data = np.random.randn(32, 32, 16).astype(np.float32)
    return CanonicalVolume(
        data=data,
        spacing_mm=(1.0, 1.0, 1.5),
        origin_mm=(0.0, 0.0, 0.0),
        orientation="RAS",
        source="test",
    )
