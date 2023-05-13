import socket
from os import path

from dtls.sslconnection import SSLConnection

from server import Server
import cfg as cfg


class DTLSServer(Server):
    def __init__(self, address: str, port: int) -> None:
        cert_path = path.join(path.abspath(path.dirname(__file__)), "certs")
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.socket.bind((address, port))
        self.socket.settimeout(cfg.TIMEOUT)

        self.connection = SSLConnection(
            self.socket,
            keyfile=path.join(cert_path, "key.pem"),
            certfile=path.join(cert_path, "cert.pem"),
            server_side=True,
            ca_certs=path.join(cert_path, "cert.pem"),
            ciphers='AES128-SHA',
            do_handshake_on_connect=True  # TODO: verify
            )

    def wait_for_connection(self):
        address = self.connection.listen()
        assert address, 'No connection'
        print(f'Connected {address}')
        self.established_connection = self.connection.accept()[0]

    def receive(self) -> bytes:
        return self.established_connection.read(cfg.BUFFER_SIZE)

    def send(self, m: bytes):
        self.established_connection.write(m)

    def close_connection(self):
        s = self.established_connection.unwrap()
        s.close()
        self.socket.close()
        self.established_connection = self.connection = None
