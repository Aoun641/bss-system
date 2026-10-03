import cv2
import numpy as np
import pickle
from .utils import decode_base64_image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def recognize_face(frame_b64, known_list):
    """Compares the live camera frame against all saved database faces."""
    img = decode_base64_image(frame_b64)
    if img is None:
        return None, None, None
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))
    
    if len(faces) == 0:
        return None, None, None
        
    x, y, w, h = faces[0]
    face_roi = gray[y:y+h, x:x+w]
    face_resized = cv2.resize(face_roi, (100, 100)).flatten()
    
    best_match_id = None
    best_match_type = None
    min_dist = float('inf')
    
    # Compare live face to database
    for record_id, record_type, emb_bytes in known_list:
        try:
            known_emb = pickle.loads(emb_bytes)
            # Calculate Euclidean distance between face matrices
            dist = np.linalg.norm(face_resized - known_emb)
            
            if dist < min_dist:
                min_dist = dist
                best_match_id = record_id
                best_match_type = record_type
        except Exception:
            continue
            
    # Threshold for match (lower is stricter)
    if min_dist < 2900:
        return best_match_id, best_match_type, (x, y, w, h)
        
    # Face found but not recognized
    return None, None, (x, y, w, h)