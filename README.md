"# image-cluster-intelligence-engine" 
Offline photo analysis and indexing system.

Current Features (v0.7)
- **Face Detection & Analysis**: High-accuracy face detection using InsightFace.
- **Vector Search**: Blazing fast similarity search powered by Faiss (FlatL2).
- **Clustering**: Automatic person grouping using DBSCAN with cosine metrics.
- **Persistent Storage**: Full SQLite backend for images, faces, embeddings, and clusters.
- **Path Intelligence**: Automated absolute path resolution and numerical embedding synchronization.
- **Visualization**: Integrated OpenCV display showing cluster results with localized bounding boxes.
- **Offline First**: Entirely local processing with no external API calls.


Tech Stack
- **Language**: Python 3.x
- **Vision**: InsightFace, OpenCV
- **Database**: SQLite3
- **Vector Search**: Faiss
- **Machine Learning**: Scikit-learn (DBSCAN), NumPy


Project Goal

- Folder scanning
- Face embeddings
- Similarity search
- Clustering
- Semantic search


Installation
pip install -r requirements.txt
Usage
python src/main.py
Roadmap
v0.1
Face detection
v0.2
Folder scanning
Metadata storage
v0.3
Face embeddings
v0.4
Similarity search
v0.5
Clustering