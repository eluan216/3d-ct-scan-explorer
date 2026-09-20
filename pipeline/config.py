"""
Pipeline configuration.

All processing parameters live here so runs are reproducible
and easy to adjust without touching core logic.
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any
import json


@dataclass
class WindowSettings:
    level: float = 50.0
    width: float = 400.0


@dataclass
class CropSettings:
    margin_mm: float = 20.0
    enabled: bool = True


@dataclass
class ResampleSettings:
    target_spacing_mm: Optional[tuple] = None  # e.g. (1.0, 1.0, 1.5)
    enabled: bool = False


@dataclass
class MeshSettings:
    max_faces: int = 40000
    smooth_iterations: int = 5
    min_component_voxels: int = 100


@dataclass
class PipelineConfig:
    # Input
    input_path: Path = Path("data/raw")
    output_path: Path = Path("assets")

    # Which structures to keep
    target_labels: List[str] = field(default_factory=lambda: [
        "liver", "spleen", "stomach",
        "kidney_left", "kidney_right",
        "aorta", "inferior_vena_cava", "spine"
    ])

    # Processing stages
    window: WindowSettings = field(default_factory=WindowSettings)
    crop: CropSettings = field(default_factory=CropSettings)
    resample: ResampleSettings = field(default_factory=ResampleSettings)
    mesh: MeshSettings = field(default_factory=MeshSettings)

    # Quality gates
    require_orientation_check: bool = True
    fail_on_empty_label: bool = True
    max_nan_fraction: float = 0.0

    # Versioning
    pipeline_version: str = "0.1.0"

    def to_dict(self) -> Dict[str, Any]:
        def _convert(obj):
            if isinstance(obj, Path):
                return str(obj)
            if isinstance(obj, tuple):
                return list(obj)
            return obj

        return json.loads(json.dumps(asdict(self), default=_convert))

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path: Path) -> "PipelineConfig":
        data = json.loads(path.read_text())
        # Simple reconstruction — expand as needed
        cfg = cls()
        cfg.input_path = Path(data.get("input_path", cfg.input_path))
        cfg.output_path = Path(data.get("output_path", cfg.output_path))
        cfg.target_labels = data.get("target_labels", cfg.target_labels)
        cfg.pipeline_version = data.get("pipeline_version", cfg.pipeline_version)
        return cfg
