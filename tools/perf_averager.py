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

    # tab = [['Case', 'Text', 'Data', 'BSS', 'DEC']]
    # text_t = []
    # data_t = []
    # bss_t = []
    # names_t = []
    # lines = open(FILE).readlines()
    # for i in range(math.ceil(len(lines) / 5)):
    #     name = lines[i * 5].replace(':', '').strip()
    #     sizes = [int(x) for x in lines[i * 5 + 2].split()[:4]]
    #     text_t.append(sizes[1]/1000)
    #     data_t.append(sizes[2]/1000)
    #     bss_t.append(sizes[3]/1000)
    #     names_t.append(name)
    #     tab.append([headers_d[name], *sizes])
    # latex_table = tabulate(tab, headers="firstrow", tablefmt="latex")
    # print(latex_table)


    # # Calculate the positions of the bars on the x-axis
    # categories = ['Text', 'Data', 'BSS']
    # bar_positions = range(len(tab) - 1)

    # # Create the figure and axis objects
    # fig, ax = plt.subplots()

    # # Plot the stacked bars
    # ax.bar(bar_positions, bss_t, label='BSS')
    # ax.bar(bar_positions, data_t, bottom=bss_t, label='Data')
    # ax.bar(bar_positions, text_t, bottom=[i + j for i, j in zip(bss_t, data_t)], label='Text')

    # # Set the x-axis labels
    # ax.set_xticks(bar_positions)
    # #ax.set_xticklabels([headers_d[n] for n in names_t], rotation=90)
    # ax.set_xticklabels(names_t, rotation=90)

    # # Add a legend
    # ax.legend()

    # # Add labels to the y-axis and title to the chart
    # ax.set_ylabel('Size [kB]')
    # ax.set_title('Binary file sizes')

    # # Display the chart
    # plt.subplots_adjust(left=0.1, bottom=0.4, right=0.9, top=0.9)
    # #plt.show()
    # plt.savefig(BASE_DIR / f'graphs/module_sizes', dpi=1000)


if __name__ == '__main__':
    main()
