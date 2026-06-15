import threading

_detector = None
_lock = threading.Lock()

def get_detector():
    global _detector
    if _detector is None:
        with _lock:
            if _detector is None:
                from insightface.app import FaceAnalysis
                detector = FaceAnalysis(providers=["CPUExecutionProvider"])
                detector.prepare(ctx_id=-1, det_size=(320, 320))
                _detector = detector
    return _detector

def detect_faces(image):
    return get_detector().get(image)

def unload_detector():
    """Optional: free memory after batch jobs finish."""
    global _detector
    with _lock:
        _detector = None