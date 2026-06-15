# Face Clustering Engine V0.8⚡

A high-performance, local AI tool designed to organize unstructured photo libraries using advanced vector search and facial recognition.

> **Status: Work in Progress (WIP)**. The core engine and dashboard UI are currently under active development.

## 🚀 Features
- **Local AI Processing**: Privacy-focused analysis that never leaves your machine.
- **Vector Indexing**: Fast similarity search for large image datasets.
- **Face Detection**: Automated clustering of individuals across thousands of photos.
- **Real-time Dashboard**: Live status of processed images and detected clusters.

## 🛠️ Tech Stack
- **Frontend**: React 19, Vite, Tailwind CSS v4, Lucide Icons.
- **Backend**: Python (FastAPI/Flask) or Node.js.
- **AI Models**: Local vector embeddings and face detection.

## 📁 Project Structure
```text
├── frontend/    # React Dashboard (Vite)
└── backend/     # AI Processing Engine & API
```

## ⚙️ Setup Instructions

### Prerequisites
- Node.js (v20+)
- Python 3.10+ (for Backend)

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file and set your backend URL:
   ```text
   VITE_BACKEND_URL=http://localhost:8000
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```

## 📝 Roadmap
- [ ] Complete Status Card integration with live API.
- [ ] Implement image upload and batch processing.
- [ ] Add Cluster Visualization view.
- [ ] Support for exported JSON metadata.