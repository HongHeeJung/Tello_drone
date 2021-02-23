# ---------------------------------------
# Send & Receive commands to/from Tello
# ---------------------------------------

# Import Module.
import socket
import time
import cv2          # Video에서 수신된 데이터 처리 모듈

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
    # (1) Tello에게 sdk mode 시작 요청 command 전송
    send('command')
    receive()
    time.sleep(2)

    # 카메라로부터 수신된 영상 데이터 화면 출력
    cap = cv2.VideoCapture(video_address, cv2.CAP_FFMPEG)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            cv2.imshow('FROM Tello CAM'. frame)

    sock.close()


