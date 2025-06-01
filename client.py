import random
import tkinter as tk
from socket import *
import _thread

from TicTacToe import TTT, check_msg
    


if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        
        ###################################################################
        # Receive who will start first from the server
        start = int(client_socket.recv(SIZE).decode())
    
        ######################### Fill Out ################################
        # Send ACK 
        client_socket.sendall("ACK".encode())

        f_msg = client_socket.recv(SIZE).decode()

        if "First-Move: YOU" in f_msg: #서버가 클라이언트에게 먼저 시작하라고 한 경우
            ACK = f"ACK ETTTP/1.0\r\nHost:{MY_IP}\r\nFirst-Move: ME\r\n\r\n"
        else: #서버가 먼저 시작한 경우
            ACK = f"ACK ETTTP/1.0\r\nHost:{MY_IP}\r\nFirst-Move: YOU\r\n\r\n"

        client_socket.sendall(ACK.encode())
        print(ACK) #디버깅용 출력
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        