import cv2
import numpy as np
import socket
import threading

# Set up UDP socket
UDP_IP = "172.24.0.122" # Broadcast IP address. Leave it as it is
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set up video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # Reduce image size
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50] # Reduce video quality

def send_video():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to bytes
        _, frame_bytes = cv2.imencode('.jpg', frame, encode_param)
        data = frame_bytes.tobytes()

        # Send frame over UDP
        sock.sendto(data, (UDP_IP, UDP_PORT))
        
        # Display frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()

# Start video capture and transmission thread
thread = threading.Thread(target=send_video)
thread.start()

# Wait for thread to complete
thread.join()

# Close the socket
sock.close()
