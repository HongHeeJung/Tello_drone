# ---------------------------------------
# Receive state from Tello
# ---------------------------------------

# Import Module.
import socket
import time
import logging

# Create logger instance
logger = logging.getLogger(__name__)

# Create handler (stream, file)
streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler('./server.log')

# Set handler at logger instance.
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

# Set IP & Port.
tello_address = ('192.168.10.1', 8889)   # Tello
local_address = ('0.0.0.0', 8890) # State

# Create UDP Connection Socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(local_address)

# Function
# Func 1) Send Messages to Tello.
def send(message):
    try:
        sock.sendto(message.encode(), tello_address)
        print("Sending message: " + message)
    except Exception as e:
        print("Error sending: " + str(e))

# Func 2) Receive Messages from Tello.
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

    # (2) Tello로부터 Tello State 정보 수신
    for i in range(10):
        receive()  # Tello Drone으로부터 응답 받기
        time.sleep(2)  # 지정된 시간 일시 정지

    # (3) 통신 종료
    sock.close()


