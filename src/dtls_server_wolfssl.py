import socket
from os import path
import logging

import wolfssl

from server import Server
import cfg as cfg


logging.getLogger().setLevel(logging.NOTSET)
wolfssl.WolfSSL.enable_debug()


class DTLSServerWolfSSL(Server):
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
        self.ss.do_handshake()
        # print(f'Connected {from_addr}')
        print('Connected')

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
