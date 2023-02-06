import pandas as pd
import passwd
from datetime import datetime as dt
from plotly import express
from email_sender import EmailSender

if __name__ == '__main__':
    # 1. Crie uma nova coluna chamada: “house_age”
	# - Se o valor da coluna “date” for maior que ou igual a 2014-01-01 => “new_house”
	# - Se o valor da coluna “date” for menor que 2014-01-01 => “old_house”
    data = pd.read_csv('/home/leafar/Documents/dev/py/ds/datasets/kc_house_data.csv')
    data['date'] = pd.to_datetime(data['date'])
    data['house_age'] = 'new'
    data.loc[data['date'] < dt(2014, 1, 1), 'house_age'] = 'old'
    # print(data[data['date'] >= dt(2014, 1, 1)])
    # 2. Crie uma nova coluna chamada: “dormitory_type”
	# - Se o valor da coluna “bedrooms” for igual a 1 => ‘studio’
	# - Se o valor da coluna “bedrooms” for igual a 2 => ‘apartment’
	# - Se o valor da coluna “bedrooms” for maior que 2 => ‘house’
    data['dormitory_type'] = 'house'
    data.loc[data['bedrooms'] == 1, 'dormitory_type'] = 'studio'
    data.loc[data['bedrooms'] == 2, 'dormitory_type'] = 'apartment'
    # 3. Crie uma nova coluna chamada: “condition_type”
	# - Se o valor da coluna “condition” for menor ou igual a 2 => ‘bad’
	# - Se o valor da coluna “condition” for igual a 3 ou 4 => ‘regular’
	# - Se o valor da coluna “condition” for igual a 5 => ‘good’
    data['condition_type'] = 'regular'
    data.loc[data['condition'] <= 2, 'condition_type'] = 'bad'
    data.loc[data['condition'] == 5, 'condition_type'] = 'good'
    # 4. Modifique o TIPO da coluna “condition” para STRING
    data['condition'] = data['condition'].astype(str)
    # 5.Delete as colunas: “sqft_living15” e “sqft_lot15”
    data = data.drop(['sqft_living15', 'sqft_lot15'], axis=1)
    # 6. Modifique o TIPO da coluna “yr_built” para DATE
    data['yr_built'] = data['yr_built'].astype(str)      # Cast from int64 to object (str).
    data['yr_built'] = data['yr_built'] + '0101T000000'  # Fill out the other fields.
    data['yr_built'] = pd.to_datetime(data['yr_built'])  # Cast from object (str) to datetime.  
    # 7. Modifique o TIPO da coluna “yr_renovated” para DATE
    data['yr_renovated'] = data['yr_renovated'].astype(str)
    data.loc[data['yr_renovated'] == '0', 'yr_renovated'] = None
    data.loc[data['yr_renovated'] != 'None', 'yr_renovated'] = data[data['yr_renovated'] != 'None']['yr_renovated'] + '0101T000000'
    data['yr_renovated'] = pd.to_datetime(data['yr_renovated'])
    # 8. Qual a data mais antiga de construcao de um imovel?
    oldest_built_year = data.sort_values('yr_built').head(1)['yr_built'].values[0].__str__().split('-')[0]
    answers = []
    answers.append(f'The oldest built year is {oldest_built_year}.')
    # 9. Qual a data mais antiga de renovacao de um imovel?
    oldest_renovation_year = data.sort_values('yr_renovated').head(1)['yr_renovated'].values[0].__str__().split('-')[0]
    answers.append(f'The oldest renovation year is {oldest_renovation_year}.')
    # 10. Quantos imoveis tem 2 andares?
    two_floor_properties = data[data['floors'] == 2].shape[0]
    answers.append(f'There is(are) {two_floor_properties} properties with 2 floors.')
    # 11. Quantos imoveis estao com a condicao igual a “regular”?
    regular_properties = data[data['condition_type'] == 'regular'].shape[0]
    answers.append(f'There is(are) {regular_properties} regular properties.')
    # 12. Quantos imoveis estao com a condicao igual a “bad” e possuem “vista para agua”?
    water_view = data[data['view'] == 1]
    bad_properties = water_view[water_view['condition_type'] == 'bad'].shape[0]
    answers.append(f'There is(are) {bad_properties} bad properties with water view.')
    # 13. Quantos imoveis estao com a condicao igual a “good” e sao “new_house”
    new_houses = data[data['house_age'] == 'new']
    good_properties = new_houses[new_houses['condition_type'] == 'good'].shape[0]
    answers.append(f'There is(are) {good_properties} new good properties.')
    # 14. Qual o valor do imovel mais caro do tipo “studio”
    most_expensive_studio = data[data['dormitory_type'] == 'studio'].sort_values('price', ascending=False).head(1)['price'].values[0]
    answers.append(f'The most expensive studio property is worth ${most_expensive_studio}.')
    # 15. Quantos imoveis do tipo “apartment” foram reformados em 2015?
    reformed_2015 = data[data['yr_renovated'] == '2015-01-01']
    apartments = reformed_2015[reformed_2015['dormitory_type'] == 'apartment'].shape[0]
    answers.append(f'There was(were) {apartments} apartment(s) reformed in 2015.')
    # 16. Qual o maior numero de quartos que um imovel do tipo “house” possui?
    houses = data[data['dormitory_type'] == 'house']
    bedrooms = houses.sort_values('bedrooms', ascending=False).head(1)['bedrooms'].values[0]
    answers.append(f'The largest quantity of bedrooms a house has is {bedrooms}.')
    # 17. Quantos imoveis “new_house” foram reformados no ano de 2014?
    reformed_2014 = data[data['yr_renovated'] == '2014-01-01']
    new_houses = reformed_2014[reformed_2014['house_age'] == 'new'].shape[0]
    answers.append(f'There was(were) renovated {new_houses} new houses in 2014.')
    # 18. Selecione as colunas: “id”, “date”, “price”, “floors”, “zipcode” pelo metodo:
	# 18.1 – Direto pelo nome das colunas
    # result = data[['id', 'date', 'price', 'floors', 'zipcode']]
	# 18.2 – Pelos indices
    # result = data.iloc[:, [0, 1, 2, 7, 16]]
	# 18.3 – Pelos indices das linhas e o nome das colunas
    # result = data.loc[:, ['id', 'date', 'price', 'floors', 'zipcode']]
	# 18.4 – Indices booleanos
    # result = data.loc[:, [True, True, True, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False]]
    # print(result)
    # 19. Salve um arquivo .csv com somente as colunas do item 18
    # report = data[['id', 'date', 'price', 'floors', 'zipcode']]
    # report.to_csv('/home/leafar/Documents/dev/py/ds/datasets/report2.csv', index=False)
    # 20. Modifique a cor dos pontos no mapa de “pink” para “verde-escuro”
    # map_data = data[['id', 'lat', 'long', 'price']]
    # map = express.scatter_mapbox(
    #     map_data, lat='lat', 
    #     lon='long', hover_name='id', 
    #     hover_data=['price'], color_discrete_sequence=['darkgreen'], 
    #     zoom=10, height=300
    # )
    # map.update_layout(mapbox_style='open-street-map')
    # map.update_layout(
    #     height=600, 
    #     margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
    # )
    # map.show()
    # map.write_html('/home/leafar/Documents/dev/py/ds/datasets/green_property_map.html')
    # final_answer = answers[0]
    # for answer in answers[1:]:
    #     final_answer += '\n' + answer
    # es = EmailSender(
    #     author='Rafael Guimarães',
    #     sender_email='rafaelfonseca1020@gmail.com',
    #     password=passwd.EMAIL1,
    #     subject='Respostas para Perguntas',
    #     body=final_answer
    # )
    # es.add_target('rafael.fonseca@estudante.ifgoiano.edu.br')
    # es.add_attachment('/home/leafar/Documents/dev/py/ds/datasets/green_property_map.html')
    # es.add_attachment('/home/leafar/Documents/dev/py/ds/datasets/report2.csv')
    # es.send()
    