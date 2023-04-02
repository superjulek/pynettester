import socket


def run_server():
    print('Server starting')

    sck = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sck.bind(("aa::01", 11111))
    sck.settimeout(30)

    cnt = 0
    while True:
        cnt += 1
        print("Read invocation: %d" % cnt)
        try:
            message, address = sck.recvfrom(1500)
            print(f"Received {len(message)} bytes")
            sck.sendto(message, address)
        except Exception as e:
            print(e)

    sck.close()
