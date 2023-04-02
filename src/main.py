
import argparse

from dtls_server import run_server as run_dtls_server
from udp_server import run_server as run_udp_server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ds', '--dtls_server', action='store_true', help='run DTLS server')
    parser.add_argument('-us', '--udp_server', action='store_true', help='run UDP server')
    args = parser.parse_args()
    if args.dtls_server:
        run_dtls_server()
    elif args.udp_server:
        run_udp_server()

if __name__ == '__main__':
    main()