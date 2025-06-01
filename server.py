import random
import tkinter as tk
from socket import *
import _thread

from TicTacToe import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept()
        
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        # Send start move information to peer
        client_socket.sendall(str(start).encode())
    
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        ack = client_socket.recv(SIZE).decode()
        if ack != 'ACK':
            client_socket.close()
            continue

        if start == 0 : #Server가 먼저 시작 
            msg = f"SEND ETTTP/1.0\r\nHost: {MY_IP}\r\nFirst-Move: ME\r\n\r\n"
        else : #Client가 먼저 시작  
            msg = f"SEND ETTTP/1.0\r\nHost: {MY_IP}\r\nFirst-Move: YOU\r\n\r\n"

        print(msg)
        client_socket.sendall(msg.encode())

        f_ack = client_socket.recv(SIZE).decode()
        if not f_ack.startswith('ACK'):
            client_socket.close()
            continue
        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()