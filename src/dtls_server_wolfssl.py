import socket
from os import path
import logging

import wolfssl

from server import Server
import cfg as cfg
import scapy.all as sc

import time

"""
ifconfig 5 add fc::02/120
ifconfig 9 add fc::02/120
dtlsl fc::01 3
"""




logging.getLogger().setLevel(logging.NOTSET)
wolfssl.WolfSSL.enable_debug()


class DTLSServerWolfSSL(Server):
    MESSAGES = [
        'Client Hello 1',
        'Hello Verify Request',
        'Client Hello 2',
        'Server Hello, Certificate',
        'Server Key Exchange, Server Hello Done',
        'Client Key Exchange',
        'Change Cipher Spec, Encrypted Handshake Message 1',
        'Change Cipher Spec, Encrypted Handshake Message 2',
    ]
    def __init__(self, address: str, port: int) -> None:
        self.ctx = wolfssl.SSLContext(wolfssl.PROTOCOL_DTLSv1_2, server_side=True)
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.socket.bind((address, port))

        # Load the server certificate and key
        cert_path = path.join(path.abspath(path.dirname(__file__)), "certs")
        keyfile=path.join(cert_path, "key.pem")
        certfile=path.join(cert_path, "cert.pem")
        self.ctx.load_cert_chain(certfile, keyfile)


    def wait_for_connection(self):
        self.ctx.set_ciphers('DHE-RSA-AES128-SHA')
        #self.ctx.set_ciphers('DEFAULT')
        self.ctx.verify_mode = wolfssl.CERT_NONE
        self.ss = self.ctx.wrap_socket(self.socket)
        wolfssl._lib.wolfSSL_dtls_set_timeout_init(self.ss.native_object, 20)


        #sniffer = sc.AsyncSniffer(iface=['enp0s31f6'], filter='udp')
        sniffer = sc.AsyncSniffer(iface=['wlp4s0'], filter='udp')

        sniffer.start()
        time.sleep(0.08)


        self.ss.do_handshake()
        print('Connected')


        sniffer.stop()
        if len(sniffer.results) != len(self.MESSAGES):
            print(f'Different number of messages {len(sniffer.results)}')
        else:
            p0 = sniffer.results[0].time
            for idx, p in enumerate(sniffer.results):
                p: sc.Packet
                print(f'{self.MESSAGES[idx]} {(p.time - p0)}')

    def receive(self) -> bytes:
        return self.ss.read(cfg.BUFFER_SIZE)

    def send(self, m: bytes):
        self.ss.write(m)

    def close_connection(self):
        if self.ss:
            self.ss.shutdown(socket.SHUT_RDWR)
            self.ss.close()
        self.socket.close()
        self.socket = self.ctx = self.ss = None
