import socket
import shared
from game import Ship

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_score(name, score):
    sock.sendto(f'my score\r\n{name}\r\n{score}'.encode(
        'utf-8'), shared.SERVER_ADDRESS)


def req_connect():
    sock.sendto(b'connect', shared.SERVER_ADDRESS)


def req_scores():
    sock.sendto(b'get scores', shared.SERVER_ADDRESS)


def wait_for_data(type):
    data, addr = sock.recvfrom(256)

    string = data.decode('utf-8')

    if type == 'ships':
        ships = []
        for line in string.splitlines():
            args = line.split(' ')
            ship = Ship(int(args[2]), [int(args[0]), int(args[1])])
            ships.append(ship)
        return ships
    elif type == 'scores':
        return string
