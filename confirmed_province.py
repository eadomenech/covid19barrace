import json

import pandas as pd
from utils import date_range


def build_confirmed_data(date_end, intermediate_days=1):
    confirmed_full_result = {}
    confirmed_full_result['date'] = []
    confirmed_full_result['province'] = []
    confirmed_full_result['confirmed'] = []
    confirmed_full_result['accumulated_confirmed'] = []

    confirmed_result = {}
    confirmed_result['date'] = []
    confirmed_result['province'] = []
    confirmed_result['confirmed'] = []
    confirmed_result['accumulated_confirmed'] = []

    provinces = [
        'Pinar del Río', 'Artemisa', 'La Habana', 'Mayabeque', 'Matanzas',
        'Cienfuegos', 'Villa Clara', 'Sancti Spíritus', 'Ciego de Ávila',
        'Camagüey', 'Las Tunas', 'Holguín', 'Granma', 'Santiago de Cuba',
        'Guantánamo', 'Isla de la Juventud'
    ]

    accumulated_confirmed = {}
    for p in provinces:
        accumulated_confirmed[p] = 0

    with open('data/covid19-cuba.json', 'r') as f:
        distros_dict = json.load(f)

    for caso in distros_dict['casos']['dias']:
        c = distros_dict['casos']['dias'][caso]
        if 'diagnosticados' in c:
            for p in provinces:
                confirmed = 0
                for d in c['diagnosticados']:
                    if d['provincia_detección'] == p:
                        confirmed += 1
                accumulated_confirmed[p] += confirmed
                s = c['fecha'].split('/')
                confirmed_result['date'].append("-".join(s))
                confirmed_result['province'].append(p)
                confirmed_result['confirmed'].append(confirmed)
                confirmed_result['accumulated_confirmed'].append(
                    accumulated_confirmed[p])

    def datos(dat, pro):
        for i in range(len(confirmed_result['date'])):
            if (confirmed_result['date'][i] == dat) and (confirmed_result['province'][i] == pro):
                return [
                    dat, pro, confirmed_result['confirmed'][i],
                    confirmed_result['accumulated_confirmed'][i]]
        return None

    range_date = date_range('2020-03-11', date_end)
    for ran in range_date:
        for pro in provinces:
            d = datos(ran, pro)
            if d == None:
                confirmed_full_result['date'].append(ran)
                confirmed_full_result['province'].append(pro)
                confirmed_full_result['confirmed'].append(0)
                confirmed_full_result['accumulated_confirmed'].append(
                    accumulated_confirmed[pro])
            else:
                confirmed_full_result['date'].append(d[0])
                confirmed_full_result['province'].append(d[1])
                confirmed_full_result['confirmed'].append(d[2])
                confirmed_full_result[
                    'accumulated_confirmed'].append(d[3])
                accumulated_confirmed[pro] = d[3]

    df = pd.DataFrame(
        confirmed_full_result,
        columns= [
            'date', 'province', 'confirmed', 'accumulated_confirmed'])

    df = df[df['date'].isin(
        date_range('2020-03-11', date_end, intermediate_days))]

    df.to_csv(
        f"data/province_confirmed_{intermediate_days}.csv",
        index = False, header=True)
