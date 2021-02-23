# ---------------------------------------
# Send & Receive commands to/from Tello
# ---------------------------------------

# Import Module.
import socket
import time

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
    while True:
        cmd = input("Enter command : ")
        sec = int(input("Enter second : "))

        send(cmd)
        receive()
        time.sleep(sec)

        if cmd == "land" : break
    sock.close()

    '''
    # 아래처럼 list로 명령어를 입력할 수 있음
    cmd = ['command', 'takeoff', 'forward 50', 'flip r', 'land']
    sec = [2, 2, 5, 3, 2]
    
    count = len(cmd)
    for i in range(count):
        send(cmd[i])
        receive()
        time.sleep(sec[i])
    
    sock.close()
    '''

