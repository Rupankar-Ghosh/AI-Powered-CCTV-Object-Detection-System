import torch
import cv2
import winsound  # For alarm sound on Windows
import getpass

find=input("Target : ")
#find="x"
# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Define a function to trigger the alarm
def trigger_alarm():
    winsound.Beep(1000, 500)  # Frequency: 1000 Hz, Duration: 500 ms

while True:
    p=getpass.getpass("Password")
    if p=="123":
        break

# Open video file
video_path = r"D:\CCTV\CCTV_Video\CCTV.mp4"  # Raw string to handle backslashes

cap = cv2.VideoCapture(video_path)
#cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv5 inference on the frame
    results = model(frame)
    
    # Extract detected objects
    labels = results.xyxy[0][:, -1].tolist()  # Get class labels
    names = results.names  # Get class names
    
    # Check if 'person' is detected
    if any(names[int(label)] == find for label in labels):
        trigger_alarm()

    # Display the results
    cv2.imshow('YOLOv5 Detection', results.render()[0])
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()