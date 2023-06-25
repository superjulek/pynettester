import numpy as np

from graphs import draw_neg_pie_chart

from tabulate import tabulate


FILE = 'results/dtls_neg_esp.txt'
FILE = 'results/dtls_neg_stm.txt'

def parse_dtls_neg_text(text: str):
    headers = [
        'Client Hello 1',
        'Hello Verify Request',
        'Client Hello 2',
        'Server Hello, Certificate',
        'Server Key Exchange, Server Hello Done',
        'Client Key Exchange',
        'Change Cipher Spec, Encrypted Handshake Message 1',
        'Change Cipher Spec, Encrypted Handshake Message 2',
        'total'
    ]
    values = {}
    for h in headers:
        values[h] = [float(l.replace(h, '').strip()) for l in text.splitlines() if h in l]
    for i, h in enumerate(headers[-2:0:-1]):
        v2 = values[h]
        v1 = list(values.values())[-3 - i]
        new_v = [vv2 - vv1 for vv1, vv2 in zip(v1, v2)]
        values[h] = new_v
    values['total'] = [v/1000000 for v in values['total']]
    return values


def plot_neg(text: str):
    v = parse_dtls_neg_text(text)
    v = {key: (np.average(value), np.std(value)) for key, value in v.items()}
    print(v)
    tab = [['Step', 'Duration [ms]', 'Deviation [ms]']]
    for k, (avg, std) in v.items():
        tab.append([k, 1000 * avg, 1000 * std])
    latex_table = tabulate(tab, headers="firstrow", tablefmt="latex")
    print(latex_table)
    return
    t = v['generate_key']
    v['init context - generate key'] = v.pop('init context') - t
    t = v['get_secret']
    v['parse INIT - get_secret'] = v.pop('parse INIT') - t
    v.pop('total established')
    bigv = {
        'generate_key': v['generate_key'],
        'get_secret': v['get_secret'],
        'other': sum(y for x, y in v.items() if x not in ['get_secret', 'generate_key'])
    }
    normalv = {
        'receive AUTH': v['receive AUTH'],
        'receive INIT': v['receive INIT'],
        'other': sum(y for x, y in v.items() if x not in ['receive AUTH', 'receive INIT'] + list(bigv.keys()))
    }
    print(normalv)
    smallv = {x: y for x, y in v.items() if x not in list(bigv.keys()) + list(normalv.keys())}
    draw_neg_pie_chart(bigv)
    draw_neg_pie_chart(normalv)
    draw_neg_pie_chart(smallv)

if __name__ == '__main__':
    with open(FILE, 'r') as negfile:
        plot_neg(negfile.read())
