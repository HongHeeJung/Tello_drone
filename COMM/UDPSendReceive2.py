# -------------------------------------------------------------
# Send & Receive commands to/from Tello
# -------------------------------------------------------------

# 모듈 추가 ----------------------------------------------------
import socket
import time

# IP & Port 설정 ----------------------------------------------
tello_address = ('192.168.10.1', 8889)  # Tello
local_address = ('', 8889)  # Local

# UDP Connetion Socket 생성 ------------------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_address)


# ------------------------------------------------------------------
# 함수
# ------------------------------------------------------------------
# Tello에 메시지 전송 함수 --------------------------------------------
def send(message):
    try:
        sock.sendto(message.encode(), tello_address)
        print("Sending message: " + message)
    except Exception as e:
        print("Error sending: " + str(e))


# Tello로부터 메시지 수신 함수 ------------------------------------------
def receive():
    try:
        response, ip_address = sock.recvfrom(1024)
        print("Received message: " + response.decode(encoding='utf-8')
              + " from Tello with IP: " + str(ip_address))
        return response.decode(encoding='utf-8')
    except Exception as e:
        print("Error receiving: " + str(e))
        return "error"


# ------------------------------------------------------------------
# Main 기능
# ------------------------------------------------------------------
if __name__ == '__main__':
    # Tello Drone에게 보낼 명령어들
    cmd = ['command', 'takeoff', 'forward 50', 'flip r', 'land']
    sec = [2, 2, 5, 3, 2]

    count = len(cmd)

    for i in range(count):  # 0~4까지 범위
        send(cmd[i])        # Tello Drone에게 명령어 전달
        receive()           # Tello Drone으로부터 응답 받기
        time.sleep(sec[i])  # 지정된 시간 일시 정지

    sock.close()            # UDP Socket 닫기

