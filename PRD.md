# Product Requirements Document

**Project:** 3D CT Scan Explorer  
**Owner:** eluan216  
**Updated:** 2026-09-20

## Purpose
Build a web tool that turns a real clinical CT scan into interactive 3D organ models with synchronized axial, coronal, and sagittal views. The goal is a solid learning and portfolio piece for medical imaging and 3D visualization work.

## Core Requirements
- Generate 3D meshes from segmentation masks
- Keep axial, coronal, and sagittal views locked to the same crosshair
- Click an organ in 3D or in the list and jump every view to that location
- Support organ visibility toggles
- Work on both desktop and mobile
- Use a dark theme suitable for radiology review

## Out of Scope
- Any clinical decision support or diagnosis use
- Processing brand-new patient scans in real time
- Regulatory clearance

## Technical Choices
- Python pipeline for mesh creation (nibabel, scikit-image, trimesh)
- Next.js + React Three Fiber + Zustand for the frontend
- Public TotalSegmentator CT data with full attribution
- Keep final web assets under ~20 MB

## Acceptance Criteria
- Anatomical orientation is correct (liver on patient right, etc.)
- All views stay perfectly synchronized
- Clean build that can be deployed
- Clear README explaining architecture and verification steps

## Notes on Ownership
This repository and all design decisions, code structure, verification methods, and documentation are original work by the owner. Public educational resources may have provided high-level inspiration, but the implementation is independent.
