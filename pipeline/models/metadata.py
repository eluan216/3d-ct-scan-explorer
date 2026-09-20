"""
Shared metadata models used across the pipeline.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json
from pathlib import Path


@dataclass
class VolumeMetadata:
    shape: List[int]
    spacing_mm: List[float]
    origin_mm: List[float]
    orientation: str
    intensity_range: List[float]
    dtype: str = "uint8"
    window_level: float = 50.0
    window_width: float = 400.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2))


@dataclass
class Manifest:
    pipeline_version: str
    subject_id: str
    volume: Dict[str, str]
    meshes: Dict[str, str] = field(default_factory=dict)
    slices: Dict[str, str] = field(default_factory=dict)
    labels: Dict[str, Any] = field(default_factory=dict)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2))
