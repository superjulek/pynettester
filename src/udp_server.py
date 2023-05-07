import socket

from server import Server
import cfg as cfg


class UDPServer(Server):
    def __init__(self, address: str, port: int) -> None:
        self.socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.socket.bind((address, port))
        self.socket.settimeout(cfg.TIMEOUT)
        self.remote_address = None

    def wait_for_connection(self):
        message, address = self.socket.recvfrom(1500)
        print(f'Received {len(message)} bytes ({message.decode()}) from {address}')
        self.remote_address = address

    def receive(self) -> bytes:
        message, address = self.socket.recvfrom(1500)
        self.remote_address = address
        return message

    def send(self, m: bytes):
        assert self.remote_address is not None, 'Address unknown'
        self.socket.sendto(m, self.remote_address)

    def close_connection(self):
        self.socket.close()
        self.remote_address = None
