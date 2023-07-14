import math

import numpy as np
import pathlib

import matplotlib.pyplot as plt

from tabulate import tabulate


BASE_DIR = pathlib.Path(__file__).parent.parent
FILE = BASE_DIR / 'results/size_modules.txt'

headers_d = {
    'DTLS STM': 'dtls-wolfssl-client (STM)',
    'DTLS ESP': 'dtls-wolfssl-client (ESP)',
    'IPSEC STM': 'gnrc-networking-ike (STM)',
    'IPSEC ESP': 'gnrc-networking-ike (ESP)',
    'NOIKE STM': 'gnrc-networking-ike bez IKE (STM)',
    'NOIKE ESP': 'gnrc-networking-ike bez IKE (ESP)',
    'GNRC_NET STM': 'gnrc-networking (STM)',
    'GNRC_NET ESP': 'gnrc-networking (ESP)',
    'DTLS_WOLFSSL STM': 'dtls-wolfssl (STM)',
    'DTLS_WOLFSSL ESP': 'dtls-wolfssl (ESP)',
}


def main():
    tab = [['Case', 'Text', 'Data', 'BSS', 'DEC']]
    text_t = []
    data_t = []
    bss_t = []
    names_t = []
    lines = open(FILE).readlines()
    for i in range(math.ceil(len(lines) / 5)):
        name = lines[i * 5].replace(':', '').strip()
        sizes = [int(x) for x in lines[i * 5 + 2].split()[:4]]
        text_t.append(sizes[1]/1000)
        data_t.append(sizes[2]/1000)
        bss_t.append(sizes[3]/1000)
        names_t.append(name)
        tab.append([headers_d[name], *sizes])
    latex_table = tabulate(tab, headers="firstrow", tablefmt="latex")
    print(latex_table)


    # Calculate the positions of the bars on the x-axis
    categories = ['Text', 'Data', 'BSS']
    bar_positions = range(len(tab) - 1)

    # Create the figure and axis objects
    fig, ax = plt.subplots()

    # Plot the stacked bars
    ax.bar(bar_positions, bss_t, label='BSS')
    ax.bar(bar_positions, data_t, bottom=bss_t, label='Data')
    ax.bar(bar_positions, text_t, bottom=[i + j for i, j in zip(bss_t, data_t)], label='Text')

    # Set the x-axis labels
    ax.set_xticks(bar_positions)
    #ax.set_xticklabels([headers_d[n] for n in names_t], rotation=90)
    ax.set_xticklabels(names_t, rotation=90)

    # Add a legend
    ax.legend()

    # Add labels to the y-axis and title to the chart
    ax.set_ylabel('Size [kB]')
    ax.set_title('Binary file sizes')

    # Display the chart
    plt.subplots_adjust(left=0.1, bottom=0.4, right=0.9, top=0.9)
    #plt.show()
    plt.savefig(BASE_DIR / f'graphs/module_sizes', dpi=1000)


if __name__ == '__main__':
    main()
