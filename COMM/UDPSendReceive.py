# -------------------------------------------------------------
# Send & Receive commands to/from Tello
# -------------------------------------------------------------

# 모듈 추가 ----------------------------------------------------
import socket
import time

# IP & Port 설정 ----------------------------------------------
tello_address = ('192.168.10.1', 8889)      # Tello
local_address = ('', 8889)                  # Local

# UDP Connetion Socket 생성 ------------------------------------
# 데이터 주고 받을 통로 설정 : IP주소방식, 데이터 송수신 방식
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 생성된 통로를 찾을 수 있도록 IP주소랑 포트 설정 연결
sock.bind(local_address)

# ------------------------------------------------------------------
# 함수 : 자주 사용하는 코드에 이름을 붙인것, 이름 불러서 사용
# ------------------------------------------------------------------
# Tello에 메시지 전송 함수 --------------------------------------------
def send(message):
  try:
    # 텔로에게 messasge 보내기
    num=sock.sendto(message.encode(encoding='utf-8'), tello_address)
    print("Sending message: " + message +" Sending bytes => " + str(num))
  except Exception as e:
    print("Error sending: " + str(e))

# # Tello로부터 메시지 수신 함수 ------------------------------------------
def receive():
  try:
    response, ip_address = sock.recvfrom(1024)  # 1024byte
    print("Rx message: " + response.decode(encoding='utf-8')
                         + " from Tello with IP: " + str(ip_address))
    return response.decode(encoding='utf-8')
  except Exception as e:
    print("Error receiving: " + str(e))
    return "error"

# ------------------------------------------------------------------
# Main 기능
# ------------------------------------------------------------
# 해당 파이썬 파일이 run할때만 동작하는 코드
if __name__ == '__main__':
  # while True:
  #   cmd=input("Enter command : ")
  #   sec=int(input("Enter second : "))
  #
  #   send(cmd)                 # Tello command
  #   receive()                 # 응답
  #   time.sleep(sec)           # 지정된 초만큼 일시 정지
  #
  #   if cmd=="land": break     # '착륙'으로 통신 종료

  send('command')             # Tello command
  receive()                   # 응답
  time.sleep(2)               # 지정된 초만큼 일시 정지

  cmd = f"ap {'so'} {'so123456'}"
  send(cmd)                   # ap 설정
  receive()                   # 응답
  time.sleep(2)               # 지정된 초만큼 일시 정지

  sock.close()                # UDP Socket 닫기