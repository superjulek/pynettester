import socket
import wolfssl


bind_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bind_socket.connect(("0.0.0.0", 11111))

context = wolfssl.SSLContext(wolfssl.PROTOCOL_DTLSv1_2)

context.verify_mode = wolfssl.CERT_NONE

secure_socket = context.wrap_socket(bind_socket)

#secure_socket.connect(("0.0.0.0", 11111))

secure_socket.write(b"TEST")

print(secure_socket.read())

secure_socket.close()