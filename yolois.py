from ultralytics import YOLO
import cv2
import time

def eyes():
    
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    time.sleep(1)

    ret, frame = cap.read()

    if not ret:
        print("Error: Could not capture frame.")
        cap.release() 
        exit()

    image_filename = "captured_image.jpg"
    cv2.imwrite(image_filename, frame)

    print(f"Image saved as {image_filename}")

    capture_duration = 3
    start_time = time.time()

    while time.time() - start_time < capture_duration:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not capture frame.")
            break

        cv2.imshow("Live Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()