import pandas as pd
from matplotlib import pyplot, gridspec
from plotly import express as exp
import streamlit as slit


# Organize 4th class code in functions.


def organize_4th_class_code():
    def load_data():
        return pd.read_csv('datasets/kc_house_data.csv')

    def properties_per_bedrooms(data):
        sorted_data = data.sort_values('bedrooms')
        minimum = sorted_data.head(1)['bedrooms'].values[0]
        maximum = sorted_data.tail(1)['bedrooms'].values[0]
        table = dict()
        for i in range(minimum, maximum + 1):
            table[str(i)] = sorted_data[sorted_data['bedrooms'] == i].shape[0]
        print('-' * 30)
        print(f'{"Bedrooms":<15}Properties')
        print('-' * 30)
        for key, value in table.items():
            if value == 0:
                continue
            print(f'{key:<15}{value}')
        print('-' * 30)

    def properties_per_bedrooms_groupby(data):
        df_grouped = data[['id', 'bedrooms']].groupby('bedrooms')
        print('-' * 30)
        print(f'{"Bedrooms":<15}Properties')
        print('-' * 30)
        for bedrooms, frame in df_grouped:
            print(f'{bedrooms:<15}{frame.shape[0]}')
        print('-' * 30)

    def properties_per_built_year(data):
        df_grouped = data[['id', 'yr_built']].groupby('yr_built')
        print('-' * 30)
        print(f'{"Build year":<15}Properties')
        print('-' * 30)
        for build_year, frame in df_grouped:
            print(f'{build_year:<15}{frame.shape[0]}')
        print('-' * 30)

    def least_bedroom_number_per_built_year(data):
        df = data[['bedrooms', 'yr_built']].groupby('yr_built')
        print('-' * 30)
        print(f'{"Build year":<15}Bedrooms')
        print('-' * 30)
        for build_year, frame in df:
            print(f'{build_year:<15}{frame.min().values[0]}')
        print('-' * 30)

    def highest_price_per_bedroom_number(data):
        df = data[['price', 'bedrooms']].groupby('bedrooms')
        print('-' * 30)
        print(f'{"Bedrooms":<15}Price')
        print('-' * 30)
        for bedrooms, frame in df:
            print(f'{bedrooms:<15}{frame.max().values[0]}')
        print('-' * 30)

    def sum_prices_per_bedroom_number(data):
        df = data[['price', 'bedrooms']].groupby('bedrooms')
        print('-' * 30)
        print(f'{"Bedrooms":<15}Sum of prices')
        print('-' * 30)
        for bedrooms, frame in df:
            print(f'{bedrooms:<15}{frame.sum().values[0]}')
        print('-' * 30)

    def sum_prices_per_bedroom_bathroom_number(data):
        df = data[['price', 'bedrooms', 'bathrooms']].groupby(['bedrooms', 'bathrooms'])
        print('-' * 45)
        print(f'{"Bedrooms":<15}{"Bathrooms":<15}Sum of prices')
        print('-' * 45)
        for joint, frame in df:
            print(f'{joint[0]:<15}{joint[1]:<15}{frame.sum().values[0]}')
        print('-' * 45)

    def mean_living_room_size_per_built_year(data):
        df = data[['sqft_living', 'yr_built']].groupby('yr_built')
        print('-' * 45)
        print(f'{"Average sqft living":<30}Build year')
        print('-' * 45)
        for build_year, frame in df:
            print(f'{round(frame.mean().values[0], 2):<30}{build_year}')
        print('-' * 45)

    def median_living_room_size_per_built_year(data):
        df = data[['sqft_living', 'yr_built']].groupby('yr_built')
        print('-' * 45)
        print(f'{"Medium size sqft living":<30}Build year')
        print('-' * 45)
        for build_year, frame in df:
            print(f'{round(frame.median().values[0], 2):<30}{build_year}')
        print('-' * 45)

    def std_dev_living_room_sizes_per_built_year(data):
        df = data[['sqft_living', 'yr_built']].groupby('yr_built')
        print('-' * 60)
        print(f'{"Standard deviation sqft living":<50}Build year')
        print('-' * 60)
        for build_year, frame in df:
            print(f'{round(frame.std().values[0], 2):<50}{build_year}')
        print('-' * 60)

    def chart1(data):
        pd.set_option('display.float_format',
                      lambda x: '%.2f' % x)  # Set a formatting that disables scientific notation of being used,
        # First graph.
        data['year'] = pd.to_datetime(data['date']).dt.year  # Get the year of the dates.
        chart_by_year = data[['price', 'year']].groupby('year').mean().reset_index()
        pyplot.figure(figsize=(20, 12))
        pyplot.bar(chart_by_year['year'], chart_by_year['price'])

    def chart2(data):
        data['date'] = pd.to_datetime(data['date'])
        chart_by_day = data[['price', 'date']].groupby('date').mean().reset_index()
        pyplot.figure(figsize=(20, 12))
        pyplot.plot(chart_by_day['date'], chart_by_day['price'])

    def chart3(data):
        data['year_week'] = pd.to_datetime(data['date']).dt.strftime('%Y-%U')
        chart_by_week = data[['price', 'year_week']].groupby('year_week').mean().reset_index()
        pyplot.figure(figsize=(20, 12))
        pyplot.xticks(rotation=60)  # Rotate the labels of the X axis 60 degrees.
        pyplot.plot(chart_by_week['year_week'], chart_by_week['price'])

    dt = load_data()
    properties_per_bedrooms(dt)
    properties_per_bedrooms_groupby(dt)
    properties_per_built_year(dt)
    least_bedroom_number_per_built_year(dt)
    highest_price_per_bedroom_number(dt)
    sum_prices_per_bedroom_number(dt)
    sum_prices_per_bedroom_bathroom_number(dt)
    mean_living_room_size_per_built_year(dt)
    median_living_room_size_per_built_year(dt)
    std_dev_living_room_sizes_per_built_year(dt)
    chart1(dt)
    chart2(dt)
    chart3(dt)


# Remake the graphs and dashboards with `Streamlit`.

def streamlit_app():
    @slit.cache(allow_output_mutation=True)
    def read_csv(path='datasets/kc_house_data.csv'):
        csv_data = pd.read_csv(path)
        csv_data['date'] = pd.to_datetime(csv_data['date'])
        return csv_data

    def draw_header():
        slit.title("""
            House Rocket Company
        """)
        slit.markdown('Welcome to House Rocket data analysis')
        slit.header('Graphs and dashboards')

    def draw_dashboard(dt):
        pyplot.rcParams.update({'font.size': 22})
        fig = pyplot.figure(figsize=(30, 30))
        specs = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)
        ax1 = fig.add_subplot(specs[0, :])  # First row.
        ax2 = fig.add_subplot(specs[1, 0])  # Second row - first column.
        ax3 = fig.add_subplot(specs[1, 1])  # Second row - second column.

        # First graph.
        dt['year'] = pd.to_datetime(dt['date']).dt.year  # Get the year of the dates.
        chart_by_year = dt[['price', 'year']].groupby('year').mean().reset_index()
        ax1.bar(chart_by_year['year'], chart_by_year['price'])

        # Second graph.
        dt['date'] = pd.to_datetime(dt['date'])
        chart_by_day = dt[['price', 'date']].groupby('date').mean().reset_index()
        ax2.plot(chart_by_day['date'], chart_by_day['price'])

        # Third graph.
        dt['year_week'] = pd.to_datetime(dt['date']).dt.strftime('%Y-%U')
        chart_by_week = dt[['price', 'year_week']].groupby('year_week').mean().reset_index()
        pyplot.xticks(rotation=90)  # Rotate the labels of the X axis 60 degrees.
        ax3.plot(chart_by_week['year_week'], chart_by_week['price'])

        slit.pyplot(fig)

    data = read_csv()
    draw_header()
    draw_dashboard(data)

# Test new kinds of filter.


if __name__ == '__main__':
    # organize_4th_class_code()
    streamlit_app()
