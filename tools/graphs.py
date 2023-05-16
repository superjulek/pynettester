import csv

import matplotlib.pyplot as plt
import numpy as np


FILE_UDP = 'results/benchmark_server_UDPServer_enp0s31f6_2023_05_14_17_22.csv'
FILE_ESP = 'results/benchmark_server_UDPServer_enp0s31f6_2023_05_13_17_46.csv'
FILE_DTLS = 'results/benchmark_server_DTLSServer_enp0s31f6_2023_05_14_12_59.csv'


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


def draw_processing_multi_graph(datas: dict):
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
    plt.show()






def draw_neg_pie_chart(data: dict):

    # Creating the main pie chart
    def format(d):
        return f'{round(d * sum(data.values())/100000., 3)} ms'
    fig, ax = plt.subplots(figsize=(8, 8))
    patches, texts, _ = ax.pie(data.values(), labels=None, startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}, autopct=format)


    # Adding title and labels
    ax.set_title('IKE Negotiation time')
    ax.legend(patches, data.keys(), loc='best')

    # Displaying the plot
    plt.show()


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
    draw_processing_multi_graph(datas)
