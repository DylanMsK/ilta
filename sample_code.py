import socket
import time
import math
import stage

# User and Game Server Information
NICKNAME = '파이썬'
HOST = '127.0.0.1'
PORT = 1447 # Do not modify

# predefined variables(Do not modify these values)
TABLE_WIDTH = 254
TABLE_HEIGHT = 124
NUMBER_OF_BALLS = 5
HOLES = [ [0, 0], [130, 0], [260, 0], [0, 130], [130, 130], [260, 130] ]
cnt = 0
class Conn:
    def __init__(self):
        self.sock = socket.socket()
        print('Trying to Connect: ' + HOST + ':' + str(PORT))
        self.sock.connect((HOST, PORT))
        print('Connected: ' + HOST + ':' + str(PORT))
        send_data = '9901/' + NICKNAME
        self.sock.send(send_data.encode('utf-8'))
        print('Ready to play.\n--------------------')
    def request(self):
        self.sock.send('9902/9902'.encode())
        print('Received Data has been currupted, Resend Requested.')
    def receive(self):
        recv_data = (self.sock.recv(1024)).decode()
        print('Data Received: ' + recv_data)
        return recv_data
    def send(self, angle, power):
        merged_data = '%f/%d' % (angle, power)
        self.sock.send(merged_data.encode('utf-8'))
        print('Data Sent: ' + merged_data)
    def close(self):
        self.sock.close()

class GameData:
    def __init__(self):
        self.reset()
    def reset(self):
        self.balls = [[0, 0] for i in range(NUMBER_OF_BALLS)]
    def read(self, conn):
        recv_data = conn.receive()
        split_data = recv_data.split('/')
        idx = 0
        try:
            for i in range(NUMBER_OF_BALLS):
                for j in range(2):
                    self.balls[i][j] = int(split_data[idx])
                    idx += 1
        except:
            self.reset()
            conn.request()
            self.read(conn)
    def show(self):
        print('=== Arrays ===')
        for i in range(NUMBER_OF_BALLS):
            print('Ball%d: %d, %d' % (i, self.balls[i][0], self.balls[i][1]))
        print()

# 자신의 차례가 되어 게임을 진행해야 할 때 호출되는 Method
def play(conn, gameData):
    left = find_targets(gameData)[0]
    print(left)
    angle = left[2] + math.degrees(math.atan(10.5/left[3]))
    print('angle: {}'.format(math.degrees(math.atan(10.5/left[3]))))
    # angle = find_degree(gameData.balls[0], left[:-1])
    # print(math.degrees(math.atan(10.5/left[-1])))
    conn.send(angle, 100)
    # degree = find_degree(gameData, left[0])
    # print('Degree: {}'.format(degree))

def find_degree(white, ball):
    # white = gameData.balls[0]
    dx = white[0] - ball[0]
    dy = white[1] - ball[1]
    if dx == 0 and dy > 0:
        return 0
    elif dx == 0 and dy < 0:
        return 180
    elif dx < 0 and dy <= 0:    # 1사분면
        return 90 - math.degrees(math.atan(abs(dy/dx)))
    elif dx < 0 and dy > 0:     # 2사분면
        return 90 + math.degrees(math.atan(abs(dy/dx)))
    elif dx > 0 and dy > 0:     # 3사분면
        return 180 + math.degrees(math.atan(abs(dy/dx)))
    elif dx > 0 and dy <= 0:    # 4사분면
        return 270 + math.degrees(math.atan(abs(dy/dx)))
    else:
        print('이상함')
        return -1

def get_distance(ball1, ball2):
    return ((ball1[0]-ball2[0])**2 + (ball1[1]-ball2[1])**2)**0.5


def find_targets(gameData):
    balls = gameData.balls
    white = balls[0]
    left = []
    for i in range(1, NUMBER_OF_BALLS):
        if balls[i][0] != 0 and balls[i][1] != 0:
            degree = find_degree(white, balls[i])
            distance = get_distance(white, balls[i])
            print('Ball{}: ({}, {}), Degree: {}, Distance: {}'.format(i, balls[i][0], balls[i][1], degree, distance))
            left.append([balls[i][0], balls[i][1], degree, distance])

    return left

def main():
    conn = Conn()
    gameData = GameData()
    while True:
        gameData.read(conn)
        gameData.show()
        play(conn, gameData)        
    conn.close()
    print('Connection Closed')

if __name__ == '__main__':
    main()
