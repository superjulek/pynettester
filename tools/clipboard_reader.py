import numpy as np

from graphs import draw_neg_pie_chart


FILE = 'results/neg_1.csv'

def parse_ike_neg_text(text: str):
    headers = [
       'total established',
       'reset context',
       'init context',
       'build INIT',
       'send INIT',
       'receive INIT',
       'parse INIT',
       'build AUTH',
       'send AUTH',
       'receive AUTH',
       'parse AUTH',
       'generate_key',
       'get_secret'
    ]
    values = {}
    for h in headers:
        values[h] = [l.strip().split()[0] for l in text.splitlines() if h in l]
    return values


def plot_neg(text: str):
    v = parse_ike_neg_text(text)
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
    draw_neg_pie_chart(bigv)
    draw_neg_pie_chart(normalv)
    draw_neg_pie_chart(smallv)

if __name__ == '__main__':
    with open(FILE, 'r') as negfile:
        plot_neg(negfile.read())
