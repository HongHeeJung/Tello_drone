# ---------------------------------------
# Streaming
# ---------------------------------------

# Import Module.
import socket
import time
import logging



tello_address = ('192.168.10.1', 8889)   # Tello
local_address = ('', 8889)

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

    send('streamon')
    receive()
    time.sleep(5)

    send('streamoff')
    receive()
    time.sleep(2)

    # (3) 통신 종료
    sock.close()