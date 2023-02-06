import pandas as pd
import passwd
from plotly import express as px
from email_senderimport EmailSender
# import numpy as nm

if __name__ == '__main__':
    data = pd.read_csv('/home/leafar/Documents/dev/py/ds/datasets/kc_house_data.csv')
    ### Some basic convertions.
    # data['bedrooms'] = data['bedrooms'].astype(nm.float64)
    # data['price'] = data['price'].astype(nm.int64)
    # print(data.dtypes)
    # Qual a data do imóvel mais antigo no portfólio?
    data['date'] = pd.to_datetime(data['date'])  # Convert 'date' values from 'object' to 'datetime'.
    oldest_house = data.sort_values('date').head(1)[['id', 'date']]
    question1 = f'O imóvel mais antigo é o de id={oldest_house["id"].values[0]} e data={oldest_house["date"].values[0]}.'
    # Quantos imóveis possuem o número máximo de andares?
    max_floors = data.sort_values('floors', ascending=False).head(1)['floors'].values[0]
    question2 = f'{data[data["floors"] == max_floors].shape[0]} imóvel(is) possui(em) a quantidade máxima de andares, que é {max_floors}.'
    # Criar uma classificação para os imóveis, separando-os em baixo e alto padrão, de acordo com o preço:
    #   -> Acima de $540,000.00 é alto padrão;
    #   -> Abaixo é baixo padrão.
    # New column: 'standard' with possible values 'high' and 'low'.
    data['standard'] = 'low'
    data.loc[data['price'] > 540000, 'standard'] = 'high'
    ### Select data.
    ## By columns;
    ## By index of rows and columns (iloc);
    ## by index of rows and name of the columns (loc);
    ## And by index of rows and boolean values.
    # print(data[['id', 'price', 'date']])
    # print(data.iloc[0:10, 0:3])
    # print(data.loc[0:10, ['price', 'id']])
    # print(data.loc[0:10, [True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]])
    ### Create new columns.
    # data['standard'] = 'low'  # Create new columns with 'low' as value to all tuples.
    ### Delete some columns.
    # data = data.drop('id', axis=1)  # axis=1 means columns.
    # Relatório com as seguintes informações: id do imóvel, data, quartos, área do terreno, preço e a classificação.
    # As tuplas devem ser ordenadas pela coluna preço.
    report = data[['id', 'date', 'bedrooms', 'sqft_lot', 'price', 'standard']].sort_values('price')
    # report.to_csv('datasets/relatorio.csv', index=False)
    # Um mapa indicando onde as casas estão situadas geograficamente. 
    # map_data = data[['id', 'lat', 'long', 'price']]
    # map = px.scatter_mapbox(
    #     map_data, lat='lat', 
    #     lon='long', hover_name='id', 
    #     hover_data=['price'], color_discrete_sequence=['fuchsia'], 
    #     zoom=10, height=300
    # )
    # map.update_layout(mapbox_style='open-street-map')
    # map.update_layout(
    #     height=600, 
    #     margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
    # )
    # map.show()
    # map.write_html('/home/leafar/Documents/dev/py/ds/datasets/mapa_casas.html')
    # Entregar documentos via e-mail e dois anexos.
    # -> E-mail: texto com perguntas e respostas.
    # -> Anexos: um arquivo csv (relatório) e um mapa em html.
    # es = EmailSender(
    #     author='Rafael Guimarães',
    #     sender_email='rafaelfonseca1020@gmail.com',
    #     password=passwd.EMAIL1,
    #     subject='Respostas para Perguntas',
    #     body=f'{question1}\n{question2}'
    # )
    # es.add_target('rafael.fonseca@estudante.ifgoiano.edu.br')
    # es.add_attachment('/home/leafar/Documents/dev/py/ds/datasets/relatorio.csv')
    # es.add_attachment('/home/leafar/Documents/dev/py/ds/datasets/mapa_casas.html')
    # es.send()
 