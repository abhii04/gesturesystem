import cv2
import serial
import mediapipe as mp

# Set up Arduino connection
arduino = serial.Serial('COM3', 9600)

# Set up MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Set up drawing module
mp_drawing = mp.solutions.drawing_utils

# Main loop
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the image to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image with MediaPipe Hands
    results = hands.process(image_rgb)

    # Draw hand landmarks on the image
    image_out = frame.copy()
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image_out, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Get the hand gesture based on landmarks
        landmarks = results.multi_hand_landmarks[0].landmark
        thumb_x = landmarks[4].x
        thumb_y = landmarks[4].y
        thumb_tip_x = landmarks[8].x
        thumb_tip_y = landmarks[8].y

        # Check thumb gesture
        if thumb_y > thumb_tip_y:
            arduino.write(b'1')  # Send '1' to Arduino (Thumbs Up gesture)
        else:
            arduino.write(b'0')  # Send '0' to Arduino (Thumbs Down gesture)

    # Display the image with landmarks
    cv2.imshow('Hand Gestures', image_out)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
