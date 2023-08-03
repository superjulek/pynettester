import math
import os
import pprint

import numpy as np
import pathlib

import matplotlib.pyplot as plt

from tabulate import tabulate


BASE_DIR = pathlib.Path(__file__).parent.parent
FILE = BASE_DIR / 'results/power.txt'

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
    data = {}
    for l in open(FILE).readlines():
        split = l.replace(',', '').split()
        name = f'{split[0]} {split[1]}'
        energy = float(split[2]) * 60 * 60  # Wh -> J
        hours, minutes, seconds = split[4].split(':')
        duration = int(seconds) + 60 * (int(minutes) + 60 * int(hours))
        packets = int(split[5])
        packet_size = int(split[7])
        power = energy / duration
        data[name] = {
            'energy': energy,
            'duration': duration,
            'packets': packets,
            'packets_size': packet_size,
            'power': power * 1000,  # [mW]
            'speed': packets * packet_size * 2 * 8 / duration / 2**20,
        }
    for k, vals in data.items():
        idle = data[f'{k.split()[0]} idle']
        extra_power = vals['power'] - idle['power']
        vals['extra_power'] = extra_power
        extra_energy = extra_power * duration
        energy_per_packet = extra_energy / (vals['packets'] or math.inf)
        energy_per_data_byte = extra_energy / ((vals['packets'] * vals['packets_size']) or math.inf)
        vals['energy_per_packet'] = energy_per_packet  # [mJ]
        vals['energy_per_data_byte'] = energy_per_data_byte * 10**3  # [mJ/kB]
    for k, v in data.items():
        for kk, vv in v.items():
            if isinstance(vv, float):
                v[kk] = float('{:.3g}'.format(vv))
    pprint.pprint(data)

    tab = [['Case', 'time [s]', 'energy [J]', 'power [mW]', 'net power [mW]', 'net energy per packet [mJ]', 'net energy per byte [mJ/kB]']]
    for k, v in data.items():
        tab.append([k, v['duration'], v['energy'], v['power'], v['extra_power'], v['energy_per_packet'], v['energy_per_data_byte']])
    pprint.pprint(tab)
    latex_table = tabulate(tab, headers="firstrow", tablefmt="latex")
    print(latex_table)
    return


if __name__ == '__main__':
    main()
