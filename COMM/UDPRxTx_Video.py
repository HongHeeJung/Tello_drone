# ---------------------------------------
# Video streaming
# ---------------------------------------

# Import Module.
import socket
import time
import cv2          # Module to process data from Video

# Set IP & Port
tello_address = ('192.168.10.1', 8889)      # Tello
local_address = ('', 8889)                  # Local
video_address = 'udp://0.0.0.0:11111'       # Video Stream

# Create UDP Connection Socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_address)

# Function
# Func 1) Send Messages to Tello
def send(message):
    try:
        sock.sendto(message.encode(), tello_address)
        print("Sending message: " + message)
    except Exception as e:
        print("Error sending: " + str(e))

# Func 2) Receive Messages from Tello
def receive():
    try:
        response, ip_address = sock.recvfrom(1024) # 1024 byte
        print("Rx message: " + response.decode(encoding='utf-8')
                             + " from Tello with IP: " + str(ip_address))
        return response.decode(encoding='utf-8')
    except Exception as e:
        print("Error receiving: " + str(e))
        return "error"

# Main
if __name__== '__main__':
    # (1) Send command to Tello to start SDK mode.
    send('command')
    receive()
    time.sleep(2)

    # (2) Stream on.
    send('streamon')
    time.sleep(2)

    # (3) Show frame data from Camera.
    cap = cv2.VideoCapture(video_address, cv2.CAP_FFMPEG)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            cv2.imshow('FROM Tello CAM', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.imwrite('capture_02.jpg', frame)
                break
        else:
            print('No CAM !!')
            break

    # (4) Release Camera.
    cap.release()
    cv2.destroyWindow()
    send("streamoff")           # Turn off Video

    # (5)Close a socket.
    sock.close()


