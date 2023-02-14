import streamlit as slit
import pandas as pd
import numpy as np
import folium as fl
import geopandas as gp
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from plotly import express as exp
from datetime import datetime

slit.set_page_config(layout='wide')


@slit.cache_data
def read_data(path='/home/leafar/Documents/dev/py/ds/datasets/kc_house_data.csv'):
    data = pd.read_csv(path)
    data['sqmt_lot'] = data['sqft_lot'] * 0.09290304
    data['price_m2'] = data['price'] / data['sqmt_lot']
    data['date'] = pd.to_datetime(data['date'])
    return data


def header(data):
    slit.markdown('# Welcome to House Rocket CEO\'s Dashboard')
    slit.markdown('## \'kc_house_data.csv\' head')
    slit.dataframe(data.head())


def overview(dt):
    slit.markdown('## Overview Based on Selected Columns and Zipcode')
    col_sel = slit.sidebar.multiselect('Select columns names', dt.columns)
    zip_sel = slit.sidebar.multiselect('Select zipcode', dt['zipcode'].unique())
    if col_sel == [] and zip_sel == []:
        df = dt.copy()
    elif col_sel != [] and zip_sel != []:
        df = dt.loc[dt['zipcode'].isin(zip_sel), col_sel]
    elif col_sel != [] and zip_sel == []:
        df = dt[col_sel]
    else:
        df = dt[dt['zipcode'].isin(zip_sel)]
    slit.dataframe(df)


def average_metrics(dt):
    slit.markdown('## Average Metrics of the Data')
    ids_per_zipcode = dt[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    price_mean_per_zipcode = dt[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    sqft_living_mean_per_zipcode = dt[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    price_m2_mean_per_zipcode = dt[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()
    m1 = pd.merge(ids_per_zipcode, price_mean_per_zipcode, on='zipcode', how='inner')
    m2 = pd.merge(m1, sqft_living_mean_per_zipcode, on='zipcode', how='inner')
    m3 = pd.merge(m2, price_m2_mean_per_zipcode, on='zipcode', how='inner')
    m3.columns = ['zipcode', 'properties', 'price mean', 'sqft_living mean', 'price per sqmt mean']
    slit.dataframe(m3)


def descriptive_statistics(dt):
    slit.markdown('## Descriptive Statistics of the Numerical Data')
    num_attr = dt.select_dtypes(include=['int64', 'float64'])
    mean_df = pd.DataFrame(num_attr.apply(np.mean))
    median_df = pd.DataFrame(num_attr.apply(np.median))
    max_df = pd.DataFrame(num_attr.apply(np.max))
    min_df = pd.DataFrame(num_attr.apply(np.min))
    std_df = pd.DataFrame(num_attr.apply(np.std))
    desc_stat_dataframe = pd.concat([mean_df, median_df, max_df, min_df, std_df], axis=1).reset_index()
    desc_stat_dataframe.columns = ['attribute', 'mean', 'median', 'max', 'min', 'std']
    slit.dataframe(desc_stat_dataframe)


@slit.cache_data
def get_geo_data(path='/home/leafar/Documents/dev/py/ds/Zip_Codes.geojson'):
    return gp.read_file(path)


def maps(dt):
    slit.header('Region Overview')
    m1, m2 = slit.columns((1, 1))
    m1.markdown('### Portfolio Density')
    # df = dt.copy()
    df = dt.sample(1000)
    dens_map = fl.Map(
        location=[df['lat'].mean(), df['long'].mean()],
        default_zoom_start=15
    )
    mc = MarkerCluster().add_to(dens_map)
    for name, row in df.iterrows():
        fl.Marker(
            [row['lat'], row['long']],
            popup=f'Price: ${row["price"]}\nDate: {row["date"]}\nSqft living: {row["sqft_living"]}\nBedrooms:'
                  f'{row["bedrooms"]}\nBathrooms: {row["bathrooms"]}\nBuild year: {row["yr_built"]}'
        ).add_to(mc)

    with m1:
        folium_static(dens_map)
    m2.markdown('### Price Density')
    price_map_df = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    price_map_df.columns = ['zip', 'price']
    price_map = fl.Map(
        location=[df['lat'].mean(), df['long'].mean()],
        default_zoom_start=15
    )
    geo_data = get_geo_data()
    filtered_geo_data = geo_data[geo_data['ZIP'].isin(price_map_df['zip']).tolist()]
    price_map.choropleth(
        data=price_map_df,
        geo_data=filtered_geo_data,
        columns=['zip', 'price'],
        key_on='feature.properties.ZIP',
        fill_color='YlOrRd',
        fill_opacity=.7,
        line_opacity=.2,
        legend_name='Average Price'
    )
    with m2:
        folium_static(price_map)


def plot_line_graphs(dt):
    slit.markdown('## Commercial Attributes')
    slit.sidebar.title('Commercial Options')
    min_year_built, max_year_built = int(dt['yr_built'].min()), int(dt['yr_built'].max())
    slit.sidebar.subheader('Select max built year')
    yr_built_sel = slit.sidebar.slider(
        'Built year',
        max_value=max_year_built,
        min_value=min_year_built,
        value=min_year_built
    )
    filtered_per_year = dt[dt['yr_built'] <= yr_built_sel]
    price_per_year_data = filtered_per_year[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
    price_per_year_chart = exp.line(price_per_year_data, x='yr_built', y='price', title='Price Average per Year')
    slit.plotly_chart(price_per_year_chart, use_container_width=True)
    dt['date'] = dt['date'].dt.strftime('%Y-%m-%d')
    slit.sidebar.subheader('Select max date')
    min_date, max_date = datetime.strptime(dt['date'].min(), '%Y-%m-%d'), datetime.strptime(dt['date'].max(),
                                                                                            '%Y-%m-%d')
    date_sel = slit.sidebar.slider(
        'Date',
        max_value=max_date,
        min_value=min_date,
        value=min_date
    )
    filtered_per_date = dt[pd.to_datetime(dt['date']) <= date_sel]
    price_per_day_data = filtered_per_date[['date', 'price']].groupby('date').mean().reset_index()
    price_per_day_chart = exp.line(price_per_day_data, x='date', y='price', title='Price Average per Day')
    slit.plotly_chart(price_per_day_chart, use_container_width=True)


def histogram(dt):
    slit.markdown('## Price Distribution')


if __name__ == '__main__':
    read_dt = read_data()
    header(read_dt)
    overview(read_dt)
    average_metrics(read_dt)
    descriptive_statistics(read_dt)
    maps(read_dt)
    plot_line_graphs(read_dt)
