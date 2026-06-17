# Face Clustering Engine V0.11 ⚡

A high-performance, local AI tool designed to organize unstructured photo libraries using advanced vector search and facial recognition.

**Status: Work in Progress (WIP)**. Core engine and dashboard are actively under development. A hosted preview is now available.

## 🌐 Live Deployment
**Frontend (Dashboard):** [Vercel Preview](https://offline-image-search-and-smart-clus-puce.vercel.app/)  
**Backend API:** [Render API](https://offline-face-cluster-backend.onrender.com)

## 🚀 Features
- **Local AI Processing**: Privacy-focused analysis that never leaves your machine.
- **Vector Indexing**: Fast similarity search for large image datasets.
- **Face Detection**: Automated clustering of individuals across thousands of photos.
- **Real-time Dashboard**: Live status of processed images and detected clusters.
- **Face Renaming**: Label and rename detected face clusters for better organization.

## ✨ V0.11 Updates
- **Cloud Hosted Preview**: Deployment of the system to Vercel and Render for evaluation.
- **Architecture Decoupling**: Separation of the frontend dashboard and backend AI engine into independent services.
- **UI Polishing**: Enhanced Hero section and pipeline status monitoring.
- **Face Renaming**: Users can now assign custom names to identified clusters, persisting metadata to the SQLite layer.

## 🛠️ Tech Stack
- **Frontend**: React 19, Vite, Tailwind CSS v4, Lucide Icons.
- **Backend**: Python (FastAPI), SQLite, FAISS.
- **AI Models**: Local vector embeddings (ResNet), Face detection (InsightFace).

## 📁 Project Structure
```
frontend/    # React Dashboard (Vite)
├── src
│   ├── components
│   ├── App.jsx
output/      # Generated cluster metadata
photos/      # Uploaded image library
src/         # Core AI Pipeline
├── api/
│   └── main.py
├── backend/
│   ├── database.py
│   └── database.db
├── detector/
│   └── detector.py
├── embeddings/
├── utils/
│   ├── path_utils.py
│   └── image_utils.py
├── faces.index
```

## ⚙️ Setup Instructions

### 📋 Prerequisites
- Node.js (v20+)
- Python 3.10+

### 💻 Frontend Setup
1. `cd frontend`
2. `npm install`
3. Create `.env`:
   ```env
   VITE_BACKEND_URL=http://localhost:8000
   ```
4. `npm run dev`

### ⚙️ Backend Setup
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. `pip install -r requirements.txt`
5. `uvicorn main:app --reload`

## 🧠 Deployment Notes
The system is now split into two deployed services:
- **Frontend** is hosted on Vercel for fast static delivery of the React 19 dashboard.
- **Backend** is deployed on Render, exposing FastAPI endpoints for image indexing, embedding generation, and the clustering pipeline.

This separation allows independent scaling of UI and AI compute workloads.

## 📝 Project Notes (v0.11)
### What this project is
A full-stack local AI photo organization system that bridges a Python computer vision pipeline with a React 19 dashboard, enabling real-time monitoring and control of face detection, vector indexing, and clustering.

### Architecture Overview
- **Frontend (React 19 + Vite)**: Handles dashboard rendering, polling, and pipeline control UI.
- **Backend (FastAPI + SQLite + FAISS)**: Runs face detection (InsightFace), embedding generation (512-d vectors), similarity search (FAISS index), and clustering (DBSCAN).

### Data Flow
1. Images uploaded → backend storage.
2. Embeddings generated → stored in `.npy` + SQLite.
3. FAISS index built for similarity search.
4. DBSCAN clusters identities.
5. Frontend polls backend for live status updates.

### Current State (v0.11)
**Working:**
- Full-stack integration (frontend ↔ backend deployed)
- Live dashboard metrics
- Pipeline control UI (upload, index, embed, cluster)
- SQLite-backed persistence
- FAISS vector indexing
- Real-time polling system

**Known gaps:**
- Gallery view for clustered faces (In Progress)
- WebSocket migration (replace polling)
- Better deduplication handling
- Cluster visualization layer
- JSON export pipeline

## 📌 Resume Summary
- Built a deployed full-stack AI face clustering system using React 19, FastAPI, and FAISS, with live dashboard monitoring and cloud-hosted backend services.
- Deployed frontend on Vercel and backend on Render, enabling public access to a local-style computer vision pipeline.
- Designed a real-time AI control dashboard with pipeline orchestration (embedding, indexing, DBSCAN clustering).
- Integrated vector search + relational database synchronization for scalable face recognition across large image datasets.

## 📝 Roadmap
- [ ] Complete Status Card integration with live API.
- [ ] Implement image upload and batch processing.
- [ ] Add Cluster Visualization view.
- [ ] Support for exported JSON metadata.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.