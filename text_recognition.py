import cv2
import pytesseract

def recognize_text(frame, center_only=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if center_only:
        h, w = gray.shape
        w6, h6 = w // 6, h // 6
        x1, y1 = w // 2 - w6, h // 2 - h6
        x2, y2 = w // 2 + w6, h // 2 + h6
        roi = gray[max(0, y1):min(h, y2), max(0, x1):min(w, x2)]
    else:
        roi = gray

    roi = cv2.GaussianBlur(roi, (3, 3), 0)
    roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    text = pytesseract.image_to_string(roi, lang="eng")
    return text.strip()
