import cv2
import webbrowser
import os
from datetime import datetime

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# QR code detector
detector = cv2.QRCodeDetector()

while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # QR code detection using OpenCV
    data, bbox, _ = detector.detectAndDecode(img)

    if data:
        # Draw bounding box around the QR code
        if bbox is not None:
            for i in range(len(bbox[0])):
                cv2.line(img, tuple(map(int, bbox[0][i])), tuple(map(int, bbox[0][(i + 1) % 4])), (0, 255, 0), 2)

        # Display QR code data on the video feed
        cv2.putText(img, f"QR Code: {data}", (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Print QR code data and open URL
        print(f"QR Code detected: {data}")
        webbrowser.open(str(data))

        # Save the image with QR code
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"QRCode_{timestamp}.png"
        cv2.imwrite(filename, img)
        print(f"Saved detected QR code image as {filename}")

        break

    # Display the image
    cv2.imshow("QR Code Scanner", img)

    # Break loop on 'q' key press
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
