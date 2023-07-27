import math
import pprint
from random import sample

import numpy as np
import pathlib

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

from tabulate import tabulate


BASE_DIR = pathlib.Path(__file__).parent.parent

dtls_cases = [
    'initial',
    'negotiated',
    'sent 100 bytes',
    'sent 500 bytes',
    'sent 1000 bytes',
]
ipsec_cases = dtls_cases + ['terminated']

DTLS = True
ESP = True


if DTLS:
    cases = dtls_cases
    if ESP:
        FILE = BASE_DIR / 'results/ps_dtls_esp.txt'
        threads = ['isr_stack', 'ppT', 'pmT', 'rtT', 'esp_events', 'idle', 'main', 'ipv6',  'udp',  'netif-esp-wifi']
    else:
        FILE = BASE_DIR / 'results/ps_dtls_stm.txt'
        threads = ['isr_stack', 'main', 'ipv6_esp', 'ipv6', 'udp', 'stm32_eth']
else:
    cases = ipsec_cases
    if ESP:
        FILE = BASE_DIR / 'results/ps_ike_esp.txt'
        threads = ['isr_stack', 'ppT', 'pmT', 'rtT', 'esp_events', 'idle', 'main', 'ipv6_esp', 'ipv6',  'udp',  'netif-esp-wifi']
    else:
        FILE = BASE_DIR / 'results/ps_ike_stm.txt'
        threads = ['isr_stack', 'main', 'ipv6_esp', 'ipv6', 'udp', 'stm32_eth']


def main():
    tab = [['thread'] + cases]
    data = {}
    for t in threads:
        data[t] = []
    for line in open(FILE).readlines():
        stripped = line.strip().replace('|', '').replace('(', '').replace(')', '').replace('bl ', 'bl_')
        parts = stripped.split()
        for t in threads:
            if t in parts:
                data[t].append(int(parts[6]))
    pprint.pprint(data)
    for k, v in data.items():
        tab.append([k] + v)

    latex_table = tabulate(tab, headers="firstrow", tablefmt="latex")
    print(latex_table)

    data = dict(sorted(data.items(), key=lambda item: item[1][-1] - item[1][0]))
    for l in data.values():
        for i in range(len(l)):
            l[i] = l[i]/1000.
    plt.figure(figsize=(10, 10))
    x = list(range(0, len(cases)))
    colors = ['r', 'y', 'g', 'c', 'b', 'm', 'pink', 'peru', 'navy', 'skyblue', 'dimgrey']
    for i, t in enumerate(data.keys()):
        if i == 0:
            plt.fill_between(x, data[t], label=t, fc=colors[i])
        else:
            plt.fill_between(x, [sum(y) for y in zip(*list(data.values())[:i])], [sum(y) for y in zip(*list(data.values())[:i+1])], label=t, fc=colors[i])

    plt.xlabel('Situation')
    plt.ylim(0)
    plt.ylabel('Used memory [kB]')
    plt.title(f'Memory usage during {"DTLS" if DTLS else "IPsec"} usage on {"Node MCU" if ESP else "Nucleo"} board')
    plt.xticks(x, cases, rotation=45)
    plt.legend()
    plt.grid(axis='y')
    plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)

    # Step 5: Display the chart.
    #plt.show()

    plt.savefig(BASE_DIR / f'graphs/ps_{"dtls" if DTLS else "ike"}_{"esp" if ESP else "stm"}', dpi=1000)


if __name__ == '__main__':
    main()
