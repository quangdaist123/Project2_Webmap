import json
import pandas as pd
from difflib import get_close_matches


def correct_data(dataset, path):

    with open(f'{path}', 'r', encoding='utf-8-sig') as f:
        root_data = json.loads(f.read())
    csv_provinces = set(x for x in dataset['admin_name'])
    json_provinces = set(x['properties']['name'] for x in root_data['features'])
    incorrect_names = list(csv_provinces - json_provinces)

    correct_names = [get_close_matches(name, json_provinces, n=1)[0] for name in incorrect_names]
    corrections = dict(zip(incorrect_names, correct_names))
    for index, city_name in enumerate(dataset['admin_name']):
        if city_name in corrections.keys():
            dataset.at[index, 'admin_name'] = corrections[city_name]


if __name__ == '__main__':

    dataset = pd.read_csv('./data/vn.csv')
    with open('./data/vn.json', 'r', encoding='utf-8-sig') as f:
        data = json.loads(f.read())
    dataset = pd.read_csv('./data/mat-do-dan-so-vn.csv')
    path = './data/vn.json'
    correct_data(dataset, path=path)