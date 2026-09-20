# Product Requirements Document (PRD)

**Project:** 3D CT Scan Explorer  
**Owner:** eluan216  
**Status:** In Development  
**Last Updated:** 2026-09-20

## 1. Overview
Build an interactive web-based 3D CT anatomy explorer that allows medical students and learners to visualize abdominal organs from real clinical CT scans. The application will provide synchronized axial, coronal, and sagittal views alongside a 3D mesh representation.

## 2. Goals
- Create a learning-focused tool (explicitly **not** a medical device).
- Demonstrate strong skills in medical imaging pipelines, 3D web visualization, and full-stack development.
- Produce a clean, well-documented portfolio piece with clear architecture and verification steps.

## 3. Key Features
- Interactive 3D organ meshes generated from segmentation masks.
- Synchronized multi-planar reformatted (MPR) views (axial / coronal / sagittal).
- Click-to-select organ functionality that updates crosshair position across all views.
- Organ visibility toggles and opacity controls.
- Responsive design (desktop + mobile).
- Dark radiology-inspired theme.

## 4. Non-Goals
- Clinical diagnosis or decision support.
- Real-time processing of new patient scans.
- Regulatory compliance (FDA, CE, etc.).

## 5. Technical Requirements
- **Backend / Pipeline:** Python (nibabel, scikit-image, trimesh) for mesh generation and asset preparation.
- **Frontend:** Next.js (App Router) + React Three Fiber + Zustand.
- **Data:** Publicly available TotalSegmentator CT subset (CC BY 4.0) with proper attribution.
- Assets must remain under reasonable size for web delivery (~20 MB target).

## 6. Success Metrics
- Correct anatomical orientation (liver on patient's right, etc.).
- All views stay perfectly synchronized.
- Clean build and deployable on Vercel or similar.
- Comprehensive README + architecture documentation.

## 7. Originality Note
This project is independently designed and implemented. Inspiration may come from publicly shared educational resources, but all architecture decisions, code structure, verification methods, and documentation are original work by the repository owner.

## 8. License & Attribution
- Code: MIT (or as specified)
- Data: TotalSegmentator dataset (Wasserthal et al.), University Hospital Basel, CC BY 4.0
