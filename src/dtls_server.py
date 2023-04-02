import socket
from os import path
from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)  # set now for dtls import code
from dtls.sslconnection import SSLConnection
from dtls.err import SSLError, SSL_ERROR_WANT_READ, SSL_ERROR_ZERO_RETURN


def run_server():
    print('Server starting')



    cert_path = path.join(path.abspath(path.dirname(__file__)), "certs")

    sck = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sck.bind(("aa::01", 11111))
    sck.settimeout(30)

    scn = SSLConnection(
        sck,
        keyfile=path.join(cert_path, "key.pem"),
        certfile=path.join(cert_path, "cert.pem"),
        server_side=True,
        ca_certs=path.join(cert_path, "cert.pem"),
        do_handshake_on_connect=False)

    cnt = 0
    while True:
        cnt += 1
        print("Listen invocation: %d" % cnt)
        peer_address = scn.listen()
        if peer_address:
            print("Completed listening for peer: %s" % str(peer_address))
            break

    print("Accepting...")
    conn = scn.accept()[0]
    sck.settimeout(5)
    conn.get_socket(True).settimeout(5)

    cnt = 0
    while True:
        cnt += 1
        # print("Listen invocation: %d" % cnt)
        # peer_address = scn.listen()
        # assert not peer_address
        print("Handshake invocation: %d" % cnt)
        try:
            conn.do_handshake()
        except SSLError as err:
            if err.errno == 504:
                continue
            raise
        print("Completed handshaking with peer")
        break

    cnt = 0
    while True:
        cnt += 1
        # print("Listen invocation: %d" % cnt)
        # peer_address = scn.listen()
        # assert not peer_address
        print("Read invocation: %d" % cnt)
        try:
            message = conn.read(len=1500)
        except SSLError as err:
            if err.errno == 502:
                continue
            if err.args[0] == SSL_ERROR_ZERO_RETURN:
                break
            raise
        #print(message.decode())
        #conn.write(str("Back to you: " + message.decode()).encode())
        conn.write(message)

    cnt = 0
    while True:
        cnt += 1
        # print("Listen invocation: %d" % cnt)
        # peer_address = scn.listen()
        # assert not peer_address
        print("Shutdown invocation: %d" % cnt)
        try:
            s = conn.unwrap()
            s.close()
        except SSLError as err:
            if err.errno == 502:
                continue
            raise
        break

    sck.close()