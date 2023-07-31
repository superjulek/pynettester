import random
import time
import socket

from server import Server
import cfg
from results_utils import save_results, ResList


LOOP_NUM = 10000


def performance_server(server: Server):
    results = ResList()
    server.wait_for_connection()
    good = 0
    total_time = 0
    try:
        while good < LOOP_NUM:
            m = bytes([random.randint(0, 255) for _ in range(cfg.PERFORMANCE_SIZE)])
            for _retry in range(cfg.RETIRES):
                try:
                    b = time.monotonic_ns()
                    server.send(m)
                    response = server.receive()
                    e = time.monotonic_ns()
                    nettime = e - b
                    assert response == m, 'Received other data'
                    if good % 100 == 0:
                        print(f'{good:0>5.0f} loop, last in {(e - b) / 1000.:0>8.3f} us')
                    total_time += nettime
                    good += 1
                    break
                except socket.timeout as e:
                    print(e)
                    time.sleep(0.1)
                    continue
                except Exception as e:
                    print(e)
    except KeyboardInterrupt:
        ...
    results.append([total_time, good, cfg.PERFORMANCE_SIZE, 000, 000])
    save_results(results, server, 'perform_test')
    server.close_connection()
