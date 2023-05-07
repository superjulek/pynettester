from server import Server


def reply_server(server: Server):
    server.wait_for_connection()
    while True:
        try:
            m = server.receive()
            print(f"Received {len(m)} bytes, responding same")
            server.send(m)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            break
    server.close_connection()
