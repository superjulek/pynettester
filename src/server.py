class Server:
    def __init__(self, address: str, port: int) -> None:
        pass

    def wait_for_connection(self):
        pass

    def receive(self) -> bytes:
        pass

    def send(self, m: bytes):
        pass

    def close_connection(self):
        pass
