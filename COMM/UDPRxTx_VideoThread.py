# -------------------------------------------------------------
# Receive Video Data info from Tello
# -------------------------------------------------------------

# Import Module.
import socket
import time
import threading
import cv2

# Set IP & Port.
tello_address = ('192.168.10.1', 8889)      # Telloq
local_address = ('', 8889)                  # Local
video_address = 'udp://0.0.0.0:11111'       # Video Stream
video_on = False
cap = None

# Create UDP Connection Socket.
# 데이터 주고 받을 통로 설정 : IP 주소 방식, 데이터 송수신 방식
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 생성된 통로를 찾을 수 있도록 IP 주소랑 포트 설정 연결
sock.bind(local_address)

# Function
# Func 1) Send Messages to Tello.
def send(message):
  try:
    # 텔로에게 messasge 보내기
    num=sock.sendto(message.encode(), tello_address)
    print(" Sending message: " + message +" Sending bytes => " + str(num))
  except Exception as e:
    print(" Error sending: " + str(e))

# Func 2) Receive Messages from Tello.
def receive():
  try:
    response, ip_address = sock.recvfrom(1024)  # 1024byte
    print(" Rx message: " + response.decode(encoding='utf-8')
                         + " from Tello with IP: " + str(ip_address))
    return response.decode(encoding='utf-8')
  except Exception as e:
    print("Error receiving: " + str(e))
    return "error"

# Func 3) Camera.
def videoThread():
    global  video_on, cap
    video_on = True
    cap = cv2.VideoCapture(video_address, cv2.CAP_FFMPEG)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            cv2.imshow('FROM Tello CAM', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.imwrite('capture_02.jpg', frame)
                time.sleep(1)
                cap.release()
                cv2.destroyAllWindows()
                video_on = False
                break
        else:
            print('No CAM !!')
            break

# ------------------------------------------------------------------
# Main 기능
# ------------------------------------------------------------
# 해당 파이썬 파일이 run할 때만 동작하는 코드
if __name__ == '__main__':
    # (1) Tello에게 sdk mode 시작 요청 command 전송
    send("command")           # Tello command mode 진입
    receive()                 # ok 응답
    time.sleep(3)             # COMMAND 진입 대기

    send("streamon")          # Video Stream 켜기
    time.sleep(1)

    # UDP Video Stream 받기
    videoTh = threading.Thread(target=videoThread)
    videoThread.daemon = True
    videoTh.start()
    time.sleep(3)

    while video_on:
        print(f' video_on = {video_on}')

        cmd = ['takeoff', 'forward 50', 'flip r', 'cw 90', 'flip l', 'back 50', 'land']
        sec = [2, 7, 4, 3, 4, 7, 2]

        count = len(cmd)

        for i in range(count):  # 0~4까지 범위
            send(cmd[i])  # Tello Drone에게 명령어 전달
            receive()  # Tello Drone으로부터 응답 받기
            time.sleep(sec[i])  # 지정된 시간 일시 정지

        if cmd == "land":
            time.sleep(1)
            cap.release()
            cv2.destroyAllWindows()
            video_on = False
            break  # '착륙'으로 통신 종료

    send("streamoff")         # Video Stream 끄기
    sock.close()              # UDP Socket 닫기