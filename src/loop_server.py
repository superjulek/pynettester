from server import Server


def loop_server(server: Server):
    while True:
        try:
            server.wait_for_connection()
            m = server.receive()
            print(f"Received {len(m)} bytes, responding same")
            server.send(m)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            break
    server.close_connection()
