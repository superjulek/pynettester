import numpy as np
import pathlib

from graphs import draw_neg_pie_chart

from tabulate import tabulate


BASE_DIR = pathlib.Path(__file__).parent.parent
FILE = BASE_DIR / 'results/neg_esp.txt'
#FILE = BASE_DIR / 'results/neg_stm.txt'

headers_d = {
    'total established': 'Total negotiation',
    'reset context': 'Resetting context',
    'init context': 'Initializing context',
    'build INIT': 'Building INIT message',
    'send INIT': 'Sending INIT message',
    'receive INIT': 'Receiving INIT message',
    'parse INIT': 'Parsing INIT message',
    'build AUTH': 'Building AUTH message',
    'send AUTH': 'Sending AUTH message',
    'receive AUTH': 'Receiving AUTH message',
    'parse AUTH': 'Parsing AUTH message',
    'generate_key': 'Generating DH key',
    'get_secret': 'Computing DH shared secret',
}


def parse_ike_neg_text(text: str):
    headers = headers_d.keys()
    values = {}
    for h in headers:
        values[h] = [l.strip().split()[0] for l in text.splitlines() if h in l]
    return values


def plot_neg(text: str):
    v = parse_ike_neg_text(text)
    org_v = v
    v = {key: np.average([float(x) for x in value]) for key, value in v.items()}
    print(v)
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

    tab = [['Step', 'Duration [ms]', 'Deviation [ms]']]
    for k, vals in org_v.items():
        fvals = [float(x) for x in vals]
        tab.append([k, np.average(fvals) / 1000, np.std(fvals) / 1000])
    latex_table = tabulate(tab, headers="firstrow", tablefmt="latex")
    print(latex_table)
    headers_d['other'] = 'Rest of processing'
    headers_d['init context - generate key'] = 'Initializing context - generating DH key'
    headers_d['parse INIT - get_secret'] = 'Parsing INIT message - computing DH shared secret'
    draw_neg_pie_chart(bigv, 'nego_ike_esp_1.png', headers_d)
    draw_neg_pie_chart(normalv, 'nego_ike_esp_2.png', headers_d)
    draw_neg_pie_chart(smallv, 'nego_ike_esp_3.png', headers_d)


if __name__ == '__main__':
    with open(FILE, 'r') as negfile:
        plot_neg(negfile.read())
