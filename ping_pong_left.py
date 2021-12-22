from tkinter import *
import random
import socket
from threading import *

WIDTH = 500
HEIGHT = 400
 

LEFT_PAD_W = 10
LEFT_PAD_H = 100
RIGHT_PAD_W = 0
RIGHT_PAD_H = 0

PAD_H = 100
PAD_W = 10

BALL_SPEED_UP = 1.0
BALL_MAX_SPEED = 30
BALL_RADIUS = 30

INITIAL_SPEED = 1
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

left_comp_ip = '192.168.0.150'
middle_comp_ip = '192.168.0.150'
right_comp_ip = '192.168.0.150'

SEND_IP_PORT1 = (left_comp_ip,10000)
SEND_IP_PORT2 = (middle_comp_ip,10002)
SEND_IP_PORT2_2 = (middle_comp_ip,10003)
SEND_IP_PORT3 = (right_comp_ip,10004)

RECV_IP_PORT1 = (left_comp_ip,12000)
RECV_IP_PORT2 = (middle_comp_ip,12001)
RECV_IP_PORT3 = (right_comp_ip,12002)



have_ball = False
def send() : 
    global have_ball,BALL_Y_CHANGE,BALL_X_CHANGE,BALL_X_SPEED,BALL_Y_SPEED
    soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    soc.bind(SEND_IP_PORT1)
    msg_l = c.coords(BALL)
    msg = str(msg_l[0]) + ',' + str(msg_l[1]) + ',' + str(msg_l[2]) + ',' + str(msg_l[3]) + ',' + str(BALL_X_CHANGE) + ','+ str(BALL_Y_CHANGE) + ',' + 'LEFT'
    msg = msg.encode('UTF-8')
    soc.sendto(msg,RECV_IP_PORT2)
    soc.sendto(msg,RECV_IP_PORT2)
    BALL_Y_SPEED = 0
    BALL_X_SPEED = 0
    c.coords(BALL,200,200,200,200)
    have_ball = False

def t_func_recv() : 
    global have_ball,BALL_Y_CHANGE,BALL_X_CHANGE,BALL_X_SPEED,BALL_Y_SPEED
    if have_ball == False :
        c.coords(BALL,200,200,200,200)
        BALL_Y_SPEED = 0
        BALL_X_SPEED = 0
        soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        soc.bind(RECV_IP_PORT1)
        msg = soc.recv(1024)
        msg = msg.decode('UTF-8')
        msg = msg.split(',')
        print(msg)
        c.coords(BALL,WIDTH-50,msg[1],WIDTH-20,msg[3])
        BALL_Y_SPEED = float(msg[5])
        BALL_X_SPEED = -10
        have_ball = True
    if have_ball == True : 
        pass
    root.after(10,t_func_recv)

right_line_distance = WIDTH - PAD_W


def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = -10

def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED


root = Tk()
root.title("left")

c = Canvas(root, width=WIDTH, height=HEIGHT, background= "#3bff83")
c.pack()
 

BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
                     HEIGHT/2-BALL_RADIUS/2,
                     WIDTH/2+BALL_RADIUS/2,
                     HEIGHT/2+BALL_RADIUS/2, fill="#300081")
 

LEFT_PAD = c.create_line(LEFT_PAD_W/2, 0, LEFT_PAD_W/2, LEFT_PAD_H, width=LEFT_PAD_W, fill="yellow")
 

RIGHT_PAD = c.create_line(WIDTH-RIGHT_PAD_W/2, 0, WIDTH-RIGHT_PAD_W/2, 
                          RIGHT_PAD_H, width=RIGHT_PAD_W, fill="yellow")

BALL_X_CHANGE = 20
BALL_Y_CHANGE = 0
 
def move_ball():
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W:
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")
            else:
                send()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce("strike")
            else:
                spawn_ball()
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)

    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

PAD_SPEED = 20

LEFT_PAD_SPEED = 0

RIGHT_PAD_SPEED = 0
 

def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED, 
            RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:

        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

 
def main():
    move_ball()
    move_pads()

    root.after(30, main)


c.focus_set()
 

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED
 

c.bind("<KeyPress>", movement_handler)
 

def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in "ws":
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0

c.bind("<KeyRelease>", stop_pad)


t1 = Thread(target=t_func_recv)
t1.start()



main()


root.mainloop()
