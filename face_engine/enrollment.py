import cv2
import numpy as np
import pickle
from .utils import decode_base64_image

# Load ultra-fast standard Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def enroll_face(b64_images):
    """Processes 3 registration photos and creates a mathematical face embedding."""
    embeddings = []
    
    for b64 in b64_images:
        img = decode_base64_image(b64)
        if img is None: continue
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            # Standardize face size to 100x100 and flatten to 1D array
            face_resized = cv2.resize(face_roi, (100, 100))
            embeddings.append(face_resized.flatten())
            
    if not embeddings:
        return None, None
        
    # Average the 3 photos for higher accuracy
    avg_embedding = np.mean(embeddings, axis=0)
    emb_bytes = pickle.dumps(avg_embedding)
    
    return emb_bytes, None