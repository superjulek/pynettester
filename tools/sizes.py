import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

IV_SIZE = 16
BLOCK_SIZE = 16
IP_HEADER_SIZE = 40
UDP_HEADER_SIZE = 8

# ESP
ESP_HEADER_SIZE = 8
NEXT_HEADER_SIZE = 1
ESP_PAD_LEN_SIZE  = 1
ESP_ICV_SIZE = 12

# DTLS
DTLS_HEADER_SIZE = 13
DTLS_PAD_LEN_SIZE  = 1
DTLS_ICV_SIZE = 20


def calculate_padding(data_size):
    return (BLOCK_SIZE - (data_size % BLOCK_SIZE)) % BLOCK_SIZE


def calculate_dtls_size(data_size):
    pad_len = calculate_padding(data_size + DTLS_ICV_SIZE + DTLS_PAD_LEN_SIZE)
    return (IP_HEADER_SIZE + UDP_HEADER_SIZE + DTLS_HEADER_SIZE + IV_SIZE
            + data_size + DTLS_ICV_SIZE + pad_len + DTLS_PAD_LEN_SIZE), pad_len


def calculate_esp_size(data_size):
    pad_len = calculate_padding(UDP_HEADER_SIZE + data_size + NEXT_HEADER_SIZE + ESP_PAD_LEN_SIZE)
    return (IP_HEADER_SIZE + ESP_HEADER_SIZE + IV_SIZE + UDP_HEADER_SIZE
            + data_size + pad_len + NEXT_HEADER_SIZE + ESP_PAD_LEN_SIZE + ESP_ICV_SIZE), pad_len


tab_esp = [['Rozmiar danych [B]'], ['Rozmiar paddingu [B]'], ['Rozmiar pakietu IP [B]']]
tab_dtls = [['Rozmiar danych [B]'], ['Rozmiar paddingu [B]'], ['Rozmiar pakietu IP [B]']]
for i in [1, 10, 100, 1000]:
    tab_esp[0].append(i)
    tab_dtls[0].append(i)
    ip_size, pad_size = calculate_esp_size(i)
    tab_esp[1].append(pad_size)
    tab_esp[2].append(ip_size)
    ip_size, pad_size = calculate_dtls_size(i)
    tab_dtls[1].append(pad_size)
    tab_dtls[2].append(ip_size)

latex_table = tabulate(tab_esp, tablefmt="latex")
print(latex_table)
latex_table = tabulate(tab_dtls, tablefmt="latex")
print(latex_table)

l = []
for i in range(1000):
    l.append(calculate_dtls_size(i)[0] - calculate_esp_size(i)[0])
print(np.average(l))

esp = []
dtls = []
data_from = 1
data_to = 60
plt.xlim((data_from - 1, data_to + 1))
plt.ylim((0, 200))
for i in range (data_from, data_to + 1):
    esp.append(calculate_esp_size(i)[0])
    dtls.append(calculate_dtls_size(i)[0])
plt.plot(range(data_from, data_to + 1), esp, 'o', label = 'ESP')
plt.plot(range(data_from, data_to + 1), dtls, 'o', label = 'DTLS')
plt.xlabel('Rozmiar danych')
plt.ylabel('Rozmiar pakietu IP')
plt.legend()
plt.grid
plt.savefig('graphs/esp_dtls_size_comp.png', dpi=1000)
# plt.show()
