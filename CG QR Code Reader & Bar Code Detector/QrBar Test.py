import cv2
import webbrowser
from pyzbar import pyzbar

# Initialize the webcam
cap = cv2.VideoCapture(0)

def decode_barcode(image):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        x, y, w, h = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f"{barcode_type}: {barcode_data}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return barcode_data, barcode_type
    return None, None

while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # QR code detection using OpenCV
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if bbox is not None:
        # Draw bounding box around the QR code
        for i in range(len(bbox[0])):
            point1 = tuple(map(int, bbox[0][i]))
            point2 = tuple(map(int, bbox[0][(i+1) % len(bbox[0])]))
            cv2.line(img, point1, point2, (255, 0, 0), 2)

    if data:
        print(f"QR Code detected: {data}")
        webbrowser.open(str(data))
        break

    # Barcode detection using pyzbar
    barcode_data, barcode_type = decode_barcode(img)
    if barcode_data:
        print(f"Barcode detected: {barcode_data} (Type: {barcode_type})")

    # Display the image with detected QR code or barcode
    cv2.imshow("QR and Barcode Scanner", img)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
