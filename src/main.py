
import argparse

from dtls_server import run_server as run_dtls_server, run_benchmark as run_dtls_benchmark
from udp_server import run_server as run_udp_server, run_benchmark as run_udp_benchmark


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ds', '--dtls_server', action='store_true', help='run DTLS server')
    parser.add_argument('-us', '--udp_server', action='store_true', help='run UDP server')
    parser.add_argument('-ub', '--udp_benchmark', action='store_true', help='run UDP benchmark')
    parser.add_argument('-db', '--dtls_benchmark', action='store_true', help='run DTLS benchmark')
    args = parser.parse_args()
    if args.dtls_server:
        run_dtls_server()
    elif args.udp_server:
        run_udp_server()
    elif args.udp_benchmark:
        run_udp_benchmark()
    elif args.dtls_benchmark:
        run_dtls_benchmark()

if __name__ == '__main__':
    main()