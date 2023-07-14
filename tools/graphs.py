import csv
import pathlib

import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = pathlib.Path(__file__).parent.parent
FILE_UDP = BASE_DIR / 'results/benchmark_server_UDPServer_enp0s31f6_2023_05_14_17_22.csv'
FILE_ESP = BASE_DIR / 'results/benchmark_server_UDPServer_enp0s31f6_2023_05_13_17_46.csv'
FILE_DTLS = BASE_DIR / 'results/benchmark_server_DTLSServer_enp0s31f6_2023_05_14_12_59.csv'

# FILE_UDP = BASE_DIR / 'results/benchmark_server_UDPServer_wlp4s0_2023_05_20_23_23.csv'
# FILE_ESP = BASE_DIR / 'results/benchmark_server_UDPServer_wlp4s0_2023_05_20_22_10.csv'
# FILE_DTLS = BASE_DIR / 'results/benchmark_server_DTLSServerWolfSSL_wlp4s0_2023_05_21_00_27.csv'


def get_buckets(x: list, y: list, n: int):
    maxx = max(x)
    minx = min(x)
    bucket_width = (maxx - minx) / n

    # Compute bucket averages and standard deviations
    bucket_averages = []
    bucket_stddevs = []
    for i in range(n):
        bucket_x = []
        bucket_y = []
        for j in range(len(x)):
            if x[j] >= (minx + i*bucket_width) and x[j] < (minx + (i+1)*bucket_width):
                bucket_x.append(x[j])
                bucket_y.append(y[j])
        if len(bucket_y) > 0:
            bucket_averages.append(np.mean(bucket_y))
            bucket_stddevs.append(np.std(bucket_y))
        else:
            bucket_averages.append(0)
            bucket_stddevs.append(0)
    return bucket_width, bucket_averages, bucket_stddevs


def draw_processing_multi_graph(datas: dict, fig_name):
    for name, data in datas.items():
        x = [r[0] for r in data]
        y = [r[1] for r in data]
        n = 40

        bucket_width, bucket_averages, bucket_stddevs = get_buckets(x, y, n)

        # Plot the data and bucket averages
        #plt.plot(x, y, 'o')
        plt.errorbar((np.arange(n)+0.5)*bucket_width, bucket_averages, yerr=bucket_stddevs, fmt='.', label=name)
    plt.xlim([0, 1400])
    plt.ylim(0, 10)
    plt.xlabel('Payload size (bytes)')
    plt.ylabel('Processing time, bidirectional (ms)')
    plt.grid()
    plt.legend()
    plt.savefig(BASE_DIR / f'graphs/{fig_name}', dpi=1000)
    #plt.show()


def draw_neg_pie_chart(data: dict, fig_name, translations: dict = None):

    # Creating the main pie chart
    def format(d):
        return f'{round(d * sum(data.values())/100000., 3)} ms'
    fig, ax = plt.subplots(figsize=(10, 10))
    patches, texts, _ = ax.pie(data.values(), labels=None, startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}, pctdistance=0.9, autopct=format)

    # Adding title and labels
    ax.set_title('IKE Negotiation time')
    if translations:
        ax.legend(patches, [translations.get(k) for k in data.keys()], loc='best')
    else:
        ax.legend(patches, data.keys(), loc='best')

    # Displaying the plot
    plt.savefig(BASE_DIR / f'graphs/{fig_name}', dpi=1000)


def read_file_data(filename: str):
    data = []
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for idx, row in enumerate(reader):
            data.append([float(row[0]), 1000*float(row[1])])
    return data


if __name__ == '__main__':
    datas = {
        'DTLS': read_file_data(FILE_DTLS),
        'UDP': read_file_data(FILE_UDP),
        'ESP': read_file_data(FILE_ESP),
    }
    draw_processing_multi_graph(datas, 'processing_stm.png')
