import random
import time
import socket

from server import Server
import cfg
from results_utils import save_results, ResList


POW_SIZE = 200

def power_server(server: Server):
    results = ResList()
    server.wait_for_connection()
    good = 0
    start_time = time.monotonic_ns()
    try:
        while True:
            m = bytes([random.randint(0, 255) for _ in range(POW_SIZE)])
            for _retry in range(100):
                try:
                    server.send(m)
                    response = server.receive()
                    assert response == m, f'Received other data ({response.decode(errors="ignore")})'
                    if good % 100 == 0:
                        print(f'{good} loop, {(time.monotonic_ns() - start_time) / 10**9:.1f} s')
                    good += 1
                    break
                except Exception as e:
                    print(e)
                    time.sleep(0.5)
    except KeyboardInterrupt:
        ...
    print(f'\n\n{good}, {time.monotonic_ns() - start_time}, {POW_SIZE}\n\n')
    server.close_connection()
