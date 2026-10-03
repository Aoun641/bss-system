import cv2
import numpy as np
import pickle
from .utils import decode_base64_image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def recognize_face(frame_b64, known_list):
    """Real-time AI face matching with lighting equalization and tuned distance threshold."""
    img = decode_base64_image(frame_b64)
    if img is None:
        return None, None, None
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Normalize lighting so room shadows don't break scanning
    gray = cv2.equalizeHist(gray)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 50))
    
    if len(faces) == 0:
        return None, None, None
        
    x, y, w, h = faces[0]
    face_roi = gray[y:y+h, x:x+w]
    
    # Normalize live face ROI to match enrolled format
    face_resized = cv2.resize(face_roi, (100, 100)).astype("float32") / 255.0
    live_vector = face_resized.flatten()
    
    best_match_id = None
    best_match_type = None
    min_dist = float('inf')
    
    # AI Comparison Loop
    for record_id, record_type, emb_bytes in known_list:
        try:
            known_emb = pickle.loads(emb_bytes)
            # Calculate Euclidean distance
            dist = np.linalg.norm(live_vector - known_emb)
            
            if dist < min_dist:
                min_dist = dist
                best_match_id = record_id
                best_match_type = record_type
        except Exception:
            continue
            
    # Tuned optimal threshold (lenient enough for lighting changes, strict enough for security)
    if min_dist < 22.0:
        return best_match_id, best_match_type, (x, y, w, h)
        
    # Face is in camera, but score did not match any registered user
    return None, None, (x, y, w, h)