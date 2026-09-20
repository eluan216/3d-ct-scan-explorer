"""
Command-line entry point for the CT processing pipeline.
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

    # discover
    p_disc = sub.add_parser("discover", help="Discover DICOM series or NIfTI subjects")
    p_disc.add_argument("input", type=Path, help="Root directory to scan")

    # validate
    p_val = sub.add_parser("validate", help="Validate a single study or subject")
    p_val.add_argument("path", type=Path)

    # run
    p_run = sub.add_parser("run", help="Run full pipeline on a subject")
    p_run.add_argument("subject", type=Path, help="Subject directory")
    p_run.add_argument("--config", type=Path, default=None)
    p_run.add_argument("--output", type=Path, default=None)

    # verify
    p_ver = sub.add_parser("verify", help="Run quality checks on generated assets")
    p_ver.add_argument("assets", type=Path, help="Path to assets directory")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "discover":
        from dicom.discover import discover
        results = discover(args.input)
        for r in results:
            print(r)
        return 0

    if args.command == "validate":
        from dicom.validate import validate_study
        ok, messages = validate_study(args.path)
        for m in messages:
            print(m)
        return 0 if ok else 1

    if args.command == "run":
        cfg = PipelineConfig()
        if args.config:
            cfg = PipelineConfig.load(args.config)
        if args.output:
            cfg.output_path = args.output

        # Full run will be wired once modules are complete
        print(f"Pipeline version {cfg.pipeline_version}")
        print(f"Subject: {args.subject}")
        print(f"Output:  {cfg.output_path}")
        print("Full run not yet fully wired — modules under construction.")
        return 0

    if args.command == "verify":
        from validation.assets import verify_assets
        ok, report = verify_assets(args.assets)
        print(report)
        return 0 if ok else 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
