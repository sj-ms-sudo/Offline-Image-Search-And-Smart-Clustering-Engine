from insightface.app import FaceAnalysis

def create_detector():
    detector = FaceAnalysis()
    detector.prepare(ctx_id = 0)
    return detector

def detect_faces(image,detector):
    return detector.get(image)