import cv2
import numpy as np
import pickle
from .utils import decode_base64_image

# Load frontal and profile face cascades for fast multi-angle recognition
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

def recognize_face(frame_b64, known_list):
    """Ultra-fast, multi-angle face recognition engine."""
    img = decode_base64_image(frame_b64)
    if img is None:
        return None, None, None

    # Downscale image to 320px for 10x faster processing speed
    h_orig, w_orig = img.shape[:2]
    target_w = 320
    scale_ratio = target_w / float(w_orig) if w_orig > target_w else 1.0
    
    if scale_ratio < 1.0:
        small_img = cv2.resize(img, (target_w, int(h_orig * scale_ratio)))
    else:
        small_img = img

    gray = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray) # Fixes dark/bright room lighting

    # Fast multi-angle detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=3, minSize=(30, 30))
    
    # If straight face not found, check angled/profile face
    if len(faces) == 0 and profile_cascade is not None:
        faces = profile_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=3, minSize=(30, 30))

    if len(faces) == 0:
        return None, None, None

    fx, fy, fw, fh = faces[0]
    
    # Scale box back to original coordinates
    x, y, w, h = int(fx / scale_ratio), int(fy / scale_ratio), int(fw / scale_ratio), int(fh / scale_ratio)

    face_roi = gray[fy:fy+fh, fx:fx+fw]
    face_resized = cv2.resize(face_roi, (100, 100)).astype("float32") / 255.0
    live_vector = face_resized.flatten()

    best_match_id = None
    best_match_type = None
    min_dist = float('inf')

    # Fast Vector Comparison Loop
    for record_id, record_type, emb_bytes in known_list:
        try:
            known_emb = pickle.loads(emb_bytes)
            dist = np.linalg.norm(live_vector - known_emb)
            if dist < min_dist:
                min_dist = dist
                best_match_id = record_id
                best_match_type = record_type
        except Exception:
            continue

    # Optimized matching distance threshold
    if min_dist < 23.5:
        return best_match_id, best_match_type, (x, y, w, h)

    # Face detected in camera, but not registered in database
    return None, None, (x, y, w, h)