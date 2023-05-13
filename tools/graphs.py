import csv

import matplotlib.pyplot as plt
import numpy as np


FILE = 'results/benchmark_server_UDPServer_enp0s31f6_2023_05_13_17_46.csv'


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


def draw_processing_graph(data: list):
    x = [r[0] for r in data]
    y = [r[1] for r in data]
    n = 20

    bucket_width, bucket_averages, bucket_stddevs = get_buckets(x, y, n)

    # Plot the data and bucket averages
    #plt.plot(x, y, 'o')
    plt.errorbar((np.arange(n)+0.5)*bucket_width, bucket_averages, yerr=bucket_stddevs, fmt='o')
    plt.xlim([0, max(x)])
    plt.xlabel('X value')
    plt.ylabel('Y value')
    plt.show()


def draw_neg_pie_chart(data: dict):

    # Creating the main pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(data.values(), labels=data.keys(), startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})


    # Adding title and labels
    ax.set_title('Compound Pie Chart')
    ax.legend(loc='best')

    # Displaying the plot
    plt.show()



if __name__ == '__main__':
    data = []
    with open(FILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for idx, row in enumerate(reader):
            data.append([float(row[0]), float(row[1])])
            if idx > 1300 * 25:
                break
    draw_processing_graph(data)
