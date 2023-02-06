import pandas as pd

def print_header(data: dict):
    data_keys_it = iter(data.keys())
    first_key = data_keys_it.__next__()
    len_largest_pair = len(str(first_key)) + len(str(data[first_key]))
    data_items_it = iter(data.items())
    data_items_it.__next__()
    for key, value in data_items_it:
        pair_len = len(str(key)) + len(str(value))
        if pair_len > len_largest_pair:
            len_largest_pair = pair_len
    bar = '-' * (len_largest_pair + 1) * 2
    print(bar)
    for key, value in data.items():
        print('|', (str(key) + "=" + str(value)).center(len_largest_pair * 2) , '|',sep='')
    print(bar)
    
    
if __name__ == '__main__':
    dataset = pd.read_csv('/home/leafar/Documents/dev/py/ds/datasets/kc_house_data.csv')
    # Some basic commands.
    # print(dataset.head())
    # print(dataset.tail())
    # print(dataset.dtypes)
    # print('Lines=', dataset.shape[0], ', columns=', dataset.shape[1], sep='')
    # print(dataset.columns) 
    # print(dataset.sort_values('price'))
    # print(dataset.sort_values('price', ascending=False))
    # print(dataset[['id', 'price']].sort_values('price'))
    # print(dataset[['id', 'price']].sort_values('price', ascending=False))
    # Answering some questions.
    questions_and_answers = dict()
    # Quantas casas estão disponíveis para compra?
    questions_and_answers['Quantas casas estão disponíveis para compra?'] = dataset.shape[0]
    # Quantos atributos as casas possuem?
    questions_and_answers['Quantos atributos as casas possuem?'] = dataset.shape[1]
    # Quais são os atributos das casas?
    columns = ''
    len_dataset_columns = len(dataset.columns)
    for i in range(len_dataset_columns):
        columns += dataset.columns[i]
        if i < len_dataset_columns - 1:
            columns += ", "
    questions_and_answers['Quais são os atributos das casas?'] = columns
    # Qual a casa mais cara?
    questions_and_answers['Qual a casa mais cara?'] = f'id={dataset.at[7252, "id"]} e preco={dataset.at[7252, "price"]}'
    # Qual a casa com maior número de quartos?
    many_bedrooms_house = dataset.sort_values('bedrooms', ascending=False).head(1)[['id', 'bedrooms']]
    questions_and_answers['Qual a casa com maior número de quartos?'] = f'id={many_bedrooms_house["id"].values[0]} e quantidade de quartos={many_bedrooms_house["bedrooms"].values[0]}'
    # Qual a soma total de quartos?
    questions_and_answers['Qual a soma total de quartos?'] = dataset[['bedrooms']].sum()[0]
    # Quantas casas possuem 2 banheiros?
    questions_and_answers['Quantas casas possuem 2 banheiros?'] = dataset[dataset['bathrooms'] == 2].shape[0]
    # Qual o preço médio de todas as casas?
    questions_and_answers['Qual o preço médio de todas as casas?'] = round(dataset['price'].sum() / dataset.shape[0], 2)
    # Qual o preço médio de todas as casas com 2 banheiros?
    questions_and_answers['Qual o preço médio de todas as casas com 2 banheiros?'] = round(dataset[dataset['bathrooms'] == 2]['price'].sum() / dataset[dataset['bedrooms'] == 2].shape[0], 2)
    # Qual o preço mínimo entre as casas com 3 banheiros?
    questions_and_answers['Qual o preço mínimo entre as casas com 3 banheiros?'] = round(dataset[dataset['bathrooms'] == 3].sort_values('price').head(1)['price'].values[0], 2)
    # Quantas casas possuem mais de 300 metros quadrados de área?
    sqft_to_sqmt = dataset['sqft_lot'] * 0.09290304
    questions_and_answers['Quantas casas possuem mais de 300 metros quadrados de área?'] = dataset[sqft_to_sqmt > 300].shape[0]
    print('-' * 150)
    for key, value in questions_and_answers.items():
        print(f'{key} {value}')
        print('-' * 150)
        