import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-01-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"YOU"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"ME"}   
        else:
            self.myID = 0
            self.title('34743-01-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        msg =  self.socket.recv(SIZE).decode() # 소켓 사용하여 메세지 받기

        msg_valid_check = check_msg(msg, self.recv_ip) # 메세지가 유효한지 확인
        
        if not msg_valid_check: # 메세지가 유효하지 않은 경우
            self.socket.close()   
            self.quit()
            return
        else:  
            # If message is valid - send ack, update board and change turn
            coords_str = msg.strip().splitlines()[2].split(":")[1].strip("()") # 메시지에서 위치 추출
            row, col = coords_str.split(",") # 위치에서 행, 열 값 추출
            row = int(row) # 행 값 정수로 변환
            col = int(col) # 열 값 정수로 변환
            loc = row * 3 + col # 위치 계산
            ACK = f"ACK ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n"# ACK 메시지
            self.socket.send(ACK.encode()) # ACK 메시지 전송
            print(ACK) # 디버깅용 ACK 출력
            ######################################################   
            
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        if d_msg.startswith("SEND "):
            msg = d_msg[5:] # 메시지에서 "SEND " 부분 제거
            msg_lines = msg.splitlines() # 줄 단위로 분리
            move_line = msg_lines[2].strip() # New-Move: (row,col) 줄만 추출
            coordinate = move_line.split(":")[1].strip("()") # move_line에서 좌표 부분만 추출
            row, col = map(int, coordinate.split(",")) # 좌표에서 행, 열 값만 추출
            loc = row * 3 + col # 위치 계산

            # DEBUG: 이미 선택된 위치인지 확인
            if self.board[loc] != 0:
                print("[DEBUG ERROR] That cell is already taken.")
                self.t_debug.delete(1.0,"end")
                return
                
            # 상대에게 msg 전송
            # 수정 SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nNew-Move:(1,2)\r\n\r\n 와 같은 형식으로 보내야함
            send_msg = f"SEND ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n"
            self.socket.send(send_msg.encode())
            print(send_msg)  # 디버깅용 메시지 출력

            # ACK 수신 및 검증
            ack = self.socket.recv(1024).decode()
            if not ack.startswith("ACK ETTTP/1.0"):
                self.socket.close()
                self.quit()
                return

            ######################################################  
                
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.user, loc)
                    
            if self.state == self.active:    # always after my move
                self.my_turn = 0
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                _thread.start_new_thread(self.get_move,())
                    
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3)
        ###################  Fill Out  #######################

        # send message and check ACK

        # DEBUG: 이미 선택된 위치인지 확인
        if self.board[selection] != 0:
            print("[DEBUG ERROR] That cell is already taken.")
            return False

        # 상대에게 msg 전송
        #수정
        # 수정 SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nNew-Move:(1,2)\r\n\r\n 와 같은 형식으로 보내야함
        send_msg = f"SEND ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n"
        self.socket.send(send_msg.encode())
        print(send_msg)  # 디버깅용 메시지 출력

        # ACK 수신 및 검증
        ack = self.socket.recv(1024).decode()
        if not ack.startswith("ACK ETTTP/1.0"):
            self.socket.close()
            self.quit()
            return

        return True
            ######################################################  

    
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        if self.myID == 1:  # 클라이언트인 경우, Name 반전 필요
            if winner == "YOU":
                protocol_winner = "ME" 
            else: 
                protocol_winner = "YOU"  
        else:  # 서버인 경우
            protocol_winner = winner
    
        if not get: #내가 이긴 경우, 결과를 먼저 전송 
            msg = f"RESULT ETTTP/1.0\r\nHost: {self.send_ip}\r\nWinner: {protocol_winner}\r\n\r\n"
            self.socket.send(msg.encode())
            print(msg)

            ACK = self.socket.recv(1024).decode()
            if not ACK.startswith("RESULT ETTTP/1.0"):
                return False
            return True
        else: #내가 결과를 수신을 우선 -> 내가 졌을 때
            msg = self.socket.recv(1024).decode()
            if not msg.startswith("RESULT ETTTP/1.0"):
                 return False
            
            # recv_winner = msg.strip().splitlines()[2].split(":")[1].strip()
            ACK = f"RESULT ETTTP/1.0\r\nHost: {self.send_ip}\r\nWinner: {protocol_winner}\r\n\r\n"
            self.socket.send(ACK.encode())
            print(ACK)
            return True
        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip):
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    msg_lines = msg.strip().splitlines() # 수정

    isETTTP = False
    isVersionValid = False
    isHostValid = False
    # 아래 세 조건문 수정
    if msg_lines[0].split()[1].split("/")[0] == "ETTTP":
        isETTTP = True
    if msg_lines[0].split()[1].split("/")[1] == "1.0": 
        isVersionValid = True
    if msg_lines[1].split(":")[1] == recv_ip:
        isHostValid = True
  
    if not (isETTTP and isVersionValid and isHostValid):
        print("[DEBUG ERROR] Invalid message format")
        return False
    else:
        return True
    ######################################################  