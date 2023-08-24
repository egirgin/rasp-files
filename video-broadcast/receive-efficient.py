import cv2
import numpy as np
import socket
import datetime

# Set up UDP socket
UDP_IP = "" # Leave empty to receive from any IP address
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Set up video display window
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)


img_width = 320
img_height = 240

result = cv2.VideoWriter("{}.avi".format(datetime.datetime.now()), cv2.VideoWriter_fourcc(*'MJPG'), 10, (img_width, img_height))


while True:
    # Receive frame over UDP
    data, addr = sock.recvfrom(65535)
    frame_bytes = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(frame_bytes, cv2.IMREAD_COLOR)

    # Display frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    result.write(frame)
    
    
result.release()
# Close the window and the socket
cv2.destroyAllWindows()
sock.close()

