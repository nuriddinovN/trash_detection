# display.py

import cv2
from ultralytics import YOLO
from trash_detector import load_and_tune_model

def run_realtime_detection(model_path="prompt_tuned_trash.pt", class_mapping=None, confidence_thresh=0.4):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(0)  # Logitech B525 main camera stream


    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    print("🎬 Running detection... Press 'Stop' button or 'q' to quit.")

    stop_button_coords = (20, 20, 120, 60)  # (x1, y1, x2, y2)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=confidence_thresh)

        display_label = "others (reject)"
        display_conf = 0.0

        if len(results[0].boxes) > 0:
            # Get highest confidence detection
            top_box = max(results[0].boxes, key=lambda b: b.conf[0])
            raw_label = results[0].names[int(top_box.cls[0])]
            label = class_mapping.get(raw_label, "others")
            conf = float(top_box.conf[0])
            display_label, display_conf = label, conf

            x1, y1, x2, y2 = map(int, top_box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{display_label} ({display_conf:.2f})",
                        (x1, max(30, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            cv2.putText(frame, display_label,
                        (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Draw "Stop" button
        x1, y1, x2, y2 = stop_button_coords
        cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 50, 255), -1)
        cv2.putText(frame, "Stop", (x1 + 20, y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Trash Detection", frame)

        # Handle key or button click
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        # Handle mouse clicks
        def mouse_click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                if x1 < x < x2 and y1 < y < y2:
                    print("🛑 Stopped by button click.")
                    cap.release()
                    cv2.destroyAllWindows()
                    exit(0)

        cv2.setMouseCallback("Trash Detection", mouse_click)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    tuned_model, class_map = load_and_tune_model()
    run_realtime_detection(tuned_model, class_mapping=class_map)

