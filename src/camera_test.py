import cv2
import os

# Camera setup
cap = cv2.VideoCapture(4)

if not cap.isOpened():
    print("❌ Cannot open Logitech B525 camera")
    exit()

print("✅ Logitech B525 camera opened successfully.")

# Create directory to save photos
save_dir = "captured_images"
os.makedirs(save_dir, exist_ok=True)

# UI Button positions
capture_btn = (30, 400, 200, 460)
exit_btn = (240, 400, 410, 460)

photo_count = 0

# Window name (no emoji for Wayland compatibility)
window_name = "Logitech B525 Camera"

# Create a named window BEFORE setting callback
cv2.namedWindow(window_name)

def mouse_click(event, x, y, flags, param):
    global photo_count
    frame = param["frame"]
    cap = param["cap"]

    if event == cv2.EVENT_LBUTTONDOWN:
        # Capture button
        if capture_btn[0] < x < capture_btn[2] and capture_btn[1] < y < capture_btn[3]:
            photo_count += 1
            filename = os.path.join(save_dir, f"photo_{photo_count}.jpg")
            cv2.imwrite(filename, frame)
            print(f"✅ Saved: {filename}")
        # Exit button
        elif exit_btn[0] < x < exit_btn[2] and exit_btn[1] < y < exit_btn[3]:
            print("👋 Exiting camera app...")
            cap.release()
            cv2.destroyAllWindows()
            exit(0)

# Set the callback once
cv2.setMouseCallback(window_name, mouse_click, {"frame": None, "cap": cap})

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    # Draw buttons
    cv2.rectangle(frame, (capture_btn[0], capture_btn[1]), (capture_btn[2], capture_btn[3]), (0, 255, 0), -1)
    cv2.rectangle(frame, (exit_btn[0], exit_btn[1]), (exit_btn[2], exit_btn[3]), (0, 0, 255), -1)

    cv2.putText(frame, "Capture", (capture_btn[0] + 40, capture_btn[1] + 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(frame, "Exit", (exit_btn[0] + 70, exit_btn[1] + 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Update callback parameter
    cv2.setMouseCallback(window_name, mouse_click, {"frame": frame.copy(), "cap": cap})

    cv2.imshow(window_name, frame)

    # Exit on ESC
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

