import cv2
import numpy as np
import pickle
from .utils import decode_base64_image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def enroll_face(b64_images):
    """Processes registration photos, normalizes lighting, and creates face embedding."""
    embeddings = []
    
    for b64 in b64_images:
        img = decode_base64_image(b64)
        if img is None: continue
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Normalize lighting across the whole image
        gray = cv2.equalizeHist(gray)
        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 50))
        
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face_roi, (100, 100))
            
            # Normalize vector to range 0-1
            norm_face = face_resized.astype("float32") / 255.0
            embeddings.append(norm_face.flatten())
            
    if not embeddings:
        return None, None
        
    # Average the captured angles
    avg_embedding = np.mean(embeddings, axis=0)
    emb_bytes = pickle.dumps(avg_embedding)
    
    return emb_bytes, None