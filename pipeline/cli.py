"""
Command-line entry point for the CT processing pipeline.

Explicit stages are exposed so each step can be run and inspected independently.
"""

import argparse
from pathlib import Path
import sys

from config import PipelineConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="3D CT Scan Explorer – processing pipeline"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # discovery / validation
    p = sub.add_parser("discover", help="Discover subjects under a root directory")
    p.add_argument("input", type=Path)

    p = sub.add_parser("validate", help="Validate a single subject")
    p.add_argument("path", type=Path)

    # processing stages
    p = sub.add_parser("preprocess", help="Run orientation + window + optional crop/resample")
    p.add_argument("subject", type=Path)
    p.add_argument("--config", type=Path, default=None)
    p.add_argument("--output", type=Path, default=None)

    p = sub.add_parser("segment", help="Run segmentation stage")
    p.add_argument("subject", type=Path)
    p.add_argument("--config", type=Path, default=None)

    p = sub.add_parser("mesh", help="Generate meshes from label map")
    p.add_argument("labels", type=Path)
    p.add_argument("--config", type=Path, default=None)
    p.add_argument("--output", type=Path, default=None)

    p = sub.add_parser("slices", help="Generate axial/coronal/sagittal slice sets")
    p.add_argument("volume", type=Path)
    p.add_argument("--config", type=Path, default=None)
    p.add_argument("--output", type=Path, default=None)

    # full build + verify
    p = sub.add_parser("build", help="Run complete pipeline and write assets/")
    p.add_argument("subject", type=Path)
    p.add_argument("--config", type=Path, default=None)
    p.add_argument("--output", type=Path, default=None)

    p = sub.add_parser("verify", help="Verify a generated assets directory")
    p.add_argument("assets", type=Path)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "discover":
        from dicom.discover import discover
        for r in discover(args.input):
            print(r)
        return 0

    if args.command == "validate":
        from dicom.validate import validate_study
        ok, messages = validate_study(args.path)
        for m in messages:
            print(m)
        return 0 if ok else 1

    if args.command == "preprocess":
        print("preprocess stage – implementation in progress")
        return 0

    if args.command == "segment":
        print("segment stage – implementation in progress")
        return 0

    if args.command == "mesh":
        print("mesh stage – implementation in progress")
        return 0

    if args.command == "slices":
        print("slices stage – implementation in progress")
        return 0

    if args.command == "build":
        cfg = PipelineConfig()
        if args.config:
            cfg = PipelineConfig.load(args.config)
        if args.output:
            cfg.output_path = args.output
        print(f"build stage – pipeline version {cfg.pipeline_version}")
        print(f"subject : {args.subject}")
        print(f"output  : {cfg.output_path}")
        print("full end-to-end wiring still under construction")
        return 0

    if args.command == "verify":
        from validation.assets import verify_assets
        ok, report = verify_assets(args.assets)
        print(report)
        return 0 if ok else 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
