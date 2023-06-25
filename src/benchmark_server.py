import random
import time
import socket

import scapy.all as sc

from server import Server
import cfg
from results_utils import save_results, ResList


class TooManyPackets(Exception):
    ...

IFACES=['tap0', 'enp0s31f6', 'wlp4s0']
IFACES = ['enp0s31f6']
IFACES = ['wlp4s0']
LOOP_NUM = 10


def benchmark_server(server: Server):
    results = ResList()
    server.wait_for_connection()
    for _ in range(LOOP_NUM):
        for i in range(1, cfg.BUFFER_SIZE - 1):
            m = bytes([random.randint(0, 255) for _ in range(i)])
            iface = 'unknown'
            for _retry in range(cfg.RETIRES):
                try:

                    sniffer = sc.AsyncSniffer(iface=IFACES, filter='esp or udp')
                    sniffer.start()
                    time.sleep(0.08)

                    b = time.monotonic_ns()
                    server.send(m)
                    response = server.receive()
                    e = time.monotonic_ns()
                    sniffer.stop()

                    nettime = 0
                    if len(sniffer.results) == 2:
                        pout: sc.Packet
                        pin: sc.Packet
                        pout, pin = sniffer.results
                        nettime = pin.time - pout.time
                        iface = pin.sniffed_on
                    else:
                        raise TooManyPackets(f'Received {len(sniffer.results)} packets')

                    assert response == m, 'Received other data'
                    print(f'{i:0>4} bytes in {(e - b) / 1000.:0>8.3f} us ({nettime*1000000:0>8.3f})')
                    results.append([i, nettime])
                except (TooManyPackets, socket.timeout) as e:
                    print(e)
                    time.sleep(0.1)
                    continue
                except Exception as e:
                    print(e)
                break
            save_results(results, server, iface)
    server.close_connection()
