import random
import time

from server import Server
import cfg

def benchmark_server(server: Server):
    server.wait_for_connection()
    for i in range(1, cfg.BUFFER_SIZE):
        m = bytes([random.randint(0, 255) for _ in range(i)])
        try:
            b = time.monotonic_ns()
            server.send(m)
            response = server.receive()
            e = time.monotonic_ns()
            assert response == m, 'Received other data'
            print(f'{i} bytes in {(e - b) / 1000.} us')
        except Exception as e:
            print(e)
    server.close_connection()
