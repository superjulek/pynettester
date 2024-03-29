
import argparse

from dtls_server import DTLSServer
from dtls_server_wolfssl import DTLSServerWolfSSL
from udp_server import UDPServer
from reply_server import reply_server
from benchmark_server import benchmark_server
from loop_server import loop_server
from performance_server import performance_server
from power_server import power_server
import cfg


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dtls', action='store_true', help='use DTLS')
    parser.add_argument('-w', '--wolfssl_dtls', action='store_true', help='use WolfSSL DTLS')
    parser.add_argument('-u', '--udp', action='store_true', help='use UDP')

    parser.add_argument('-r', '--reply', action='store_true', help='run reply server')
    parser.add_argument('-b', '--benchmark', action='store_true', help='run benchmark server')
    parser.add_argument('-l', '--loop', action='store_true', help='run loop server')
    parser.add_argument('-p', '--performance', action='store_true', help='run performance server')
    parser.add_argument('-o', '--power', action='store_true', help='run power server')

    args = parser.parse_args()

    if args.dtls:
        s = DTLSServer(cfg.ADDRESS, cfg.PORT)
    elif args.udp:
        s = UDPServer(cfg.ADDRESS, cfg.PORT)
    elif args.wolfssl_dtls:
        s = DTLSServerWolfSSL(cfg.ADDRESS, cfg.PORT)
    else:
        raise Exception('No Server option selected')

    if args.reply:
        f = reply_server
    elif args.benchmark:
        f = benchmark_server
    elif args.loop:
        f = loop_server
    elif args.performance:
        f = performance_server
    elif args.power:
        f = power_server
    else:
        raise Exception('No server selected')
    f(s)


if __name__ == '__main__':
    main()
