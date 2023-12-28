import socket
import random
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 7878))

clients = []

SCORES_PATH = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'server', 'scores')


def generate_ships():
    ships = ''
    y_offset = 40
    for i in range(10):
        ships += f'{random.randrange(-600, -200)} ' + \
            f'{y_offset} {random.randrange(2, 10)}\r\n'
        y_offset += 30

    return ships


def get_scores():
    with open(SCORES_PATH, 'r') as file:
        text = file.read()

    return text


def save_score(name, score):
    new_scores = {}

    with open(SCORES_PATH, 'r') as file:
        lines = file.read().splitlines()

        for line in lines:
            args = line.split(' ')
            new_scores[args[0]] = int(args[1])

    if name in new_scores.keys() and new_scores[name] < int(score):
        del new_scores[name]
        new_scores[name] = int(score)
    elif name not in new_scores.keys():
        new_scores[name] = int(score)

    new_scores_list = [(n, s) for n, s in new_scores.items()]
    new_scores_list = sorted(
        new_scores_list, key=lambda x: int(x[1]), reverse=True)[:10]

    string = ''

    for i in new_scores_list:
        string += f'{i[0]} {i[1]}\r\n'

    with open(SCORES_PATH, 'w') as file:
        file.write(string)


try:
    print('Server Started!')
    while True:
        data, address = sock.recvfrom(256)

        string = data.decode('utf-8')

        if string.startswith('connect'):
            print(f'{address} connected')
            clients.append(address)
            sock.sendto(generate_ships().encode('utf-8'), address)
        elif string.startswith('my score') and address in clients:
            print(f'{address} pushed his score')
            args = string.splitlines()[1:]
            save_score(args[0], args[1])
            clients.remove(address)
        elif string.startswith('get scores'):
            print(f'{address} requested scores')
            sock.sendto(get_scores().encode('utf-8'), address)
except KeyboardInterrupt:
    pass
finally:
    sock.close()
    quit()
