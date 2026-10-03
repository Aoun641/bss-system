import cv2
import numpy as np

def check_liveness(img, face_box, strictness="Medium"):
    """
    Analyzes the face for spoofing attempts (mobile screens, printed photos).
    Returns dict with 'live' boolean and 'reasons' list.
    """
    if face_box is None:
        return {"live": False, "reasons": ["No face detected"]}
    
    x, y, w, h = face_box
    face_roi = img[y:y+h, x:x+w]
    
    if face_roi.size == 0:
        return {"live": False, "reasons": ["Invalid face frame"]}

    reasons = []
    
    # Convert to grayscale for analysis
    gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    
    # 1. Blur Detection (Catches printed paper photos)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    thresholds = {"Low": 30, "Medium": 50, "High": 80}
    thresh = thresholds.get(strictness, 50)
    
    if laplacian_var < thresh:
        reasons.append("Blurry image / Photo print detected")
        
    # 2. Moire Pattern / Screen Detection (Catches Mobile Phones)
    # Screens emit high-frequency grid patterns that cameras catch
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges) / (w * h)
    
    if edge_density > 0.35 and strictness in ["Medium", "High"]:
        reasons.append("Screen pixel grid / Moire pattern detected")

    if len(reasons) > 0:
        return {"live": False, "reasons": reasons}
    
    return {"live": True, "reasons": []}