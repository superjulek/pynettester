import socket
import random
import time


def run_server():
    print('Server starting')

    sck = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sck.bind(("fc::01", 11111))
    sck.settimeout(120)

    cnt = 0
    while True:
        cnt += 1
        try:
            message, address = sck.recvfrom(1500)
            print(f"Received {len(message)} bytes")
            sck.sendto(message, address)
        except Exception as e:
            print(e)

    sck.close()


def run_benchmark():
    print('Server starting')

    sck = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sck.bind(("fc::01", 11111))
    sck.settimeout(120)
    message, address = sck.recvfrom(1500)
    print(f'Received {message.decode()}, starting test')
    time.sleep(1)

    for i in range(1, 1400):
        m = bytes([random.randint(0, 255) for _ in range(i)])
        try:
            b = time.monotonic_ns()
            sck.sendto(m, address)
            response, _ = sck.recvfrom(1500)
            e = time.monotonic_ns()
            assert response == m, 'Received other data'
            print(f'{i} bytes in {(e - b) / 1000.} us')
        except Exception as e:
            print(e)

    sck.close()
