import csv
import inspect
import datetime
from pathlib import Path

from server import Server


class ResList(list):
    ...


basepath = Path(__file__).parent / '..' / 'results'
def save_results(res: list, server: Server, extra_info: str):
    if (hasattr(res, 'filename')):
        filename = res.filename
    else:
        filename = f'{inspect.stack()[1].function}_{server.__class__.__name__}_{extra_info}_'\
                f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")}.csv'
    with open(basepath / filename, 'a') as csv_file:
        writer = csv.writer(csv_file)
        for l in res:
            writer.writerow(l)
    del res[:]
    setattr(res, 'filename', filename)
