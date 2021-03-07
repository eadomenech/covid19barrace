import json

import pandas as pd
from utils.utils import date_range


def build_deceased_data(date_end, intermediate_days=1):
    deceased_full_result = {}
    deceased_full_result['date'] = []
    deceased_full_result['province'] = []
    deceased_full_result['deceased'] = []
    deceased_full_result['accumulated_deceased'] = []

    deceased_result = {}
    deceased_result['date'] = []
    deceased_result['province'] = []
    deceased_result['deceased'] = []
    deceased_result['accumulated_deceased'] = []

    provinces = [
        'Pinar del Río', 'Artemisa', 'La Habana', 'Mayabeque', 'Matanzas',
        'Cienfuegos', 'Villa Clara', 'Sancti Spíritus', 'Ciego de Ávila',
        'Camagüey', 'Las Tunas', 'Holguín', 'Granma', 'Santiago de Cuba',
        'Guantánamo', 'Isla de la Juventud'
    ]

    accumulated_deceased = {}
    for p in provinces:
        accumulated_deceased[p] = 0

    with open('data/covid19-fallecidos.json', 'r') as f:
        distros_dict = json.load(f)

    for caso in distros_dict['casos']['dias']:
        c = distros_dict['casos']['dias'][caso]
        if 'fallecidos' in c:
            for p in provinces:
                deceased = 0
                for d in c['fallecidos']:
                    if d['provincia_detección'] == p:
                        deceased += 1
                accumulated_deceased[p] += deceased
                s = c['fecha'].split('/')
                deceased_result['date'].append("-".join(s))
                deceased_result['province'].append(p)
                deceased_result['deceased'].append(deceased)
                deceased_result['accumulated_deceased'].append(
                    accumulated_deceased[p])

    def datos(dat, pro):
        for i in range(len(deceased_result['date'])):
            if (deceased_result['date'][i] == dat) and (deceased_result['province'][i] == pro):
                return [
                    dat, pro, deceased_result['deceased'][i],
                    deceased_result['accumulated_deceased'][i]]
        return None

    range_date = date_range('2020-03-18', date_end)
    for ran in range_date:
        for pro in provinces:
            d = datos(ran, pro)
            if d == None:
                deceased_full_result['date'].append(ran)
                deceased_full_result['province'].append(pro)
                deceased_full_result['deceased'].append(0)
                deceased_full_result['accumulated_deceased'].append(
                    accumulated_deceased[pro])
            else:
                deceased_full_result['date'].append(d[0])
                deceased_full_result['province'].append(d[1])
                deceased_full_result['deceased'].append(d[2])
                deceased_full_result['accumulated_deceased'].append(d[3])
                accumulated_deceased[pro] = d[3]

    df = pd.DataFrame(
        deceased_full_result,
        columns= [
            'date', 'province', 'deceased', 'accumulated_deceased'])

    df = df[df['date'].isin(
        date_range('2020-03-13', date_end, intermediate_days))]

    df.to_csv(
        f"data/province_deceased_{intermediate_days}.csv",
        index = False, header=True)
