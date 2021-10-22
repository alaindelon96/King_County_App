import pandas as pd

import plotly.express as px

import streamlit as st

st.title('King County House Sales Data Analysis')

st.markdown('Developed By alaindelon96 guided by Comunidade DS')

#Read Data
@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])

    return data
#Load Data
data = get_data('repos/kc_house_data.csv')

#Plot Map
st.sidebar.title('Displays')
is_check = st.sidebar.checkbox('Table')
is_check1 = st.sidebar.checkbox('Map')

#Transforming data
data['dormitory_type'] = data['bedrooms'].apply( lambda x: 'studio' if x == 1 else
                                                           'apartment' if x == 2 else
                                                           'house' if x > 2 else 'NA')

data['condition_status'] = data['condition'].sort_values(ascending=True).apply( lambda x: 'critical' if x == 1 else
                                                              'poor' if x == 2 else
                                                              'regular' if x == 3 else
                                                              'good' if x == 4 else
                                                              'excellent' if x == 5 else 'NA')

bedrooms_int = data['bedrooms'].sort_values(ascending=True).unique()
bathrooms_int = data['bathrooms'].sort_values(ascending=True).unique()
year_built = data['yr_built'].sort_values(ascending=True).unique().tolist()
year_renovated = data['yr_renovated'].sort_values(ascending=True).unique().tolist()
data['is_waterfront'] = data['waterfront'].apply( lambda x: 'yes' if x == 1 else'no')

#Filters
st.sidebar.title('Filters')

dormitory_option = st.sidebar.radio("Property type", data['dormitory_type'].unique())

condition_option = st.sidebar.radio("Property condition", data['condition_status'].unique().tolist())

waterfront_option = st.sidebar.radio("Is Waterfront?", data['is_waterfront'].unique().tolist())

bedrooms_min = st.sidebar.select_slider("Min of Bedrooms",
                                        bedrooms_int,
                                        value=0)

bathrooms_min = st.sidebar.select_slider("Min of bathrooms",
                                         bathrooms_int,
                                         value=0)

year_built_min = st.sidebar.select_slider("Year Built",
                                         year_built,
                                         value=data['yr_built'].min())

year_renovated_min = st.sidebar.select_slider("Last Renovation",
                                         year_renovated,
                                         value=data['yr_renovated'].min())

price_limit = st.sidebar.slider("Price Limit",
                                min_value=0.0,
                                max_value=data['price'].max(),
                                step=100.0)





if is_check:
    # #select road
    houses = data[(data['dormitory_type'] == dormitory_option) &
                  (data['bedrooms'] > bedrooms_min) &
                  (data['bathrooms'] > bathrooms_min) &
                  (data['price'] < price_limit) &
                  (data['condition_status'] == condition_option) &
                  (data['yr_built'] > year_built_min) &
                  (data['yr_renovated'] > year_renovated_min) &
                  (data['is_waterfront'] == waterfront_option)][['id','bedrooms', 'price', 'dormitory_type', 'condition_status']]
    #
    st.dataframe(houses)
    st.write(len(houses), "properties available for sale")

if is_check1:
    houses = data[(data['dormitory_type'] == dormitory_option) &
                  (data['bedrooms'] > bedrooms_min) &
                  (data['bathrooms'] > bathrooms_min) &
                  (data['price'] < price_limit) &
                  (data['condition_status'] == condition_option) &
                  (data['yr_built'] > year_built_min) &
                  (data['yr_renovated'] > year_renovated_min) &
                  (data['is_waterfront'] == waterfront_option)][['id', 'lat', 'long', 'price', 'dormitory_type', 'condition_status']]
    #draw_map
    fig1 = px.scatter_mapbox(houses,
                             lat='lat',
                             lon='long',
                             size='price',
                             color_continuous_scale=px.colors.sequential.Inferno,
                             size_max=10,
                             zoom=10)

    fig1.update_layout(mapbox_style='open-street-map')
    fig1.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    st.plotly_chart(fig1)
    st.write(len(houses), "properties available for sale")
