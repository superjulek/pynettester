import math
import os
import pprint

import numpy as np
import pathlib

import matplotlib.pyplot as plt

from tabulate import tabulate


BASE_DIR = pathlib.Path(__file__).parent.parent
DIR = BASE_DIR / 'results/'
PREFIX = 'performance'

SIZE = 1300
NUM = 10000

translations = {
    'performance_server_DTLSServerWolfSSL_perform': 'DTLS Nucelo',
    'performance_server_DTLSServerWolfSSL_perform_esp': 'DTLS Node MCU',
    'performance_server_DTLSServerWolfSSL_perform_test': 'ESP(DTLS) Nucleo',
    'performance_server_UDPServer_perform': 'UDP Nucleo',
    'performance_server_UDPServer_perform_esp': 'UDP Node MCU',
    'performance_server_UDPServer_perform_esp_ipsec': 'ESP Node MCU',
    'performance_server_UDPServer_perform_ipsec': 'ESP Nucleo',
}


def main():
    files = [f for f in os.listdir(DIR) if f.startswith(PREFIX)]
    groups = {}
    for f in files:
        case_name = f[:-21]
        if case_name not in groups:
            groups[case_name] = []
        groups[case_name].append(int(open(DIR / f).readline().strip().split(',')[0]))
    pprint.pprint(groups)
    avgs = {}
    for k, v in groups.items():
        speeds = [SIZE * NUM * 2 / (t / 1000000000.) * 8 / 2**20 for t in v]
        avgs[k] = (np.average(speeds), max(speeds) - min(speeds))
    pprint.pprint(avgs)

    tab = [['Case', 'Speed (Mib)', 'max(Speed) - min(Speed) (MiB)']]
    for k, v in avgs.items():
        tab.append([translations[k]] + [f'{x:.3f}' for x in v])
    latex_table = tabulate(tab, headers="firstrow", tablefmt="latex")
    print(latex_table)


if __name__ == '__main__':
    main()
