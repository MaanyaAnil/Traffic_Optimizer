import cv2
import os
from ultralytics import YOLO # Import YOLO

model = YOLO('yolov8n.pt')

def detect_vehicles(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file: {video_path}")
            return 0  # Return 0 if video cannot be opened

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 video
        output_path = 'processed_video.mp4'  # You can change the output file name
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        vehicle_count = 0  # Initialize vehicle count
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)

            for result in results:
                for box in result.boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    # Get confidence score
                    confidence = box.conf[0]
                    # Get class name
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id]
                    if confidence > 0.5 and (class_id == 2 or class_id == 7):  # Count cars and trucks
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green bounding box
                        label = f'{class_name}: {confidence:.2f}'
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        vehicle_count += 1

            out.write(frame)  # Write the frame with bounding boxes to the output video

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        return vehicle_count  # Return the count of vehicles

    except Exception as e:
        print(f"Error processing video {video_path}: {e}")
        return 0  # Return 0 if any error occurs


# Load the model.  This should ideally happen *once* in app.py and be passed in, but we'll load it here for this example
try:
    model = YOLO('yolov8n.pt')  # Or your model path
    print("YOLO model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    model = None # Set model to None to prevent errors later


def process_video_with_yolov8(video_path, output_dir):
    processed_path = None
    vehicle_count = 0
    print(f"Attempting to process video: {video_path}")
    try:
        cap = cv2.VideoCapture(video_path)
        if cap is None or not cap.isOpened():
            print(f"Error: Could not open video file: {video_path}")
            return None, 0

        print(f"Successfully opened video: {video_path}")
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_filename = f"processed_{os.path.basename(video_path)}"
        processed_path = os.path.join(output_dir, output_filename)
        out = cv2.VideoWriter(processed_path, fourcc, fps, (frame_width, frame_height))
        print(f"Output video will be saved to: {processed_path}")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if model is None: # Check if model loaded
                print("YOLO model is not loaded. Skipping detection.")
                out.write(frame) # Write original frame.
                continue

            results = model(frame)  # Assuming 'model' is your YOLO model
            print(f"Number of results: {len(results)}") # Check number of results

            for result in results:
                print(f"Number of boxes in a result: {len(result.boxes)}") # Check boxes
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = box.conf[0]
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id]
                    print(f"Detected: {class_name}, Confidence: {confidence}, Box: ({x1}, {y1}, {x2}, {y2})") # Print detection info

                    if confidence > 0.5 and (class_id == 2 or class_id == 7):
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f'{class_name}: {confidence:.2f}'
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        vehicle_count += 1

            out.write(frame)  # Write the processed frame to the output video

        cap.release()
        out.release()
        print(f"Finished processing video: {video_path}, vehicle count: {vehicle_count}, output at {processed_path}")
        return processed_path, vehicle_count

    except Exception as e:
        print(f"General error processing {video_path}: {e}")
        return None, 0