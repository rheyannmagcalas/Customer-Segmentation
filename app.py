#!/usr/bin/env python
# coding: utf-8

# In[23]:


import numpy as np
import pandas as pd
import streamlit as st

from bokeh.plotting import figure, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral
from bokeh.palettes import Spectral6, Magma, Inferno
from bokeh.themes import built_in_themes
from bokeh.io import curdoc

from datetime import date, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth


# In[27]:


st.title('Customer Segmentation')


# In[25]:


data_load_state = st.text('Loading data...')


@st.cache(allow_output_mutation=True)  
def get_data():
    product_caregorization = pd.read_csv('https://eskwelabs.s3.amazonaws.com/Categorized(teamjohn).csv')
    raw_data = pd.read_csv('https://eskwelabs.s3.amazonaws.com/H_new_df.csv')
    clean_data = raw_data
    return raw_data, clean_data, product_caregorization


# In[ ]:


def get_contributors():
    st.subheader('Contributors')
    st.write('-----------------------------')
    st.markdown("<ul>"                "<li>Albert Yumol</li>"                "<li>Alphonso Balagtas</li>"                "<li>Danilo Gubaton</li>"                "<li>Elissa Mae Cabal</li>"                "<li>Emerson Chua</li>"                "<li>Franz Taborlupa</li>"                "<li>Gabriel Ong</li>"                "<li>Janina Reyes</li>"                "<li>John Barrion</li>"                "<li>Joleil Villena</li>"                "<li>Jonas Beltran</li>"                "<li>Justine Guino</li>"                "<li>Justine Brian Santoalla</li>"                "<li>Kemp Po</li>"                "<li>Kenrick Nocom</li>"                "<li>Paul Allen Chavit</li>"                "<li>Rai Ferrer</li>"                "<li>Rhey Ann Magcalas</li>"                "<li>Roberto Banadera</li>"                "<li>Ruth Ann Cabria</li>"                "<li>William Revilla</li>"                "</ul>", 
                unsafe_allow_html=True)


# In[66]:


from PIL import Image
data_load_state.text('')

image = Image.open('eskwelabs.png')
st.sidebar.image(image, caption='', use_column_width=True)
st.sidebar.markdown("<h1 style='text-align: center;margin-bottom:50px'>DS Cohort V</h1>", unsafe_allow_html=True)

raw_data, clean_data, product_categorization = get_data()

add_selectbox = st.sidebar.radio(
    "",
    ("Introduction and Problem Statement", "Data Set", "Outline and List of Tools", "Data Cleaning", "Exploratory Data Analysis", 
     "RFM Model", "K-Means Clustering and Validation", "Market Basket Analysis", "Contributors")
)


if add_selectbox == 'Introduction and Problem Statement':
    st.subheader('Introduction')
    st.write('An e-commerce company which sells souvenirs wants to segment its customers and determine marketing '             'strategies according to these segments. For this purpose, we will define the behavior of customers '             'and we will put the customers into same groups who exhibit common behaviors and then we will try to '             'develop sales and marketing techniques specific to these groups')
    st.write('0. Introduce Company, set context ')
    st.write("I. We don't know who the customers are (based on season, transactions, time period, top products per "    "continent - market research).")
    st.write("II. Why is that a problem?")
    
    st.sidebar.markdown("<h1 style='text-align: center;margin-bottom:50px'></h1>", unsafe_allow_html=True)
    
elif add_selectbox == 'Data Set':
    st.subheader('Data Set')
    st.write('This is a transnational data set which contains all the transactions '             'occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered '             'non-store online retail.The company mainly sells unique all-occasion gifts. '             'Many customers of the company are wholesalers.')
    st.table(raw_data.head(5))
    
    data_types = list(raw_data.dtypes)
    data_columns = list(raw_data.columns)
    
    st.write('Data Dimensions: Rows:   {}, Columns:   {}'.format(str(raw_data.shape[0]), str(raw_data.shape[1])))
    
    st.subheader('Data Description:')
    data_details = {
        'columns': raw_data.columns,
        'Data Types': raw_data.dtypes,
        'Description': ['A unique number that is assigned to each invoice', 
                        'Unique number assigned to each distinct product. ', 
                        'Product name ', 
                        'The quantities of each product per transaction',
                        'The day and time when each transaction was generated. ', 
                        'Product price per unit ', 
                        'A unique number assigned to each customer ', 
                        'The name of the country where each customer resides. ']
    }
    
    st.table(pd.DataFrame(data_details).set_index('columns'))

elif add_selectbox == 'Outline and List of Tools':    
    outline = """
    <div>
           <div style="width:50%;float:left;">
               <b>Outline</b> <br><br>
               1. Data Set <br>
               2. Data Cleaning <br>
               3. EDA <br>
               4. Feature Engineering  <br>
               5. Goal: Customer Segmentation <br>
               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A. RFM & Validation <br>
               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;B. K Means <br>
               6. Deployment + Demo <br>
               7. Conclusion <br>
               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A. Results <br>
               &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;B. Market Basket Analysis <br>
           </div>
           <div style="Width:50%;float:right">
               <b>List of Tools</b> <br><br>
                1. IPython (Jupyter) <br>
                2. Heatmap, Correlation <br>
                3. Elbow Method <br>
                4. Davies-Bouldin <br>
                5. Silhouette <br>
                6. ANOVA <br>
                7. Tukey’s Test <br>
                8. Heroku <br>
                9. Bokeh <br>
                10. Streamlit <br>
                11. Github <br>
                12. Regex <br>
                13. NLTK <br>
                14. Seaborn <br>
                15. Pandas <br>
                16. Matplotlib <br>
                17. Numpy <br>
                18. Scipy <br>
                19. Statmodels <br>
           </div>
    </div>
    """
    st.write(outline, unsafe_allow_html=True)

    
elif add_selectbox == 'Data Cleaning':
    st.subheader('Data Cleaning')
    get_null_sum = raw_data.isnull().sum()
    st.write('Check Null Values Per Column:')
    
    column_values = list(get_null_sum.keys())
    column_null_count = list(raw_data.isnull().sum().values)
    
    
    source1 = ColumnDataSource(data=dict(column_values=column_values, column_null_count=column_null_count, 
                                         color=['#35193e', '#35193e', '#701f57','#701f57', '#ad1759', '#e13342', 
                                                '#f37651', '#f6b48f']))
    
    null_plot= figure(x_range=column_values, plot_height=600, title='Column Null Counts')
    
    null_plot.vbar(x='column_values', top='column_null_count', width=0.5, color='color', 
                   legend_field='column_values', source=source1)
    
    null_plot.xaxis.axis_label = 'Columns'
    null_plot.yaxis.axis_label = 'Null Counts'
    null_plot.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(null_plot)
    
    st.write('Conclusion: We Need To Remove Null Values from CustomerID Column')    
    clean_column_values = list(clean_data.columns)
    clean_column_null_count = list(clean_data.count())
    
    source1 = ColumnDataSource(data=dict(column_values=clean_column_values, column_null_count=clean_column_null_count, 
                                         color=['#35193e', '#35193e', '#701f57','#701f57', '#ad1759', '#e13342', 
                                                '#f37651', '#f6b48f']))
    clean_p= figure(x_range=column_values, plot_height=600, title='Clean Data Count')
    clean_p.vbar(x='column_values', top='column_null_count', width=0.5, color='color', legend_field='column_values', 
           source=source1)
    clean_p.xaxis.axis_label = 'Columns'
    clean_p.yaxis.axis_label = 'Null Counts'
    clean_p.xaxis.major_label_orientation = 1.2
    clean_p.legend.visible = False
    st.bokeh_chart(clean_p)
    
    
    
    st.write('Checking Other Information')
    number_data = {
        'Column':  ['Quantity', 'UnitPrice'],
        'Minimum': [min(raw_data['Quantity']), min(raw_data['UnitPrice'])],
        'Maximum': [max(raw_data['Quantity']), max(raw_data['UnitPrice'])]
    }
    st.table(pd.DataFrame(number_data).set_index('Column'))
    st.write('Conclusion: We Need To Remove Negative Values from Quantity Column')
    
    st.write('Adding Total Amount Column: Quantity * UnitPrice')
    
    st.write('Current Data Dimensions: Rows:   {}, Columns:   {}'.format(
        str(clean_data.shape[0]), str(clean_data.shape[1])))
    
    clean_data = clean_data.loc[:, ~clean_data.columns.str.contains('^Unnamed')]
    
    st.write(clean_data.head(10))
    
elif add_selectbox == 'Exploratory Data Analysis':
    
    st.subheader('Exploratory Data Analysis')
    clean_data['InvoiceDate'] = pd.to_datetime(clean_data['InvoiceDate'])
    
    clean_data['day'] = clean_data['InvoiceDate'].dt.dayofweek
    clean_data['month'] = clean_data['InvoiceDate'].dt.month
    clean_data['hour'] = clean_data['InvoiceDate'].dt.hour
    
    df_uk = clean_data[clean_data['Country']=='United Kingdom']
    df_nonuk = clean_data[clean_data['Country']!='United Kingdom']
    
    uk_total_purchase = df_uk.groupby('hour')['InvoiceNo'].nunique().sum()
    nonuk_total_purchase = df_nonuk.groupby('hour')['InvoiceNo'].nunique().sum()

    uk_hour = df_uk.groupby('hour')['InvoiceNo'].nunique()/uk_total_purchase*100
    uk_day = df_uk.groupby('day')['InvoiceNo'].nunique()/uk_total_purchase*100
    uk_month = df_uk.groupby('month')['InvoiceNo'].nunique()/uk_total_purchase*100

    nonuk_hour = df_nonuk.groupby('hour')['InvoiceNo'].nunique()/nonuk_total_purchase*100
    nonuk_day = df_nonuk.groupby('day')['InvoiceNo'].nunique()/nonuk_total_purchase*100
    nonuk_month = df_nonuk.groupby('month')['InvoiceNo'].nunique()/nonuk_total_purchase*100
    
    hour_labels_uk = ['6am','7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm']
    hour_labels_nonuk = ['7am','8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm']
    month_labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    day_labels = ['Mon','Tue','Wed','Thu','Fri','Sun']

    
    top10_countries = clean_data.groupby('Country')['amount'].sum().sort_values(ascending=False).head(10)
    st.write('-----------------------------------------------------------------------') 
    
    top_10_country_purchase_source = ColumnDataSource(data=dict(column_values=list(top10_countries.index), 
                                        column_null_count=list(top10_countries.values), 
                                         color=['#35193e','#35193e','#701f57','#701f57',
                                                '#ad1759','#ad1759','#ad1759', '#e13342', '#f37651', '#f6b48f']))
    top_10_country_purchase = figure(x_range=list(top10_countries.index), plot_height=500, plot_width=600, 
                                title='Top 10 Highest Purchasing Countries')
    
    top_10_country_purchase.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=top_10_country_purchase_source)
                                         
                                         
    top_10_country_purchase.xaxis.axis_label = 'Countries'
    top_10_country_purchase.yaxis.axis_label = 'Total Purchases'
    top_10_country_purchase.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(top_10_country_purchase)
    
    
    st.subheader('UK Vs Other Countries')
    st.write('-----------------------------------------------------------------------')
    uk_purchases_day_source = ColumnDataSource(data=dict(column_values=hour_labels_uk, 
                                        column_null_count=list(uk_hour.values), 
                                         color=['#35193e','#35193e','#35193e', '#701f57','#701f57','#701f57',
                                                '#ad1759','#ad1759','#ad1759', '#e13342', '#e13342', '#e13342',
                                                '#f37651','#f37651','#f37651', '#f6b48f',  '#f6b48f']))
    uk_purchases_day = figure(x_range=hour_labels_uk, plot_height=500, plot_width=600, 
                                title='No of purchases on certain times within the day on UK')
    
    uk_purchases_day.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=uk_purchases_day_source)
                                         
                                         
    uk_purchases_day.xaxis.axis_label = 'Hour'
    uk_purchases_day.yaxis.axis_label = 'Percentage of Purchases'
    uk_purchases_day.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(uk_purchases_day)
    
    
    non_uk_purchases_day_source = ColumnDataSource(data=dict(column_values=hour_labels_nonuk, 
                                        column_null_count=list(nonuk_hour.values), 
                                         color=['#35193e','#35193e','#35193e', '#701f57','#701f57','#701f57',
                                                '#ad1759','#ad1759','#ad1759', '#e13342', '#e13342', '#e13342',
                                                '#f37651','#f37651','#f37651', '#f6b48f',  '#f6b48f']))
    non_uk_purchases_day = figure(x_range=hour_labels_nonuk, plot_height=500, plot_width=600, 
                                title='No of purchases on certain times within the day on Other Countries')
    
    non_uk_purchases_day.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=non_uk_purchases_day_source)
                                         
                                         
    non_uk_purchases_day.xaxis.axis_label = 'Hour'
    non_uk_purchases_day.yaxis.axis_label = 'Percentage of Purchases'
    non_uk_purchases_day.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(non_uk_purchases_day)
    
    st.write('Conclusion: People buy more stuff at 12pm (UK), 10am(Other Countries) ')
    st.write('-----------------------------------------------------------------------')
    

    uk_purchases_week_source = ColumnDataSource(data=dict(column_values=day_labels, 
                                        column_null_count=list(uk_day.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    uk_purchases_week = figure(x_range=day_labels, plot_height=500, plot_width=600, 
                                title='Percentage of purchases on certain days of the week on UK')
    
    uk_purchases_week.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=uk_purchases_week_source)
                                            
    uk_purchases_week.xaxis.axis_label = 'Day'
    uk_purchases_week.yaxis.axis_label = 'Percentage of Purchases'
    uk_purchases_week.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(uk_purchases_week)
    
    nonuk_purchases_week_source = ColumnDataSource(data=dict(column_values=day_labels, 
                                        column_null_count=list(nonuk_day.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    nonuk_purchases_week = figure(x_range=day_labels, plot_height=500, plot_width=600, 
                                title='Percentage of purchases on certain days of the week on other countries')
    
    nonuk_purchases_week.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=nonuk_purchases_week_source)
                                            
    nonuk_purchases_week.xaxis.axis_label = 'Day'
    nonuk_purchases_week.yaxis.axis_label = 'Percentage of Purchases'
    nonuk_purchases_week.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(nonuk_purchases_week)
    
    st.write('Conclusion: People buy more stuff on Thursdays.')
    st.write('-----------------------------------------------------------------------')
    
    uk_purchases_year_source = ColumnDataSource(data=dict(column_values=month_labels, 
                                        column_null_count=list(uk_month.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    uk_purchases_year = figure(x_range=month_labels, plot_height=500, plot_width=600, 
                                title='Percentage of purchases within the year on UK')
    
    uk_purchases_year.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=uk_purchases_year_source)
                                            
    uk_purchases_year.xaxis.axis_label = 'Month'
    uk_purchases_year.yaxis.axis_label = 'Percentage of Purchases'
    uk_purchases_year.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(uk_purchases_year)
    
    
    nonuk_purchases_year_source = ColumnDataSource(data=dict(column_values=month_labels, 
                                        column_null_count=list(nonuk_month.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    nonuk_purchases_year = figure(x_range=month_labels, plot_height=500, plot_width=600, 
                                title='Percentage of purchases within the year on other countries')
    
    nonuk_purchases_year.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=nonuk_purchases_year_source)
                                            
    nonuk_purchases_year.xaxis.axis_label = 'Month'
    nonuk_purchases_year.yaxis.axis_label = 'Percentage of Purchases'
    nonuk_purchases_year.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(nonuk_purchases_year)
    
    st.write('Conclusion: People buy more stuff from September to December')
    st.write('-----------------------------------------------------------------------')
    
    product_categorization.loc[product_categorization['Country'] == 'United Kingdom', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'France', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Australia', 'Continent'] = 'Oceania'
    product_categorization.loc[product_categorization['Country'] == 'Netherlands', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Germany', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Norway', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'EIRE', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Switzerland', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Spain', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Poland', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Portugal', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Italy', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Belgium', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Lithuania', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Japan', 'Continent'] = 'Asia'
    product_categorization.loc[product_categorization['Country'] == 'Iceland', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Channel Islands', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Denmark', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Cyprus', 'Continent'] = 'Asia'
    product_categorization.loc[product_categorization['Country'] == 'Sweden', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Finland', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Austria', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Greece', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Singapore', 'Continent'] = 'Asia'
    product_categorization.loc[product_categorization['Country'] == 'Lebanon', 'Continent'] = 'Asia'
    product_categorization.loc[product_categorization['Country'] == 'United Arab Emirates', 'Continent'] = 'Asia'
    product_categorization.loc[product_categorization['Country'] == 'Israel', 'Continent'] = 'Asia'
    product_categorization.loc[product_categorization['Country'] == 'Saudi Arabia', 'Continent'] = 'Asia'
    product_categorization.loc[product_categorization['Country'] == 'Czech Republic', 'Continent'] = 'Asia'
    product_categorization.loc[product_categorization['Country'] == 'Canada', 'Continent'] = 'North America'
    product_categorization.loc[product_categorization['Country'] == 'Unspecified', 'Continent'] = 'Unspecified'
    product_categorization.loc[product_categorization['Country'] == 'Brazil', 'Continent'] = 'South America'
    product_categorization.loc[product_categorization['Country'] == 'USA', 'Continent'] = 'North America'
    product_categorization.loc[product_categorization['Country'] == 'European Community', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'Bahrain', 'Continent'] = 'Asia'
    product_categorization.loc[product_categorization['Country'] == 'Malta', 'Continent'] = 'Europe'
    product_categorization.loc[product_categorization['Country'] == 'RSA', 'Continent'] = 'Africa'

    df_groupby_inv = product_categorization.groupby(['InvoiceNo','Continent']).sum().reset_index()
    #df_groupby_inv_average = product_categorization.groupby(['InvoiceNo','Continent']).mean().reset_index()
    
    st.subheader('Continent')
    st.write('-----------------------------------------------------------------------')
    purchase_continent_values = df_groupby_inv.groupby('Continent').sum().reset_index().sort_values(
        by='Quantity',ascending=False)
    
    purchase_continent_source = ColumnDataSource(data=dict(column_values=list(purchase_continent_values['Continent']), 
                                        column_null_count=list(purchase_continent_values['Quantity']), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    purchase_continent = figure(x_range=purchase_continent_values['Continent'], plot_height=500, plot_width=600, 
                                title='Total Quantity Purchase per Continent')
    
    purchase_continent.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=purchase_continent_source)
                                            
    purchase_continent.xaxis.axis_label = 'Continent'
    purchase_continent.yaxis.axis_label = 'Total Quantity Purchase'
    purchase_continent.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(purchase_continent)
    
    purchase_continent_values_average = df_groupby_inv.groupby('Continent').mean().reset_index().sort_values(
        by='Quantity',ascending=False)
    
    purchase_continent_average_source = ColumnDataSource(data=dict(column_values=
                                                                   list(purchase_continent_values_average['Continent']), 
                                        column_null_count=list(purchase_continent_values_average['amount']), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    
    purchase_continent_average = figure(x_range=purchase_continent_values_average['Continent'], plot_height=500, plot_width=600, 
                                title='Average Quantity per Continent')
    
    purchase_continent_average.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=purchase_continent_average_source)
                                            
    purchase_continent_average.xaxis.axis_label = 'Continent'
    purchase_continent_average.yaxis.axis_label = 'Total Purchases'
    purchase_continent_average.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(purchase_continent_average)
    
    purchase_continent_average= df_groupby_inv.groupby('Continent')['amount'].mean().reset_index()
    
    purchase_continent_average_amount_source = ColumnDataSource(data=dict(column_values=
                                                                   list(purchase_continent_values_average['Continent']), 
                                        column_null_count=list(purchase_continent_values_average['amount']), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    
    purchase_continent_average_amount = figure(x_range=purchase_continent_values_average['Continent'], plot_height=500, plot_width=600, 
                                title='Average Amount of Items per Continent')
    
    purchase_continent_average_amount.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=purchase_continent_average_amount_source)
                                            
    purchase_continent_average_amount.xaxis.axis_label = 'Continent'
    purchase_continent_average_amount.yaxis.axis_label = 'Amount'
    purchase_continent_average_amount.xaxis.major_label_orientation = 1.2
    st.bokeh_chart(purchase_continent_average_amount)
    
    
    
    df_all_top10_qty = product_categorization.groupby('description_category')['Quantity'].sum().sort_values(ascending = False).head(10)

    
    top10_product_source = ColumnDataSource(data=dict(column_values=list(df_all_top10_qty.index), 
                                        column_null_count=list(df_all_top10_qty.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    
    top10_product = figure(x_range=list(df_all_top10_qty.index), plot_height=500, plot_width=600, 
                                title='Top 10 Products Categories')
    
    top10_product.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=top10_product_source)
                                            
    top10_product.xaxis.axis_label = 'Product'
    top10_product.yaxis.axis_label = 'Quantity Purchased'
    top10_product.xaxis.major_label_orientation = 1.2
    top10_product.legend.visible = False
    st.bokeh_chart(top10_product)
    
    df_europe_top10_qty = product_categorization[product_categorization['Continent'] == 'Europe'].groupby('description_category')['Quantity'].sum().sort_values(ascending = False).head(10)
    df_oceania_top10_qty = product_categorization[product_categorization['Continent'] == 'Oceania'].groupby('description_category')['Quantity'].sum().sort_values(ascending = False).head(10)
    df_asia_top10_qty = product_categorization[product_categorization['Continent'] == 'Asia'].groupby('description_category')['Quantity'].sum().sort_values(ascending = False).head(10)
    df_northamerica_top10_qty = product_categorization[product_categorization['Continent'] == 'North America'].groupby('description_category')['Quantity'].sum().sort_values(ascending = False).head(10)
    df_southamerica_top10_qty = product_categorization[product_categorization['Continent'] == 'South America'].groupby('description_category')['Quantity'].sum().sort_values(ascending = False).head(10)
    df_africa_top10_qty = product_categorization[product_categorization['Continent'] == 'Africa'].groupby('description_category')['Quantity'].sum().sort_values(ascending = False).head(10)

    
    df_europe_top10_qty_source = ColumnDataSource(data=dict(column_values=list(df_europe_top10_qty.index), 
                                        column_null_count=list(df_europe_top10_qty.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    
    df_europe_top10 = figure(x_range=list(df_all_top10_qty.index), plot_height=500, plot_width=600, 
                                title='Top 10 Product Categories in Europe (QTY)')
    
    df_europe_top10.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=df_europe_top10_qty_source)
                                            
    df_europe_top10.xaxis.axis_label = 'Product'
    df_europe_top10.yaxis.axis_label = 'Quantity Purchased'
    df_europe_top10.xaxis.major_label_orientation = 1.2
    df_europe_top10.legend.visible = False
    st.bokeh_chart(df_europe_top10)
    
    df_asia_top10_qty_source = ColumnDataSource(data=dict(column_values=list(df_oceania_top10_qty.index), 
                                        column_null_count=list(df_oceania_top10_qty.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    
    df_oceania_top10 = figure(x_range=list(df_oceania_top10_qty.index), plot_height=500, plot_width=600, 
                                title='Top 10 Product Categories in Oceania (QTY)')
    
    df_oceania_top10.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=df_asia_top10_qty_source )
                                            
    df_oceania_top10.xaxis.axis_label = 'Product'
    df_oceania_top10.yaxis.axis_label = 'Quantity Purchased'
    df_oceania_top10.xaxis.major_label_orientation = 1.2
    df_oceania_top10.legend.visible = False
    st.bokeh_chart(df_oceania_top10)
    
    df_asia_top10_qty_source = ColumnDataSource(data=dict(column_values=list(df_asia_top10_qty.index), 
                                        column_null_count=list(df_asia_top10_qty.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    
    df_asia_top10 = figure(x_range=list(df_oceania_top10_qty.index), plot_height=500, plot_width=600, 
                                title='Top 10 Product Categories in Asia (QTY)')
    
    df_asia_top10.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=df_asia_top10_qty_source)
                                            
    df_asia_top10.xaxis.axis_label = 'Product'
    df_asia_top10.yaxis.axis_label = 'Quantity Purchased'
    df_asia_top10.xaxis.major_label_orientation = 1.2
    df_asia_top10.legend.visible = False
    st.bokeh_chart(df_asia_top10)
    
    df_northamerica_top10_qty_source = ColumnDataSource(data=dict(column_values=list(df_northamerica_top10_qty.index), 
                                        column_null_count=list(df_northamerica_top10_qty.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    
    df_northamerica_top10 = figure(x_range=list(df_northamerica_top10_qty.index), plot_height=500, plot_width=600, 
                                title='Top 10 Product Categories in North America (QTY)')
    
    df_northamerica_top10.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=df_northamerica_top10_qty_source)
                                            
    df_northamerica_top10.xaxis.axis_label = 'Product'
    df_northamerica_top10.yaxis.axis_label = 'Quantity Purchased'
    df_northamerica_top10.xaxis.major_label_orientation = 1.2
    df_northamerica_top10.legend.visible = False
    st.bokeh_chart(df_northamerica_top10)
    
    
    df_southamerica_top10_qty_source = ColumnDataSource(data=dict(column_values=list(df_southamerica_top10_qty.index), 
                                        column_null_count=list(df_southamerica_top10_qty.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    
    df_southamerica_top10 = figure(x_range=list(df_southamerica_top10_qty.index), plot_height=500, plot_width=600, 
                                title='Top 10 Product Categories in South America (QTY)')
    
    df_southamerica_top10.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=df_southamerica_top10_qty_source)
                                            
    df_southamerica_top10.xaxis.axis_label = 'Product'
    df_southamerica_top10.yaxis.axis_label = 'Quantity Purchased'
    df_southamerica_top10.xaxis.major_label_orientation = 1.2
    df_southamerica_top10.legend.visible = False
    st.bokeh_chart(df_northamerica_top10)
    
    df_africa_top10_qty_source = ColumnDataSource(data=dict(column_values=list(df_africa_top10_qty.index), 
                                        column_null_count=list(df_africa_top10_qty.values), 
                                         color=['#35193e', '#701f57', '#ad1759', '#e13342', '#f37651', '#f6b48f']))
    
    df_africa_top10 = figure(x_range=list(df_africa_top10_qty.index), plot_height=500, plot_width=600, 
                                title='Top 10 Product Categories in Africa (QTY)')
    
    df_africa_top10.vbar(x='column_values', top='column_null_count', width=0.5,
                            legend_field='column_values', color='color', source=df_africa_top10_qty_source)
                                            
    df_africa_top10.xaxis.axis_label = 'Product'
    df_africa_top10.yaxis.axis_label = 'Quantity Purchased'
    df_africa_top10.xaxis.major_label_orientation = 1.2
    df_africa_top10.legend.visible = False
    st.bokeh_chart(df_africa_top10)
    

    
elif add_selectbox == 'RFM Model':
    st.subheader('RFM Model')
    st.write('\n\n1. Recency: How much time has elapsed since a customer’s last activity or transaction with the brand')
    st.write('2. Frquency: How often has a customer transacted or interacted with the brand during a particular period of time')
    st.write('3. Monetary: How much a customer has spent with the brand during a particular period of time. ')
    
    rfm_new_df = clean_data
    
    rfm_new_df ['total_price'] = rfm_new_df ['Quantity']*rfm_new_df['UnitPrice']
    rfm_new_df ['InvoiceDate'] = pd.to_datetime(rfm_new_df['InvoiceDate'])
    reference_date = max(rfm_new_df['InvoiceDate']) + timedelta(days=1)

    history_df = rfm_new_df.groupby(['CustomerID']).agg({'InvoiceDate':lambda x: (reference_date - x.max()).days, 'InvoiceNo':'count','total_price':'sum'})
    history_df.columns = ['Recency','Frequency','Monetary']
    
    st.write("Maximum Date:"+str(max(rfm_new_df['InvoiceDate'])))
    st.write("Minimum Date:"+str(min(rfm_new_df['InvoiceDate'])))
    st.table(history_df.head(10))
    
    import math
    history_df = history_df.agg({'Recency':lambda x : x.apply(math.log),
               'Frequency':lambda x : x.apply(math.log),
               'Monetary':lambda x : x.apply(math.log)})
    
    
    plot = figure(plot_height=500, plot_width=800, title='Recency Vs Monetary')
    source = ColumnDataSource(data=dict(x=history_df['Recency'], y=history_df['Monetary']))
    plot.scatter('x', 'y', line_color=None, source=source)
    plot.xaxis.axis_label = 'Recency'
    plot.yaxis.axis_label = 'Monetary'
    st.bokeh_chart(plot)
    
    
    plot = figure(plot_height=500, plot_width=800, title='Frequency Vs Monetary')
    source = ColumnDataSource(data=dict(x=history_df['Frequency'], y=history_df['Monetary']))
    plot.scatter('x', 'y', line_color=None, source=source)
    plot.xaxis.axis_label = 'Frequency'
    plot.yaxis.axis_label = 'Monetary'
    st.bokeh_chart(plot)
    
    plot = figure(plot_height=500, plot_width=800, title='Frequency Vs Recency')
    source = ColumnDataSource(data=dict(x=history_df['Frequency'], y=history_df['Recency']))
    plot.scatter('x', 'y', line_color=None, source=source)
    plot.xaxis.axis_label = 'Frequency'
    plot.yaxis.axis_label = 'Recency'
    st.bokeh_chart(plot)
    
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')

    r = history_df.Recency
    f = history_df.Frequency
    m = history_df.Monetary
    ax.scatter(r, f, m, s=5)

    ax.set_xlabel('Recency')
    ax.set_ylabel('Frequency')
    ax.set_zlabel('Monetary')

    st.pyplot()

    RFM_final_df = history_df
    
    from sklearn import preprocessing

    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_samples, silhouette_score

    feature_vector = ['Recency','Frequency', 'Monetary']
    X_subset = RFM_final_df[feature_vector]
    scaler = preprocessing.StandardScaler().fit(X_subset)
    X_scaled = scaler.transform(X_subset)


    from sklearn.cluster import KMeans
    from sklearn.metrics import davies_bouldin_score,silhouette_score,silhouette_samples
    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import warnings
   

    sse,db,slc = {}, {}, {}
    for k in range(2, 20):
        # seed of 10 for reproducibility.
        kmeans = KMeans(n_clusters=k, max_iter=10,random_state=10).fit(X_scaled)
        if k == 3: labels = kmeans.labels_
        clusters = kmeans.labels_
        sse[k] = kmeans.inertia_ # Inertia: Sum of distances of samples to their closest cluster center
        db[k] = davies_bouldin_score(X_scaled,clusters)
        slc[k] = silhouette_score(X_scaled,clusters)
    
    p = figure(plot_width=800, plot_height=400, title='SSE Results')
    p.line(list(sse.keys() ), list(sse.values()), line_width=2)
    p.xaxis.axis_label = 'Number of Clusters'
    p.yaxis.axis_label = 'SSE'
    st.bokeh_chart(p)
    
    from kneed import *
    kl = KneeLocator(range(2,20), list(sse.values()), curve = 'convex', direction = 'decreasing')
    print("SSE Elbow"+str(kl.elbow))
    
    p = figure(plot_width=800, plot_height=400, title='DB Results')
    p.line(list(db.keys() ), list(db.values()), line_width=2)
    p.xaxis.axis_label = 'Number of Clusters'
    p.yaxis.axis_label = 'DB'
    st.bokeh_chart(p)
    print("DB Elbow"+str(list(db.keys()) [list(db.values()).index(min(db.values()))]))
    
    X = X_scaled
    for n_clusters in range(2, 20):
        # Create a subplot with 1 row and 2 columns
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(18, 7)
        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1 but in this example all
        # lie within [-0.1, 1]
        ax1.set_xlim([-0.1, 1])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility.
        clusterer = KMeans(n_clusters=n_clusters,max_iter=1000, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(X, cluster_labels)
        st.write("For n_clusters =", n_clusters,
              "The average silhouette_score is :", silhouette_avg)
        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)
        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values =                 sample_silhouette_values[cluster_labels == i]
            ith_cluster_silhouette_values.sort()
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i
            color = cm.nipy_spectral(float(i) / n_clusters)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)
            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples
        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")
        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
        # 2nd Plot showing the actual clusters formed
        colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
        ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                    c=colors, edgecolor='k')
        # Labeling the clusters
        centers = clusterer.cluster_centers_
        # Draw white circles at cluster centers
        ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
                    c="white", alpha=1, s=200, edgecolor='k')
        for i, c in enumerate(centers):
            ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                        s=50, edgecolor='k')
        ax2.set_title("The visualization of the clustered data.")
        ax2.set_xlabel("Feature space for the 1st feature")
        ax2.set_ylabel("Feature space for the 2nd feature")
        plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                      "with n_clusters = %d" % n_clusters),
                     fontsize=14, fontweight='bold')
    #st.bokeh_chart(plt)
    
    r = range(7, 0, -1)
    f = range(1, 8)
    m = range(1, 8)
    r_g = pd.qcut(RFM_final_df['Recency'], q=7, labels=r)
    f_g = pd.qcut(RFM_final_df['Frequency'], q=7, labels=f)
    m_g = pd.qcut(RFM_final_df['Monetary'], q=7, labels=m)
    RFM_final_df = RFM_final_df.assign(R = r_g.values, F = f_g.values, M = m_g.values)

    #seperate into 7 quartiles since 7 cllusters
    RFM_final_df['sum_val'] = RFM_final_df[['R', 'F', 'M']].sum(axis=1)
    st.write(RFM_final_df.head().astype('object'))

    from sklearn import preprocessing
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_samples, silhouette_score
    feature_vector = ['R','F', 'M','sum_val']


    X_subset = RFM_final_df[feature_vector]
    scaler = preprocessing.StandardScaler().fit(X_subset)
    X_scaled = scaler.transform(X_subset)
    labels = KMeans(n_clusters=7, max_iter = 100, random_state=10).fit_predict(X_scaled)
    RFM_final_df['cluster_no']= labels
    plt.figure(figsize=(20,15))
    sns.boxplot(x='cluster_no', y ='sum_val', data = RFM_final_df)
    st.pyplot()
    
    plt.figure(figsize=(20,15))
    sns.boxplot(x='cluster_no', y ='Monetary', data = RFM_final_df)
    st.pyplot()
    
    plt.figure(figsize=(20,15))
    sns.boxplot(x='cluster_no', y ='Frequency', data = RFM_final_df)
    st.pyplot()
    
    facet = sns.lmplot(data=RFM_final_df, x='Monetary', y='sum_val', hue='cluster_no', 
                   fit_reg=False, legend=True, legend_out=True, palette='rocket')
    
    st.pyplot()
    
    facet = sns.lmplot(data=RFM_final_df, x='Frequency', y='sum_val', hue='cluster_no', 
                   fit_reg=False, legend=True, legend_out=True, palette='rocket')
    
    st.pyplot()
    
    facet = sns.lmplot(data=RFM_final_df, x='Recency', y='sum_val', hue='cluster_no', 
                   fit_reg=False, legend=True, legend_out=True, palette='rocket')
    st.pyplot()
    
    facet = sns.lmplot(data=RFM_final_df, x='Frequency', y='Monetary', hue='cluster_no', 
                   fit_reg=False, legend=True, legend_out=True, palette='rocket')
    st.pyplot()
    
    facet = sns.lmplot(data=RFM_final_df, x='Monetary', y='Recency', hue='cluster_no', 
                   fit_reg=False, legend=True, legend_out=True, palette='rocket')
    
    st.pyplot()
    
    facet = sns.lmplot(data=RFM_final_df, x='Frequency', y='Recency', hue='cluster_no', 
                   fit_reg=False, legend=True, legend_out=True, palette='rocket')
    st.pyplot()
    
    facet = sns.lmplot(data=RFM_final_df, x='Frequency', y='Monetary', hue='cluster_no', 
                   fit_reg=False, legend=True, legend_out=True, palette='rocket')
    st.pyplot()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    scatter = ax.scatter(RFM_final_df['R'], RFM_final_df['sum_val'], c=RFM_final_df['cluster_no'],s=50)
    #for i,j in centers:
    #    ax.scatter(i,j,s=50,c='red',marker='+')
    ax.set_xlabel('R')
    ax.set_ylabel('sum_val')
    plt.colorbar(scatter)

    fig.show()
    
    st.pyplot()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    scatter = ax.scatter(RFM_final_df['F'], RFM_final_df['sum_val'], c=RFM_final_df['cluster_no'],s=50)
    #for i,j in centers:
    #    ax.scatter(i,j,s=50,c='red',marker='+')
    ax.set_xlabel('F')
    ax.set_ylabel('sum_val')
    plt.colorbar(scatter)

    fig.show()

    st.pyplot()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    scatter = ax.scatter(RFM_final_df['M'], RFM_final_df['sum_val'], c=RFM_final_df['cluster_no'],s=50)
    #for i,j in centers:
    #    ax.scatter(i,j,s=50,c='red',marker='+')
    ax.set_xlabel('M')
    ax.set_ylabel('sum_val')
    plt.colorbar(scatter)

    fig.show()
    st.pyplot()
    
    st.write(RFM_final_df.head().astype('object'))
    
    st.write('Look at the cluster = 4 data and try to infer things')
    
    st.table(RFM_final_df.groupby('cluster_no')['Frequency', 'Recency'].describe())
    st.table(RFM_final_df.groupby('cluster_no')['Monetary', 'sum_val'].describe())
    st.table(RFM_final_df.groupby('cluster_no')['R', 'F', 'M'].describe())
    
    test = RFM_final_df

    test = test.reset_index()

    test = test.groupby('cluster_no')['CustomerID'].nunique().sort_values(ascending=False).reset_index()
    fig.set_size_inches(10, 16)
    sns.barplot(data=test,x='cluster_no', y='CustomerID', palette='rocket', orient= True)

    st.pyplot()
    import squarify
    import matplotlib
    cmap = matplotlib.cm.tab20
    mini = min(test['CustomerID'])
    maxi = max(test['CustomerID'])
    norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
    colors = [cmap(norm(value)) for value in test['CustomerID']]
    fig = plt.gcf()
    ax = fig.add_subplot()
    fig.set_size_inches(12, 8)
    squarify.plot(sizes = test['CustomerID'],
                 label = ['Silver',
                          'Gold',
                          'Platinum',
                          'Bronze'], alpha=1, color = colors)
    
    st.write(RFM_final_df.max())    
    st.pyplot()
    
    st.write('RFM Max')
    st.write(RFM_final_df.max())
    RFM_relationships = RFM_final_df.groupby('cluster_no').mean()
    st.write('RFM Relationships')
    st.write(RFM_relationships.max())
    
    
    test = RFM_relationships

    test = test.reset_index()
    test = test.groupby('cluster_no')['Recency', 'Frequency','Monetary', 'sum_val'].mean().reset_index()
    fig.set_size_inches(10, 16)
    sns.barplot(data=test,x='cluster_no', y='sum_val', palette='rocket', orient= True)
    st.pyplot()
    
    test = RFM_relationships

    test = test.reset_index()
    test = test.groupby('cluster_no')['Recency', 'Frequency','Monetary', 'sum_val'].mean().reset_index()
    fig.set_size_inches(10, 16)
    sns.barplot(data=test,x='cluster_no', y='Frequency', palette='rocket', orient= True)
    st.pyplot()
    
    
    test = RFM_relationships

    test = test.reset_index()
    test = test.groupby('cluster_no')['Recency', 'Frequency','Monetary', 'sum_val'].mean().reset_index()
    fig.set_size_inches(10, 16)
    sns.barplot(data=test,x='cluster_no', y='Monetary', palette='rocket', orient= True)
    st.pyplot()
    
    test = RFM_relationships

    test = test.reset_index()
    test = test.groupby('cluster_no')['Recency', 'Frequency','Monetary', 'sum_val'].mean().reset_index()
    fig.set_size_inches(10, 16)
    sns.barplot(data=test,x='cluster_no', y='Recency', palette='rocket', orient= True)
    st.pyplot()
    
    test = RFM_final_df
    test = test.reset_index()
    test['R'] = test['R'].astype(int)
    test['F'] = test['F'].astype(int)
    test['M'] = test['M'].astype(int)

    test = test.groupby('cluster_no')['R', 'F','M', 'sum_val'].mean().reset_index()
    fig.set_size_inches(10, 16)
    sns.barplot(data=test,x='cluster_no', y='R', palette='rocket', orient= True)
    st.pyplot()
    
    test = RFM_final_df

    test = test.reset_index()
    test['R'] = test['R'].astype(int)
    test['F'] = test['F'].astype(int)
    test['M'] = test['M'].astype(int)

    test = test.groupby('cluster_no')['R', 'F','M', 'sum_val'].mean().reset_index()
    fig.set_size_inches(10, 16)
    sns.barplot(data=test,x='cluster_no', y='F', palette='rocket', orient= True)
    st.pyplot()
    
    test = RFM_final_df
    st.write(RFM_final_df.max())
    test = test.reset_index()
    test['R'] = test['R'].astype(int)
    test['F'] = test['F'].astype(int)
    test['M'] = test['M'].astype(int)

    test = test.groupby('cluster_no')['R', 'F','M', 'sum_val'].mean().reset_index()
    fig.set_size_inches(10, 16)
    sns.barplot(data=test,x='cluster_no', y='M', palette='rocket', orient= True)
    st.pyplot()
    
elif add_selectbox == 'K-Means Clustering and Validation':
    st.write('hello1')
    
elif add_selectbox == 'Market Basket Analysis':
    st.write('Market Basket Analysis')
    new_df = clean_data
    
    st.write('Define functions and variables')
    
    quarter = {
            'Q1': [date(2011,1,1), date(2011,3,31)],
            'Q2': [date(2011,4,1), date(2011,6,30)],
            'Q3': [date(2011,7,1), date(2011,9,30)],
            'Q4': [date(2011,10,1), date(2011,12,31)],
            'Q4_2010': [date(2010,10,1), date(2010,12,31)],
          }

    seasons = {
                'winter': [date(2010,12,1),date(2011,2,28)],
                'spring': [date(2011,3,1), date(2011,5,31)],
                'summer': [date(2011,6,1), date(2011,8,31)],
                'autumn': [date(2011,9,1), date(2011,11,30)],
              }

    def set_quarter(invoice_date):
        if(invoice_date >= quarter['Q1'][0] and invoice_date <= quarter['Q1'][1]):
            return 'Q1'
        elif(invoice_date >= quarter['Q2'][0] and invoice_date <= quarter['Q2'][1]):
            return 'Q2'
        elif(invoice_date >= quarter['Q3'][0] and invoice_date <= quarter['Q3'][1]):
            return 'Q3'
        elif((invoice_date >= quarter['Q4'][0] and invoice_date <= quarter['Q4'][1]) or             (invoice_date >= quarter['Q4_2010'][0] and invoice_date <= quarter['Q4_2010'][1])):
            return 'Q4'

    def set_season(invoice_date):
        if(invoice_date >= seasons['spring'][0] and invoice_date <= seasons['spring'][1]):
            return 'spring'
        elif(invoice_date >= seasons['summer'][0] and invoice_date <= seasons['summer'][1]):
            return 'summer'
        elif(invoice_date >= seasons['autumn'][0] and invoice_date <= seasons['autumn'][1]):
            return 'autumn'
        elif(invoice_date >= seasons['winter'][0] and invoice_date <= seasons['winter'][1]):
            return 'winter'
        
    new_df['InvoiceDate'] = pd.to_datetime(new_df.InvoiceDate) # Convert invoicedate to datetime
    new_df['Region'] = np.where(new_df['Country'].isin(['United Kingdom']), 'UK', 'Others') # Add region column
    new_df['quarter'] = new_df['InvoiceDate'].map(set_quarter)
    new_df['season'] = new_df['InvoiceDate'].map(set_season)
    st.write(new_df.head().astype('object'))
    st.write('Filtering out 9 extra days from December 2011')
    new_df = new_df[(new_df['InvoiceDate'] >= '2010-12-1 00:00:00') & (new_df['InvoiceDate'] < '2011-12-1 00:00:00')]
    st.write(new_df['InvoiceDate'].min(), new_df['InvoiceDate'].max())
    
    import re

    pattern = re.compile(r'^.*?BAG.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'BAG', new_df['Description'])

    pattern = re.compile(r'^.*?WRAP.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'WRAP', new_df['description_category'])

    pattern = re.compile(r'^.*?CASES.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'CASES', new_df['description_category'])

    pattern = re.compile(r'^.*?T-LIGHT.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'T-LIGHT', new_df['description_category'])

    pattern = re.compile(r'^.*?BOTTLE.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'BOTTLE', new_df['description_category'])

    pattern = re.compile(r'^.*?BUNTING.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'BUNTING', new_df['description_category'])

    pattern = re.compile(r'^.*?CLOCK.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'CLOCK', new_df['description_category'])

    pattern = re.compile(r'^.*?HAND WARMER.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'HAND WARMER', new_df['description_category'])

    pattern = re.compile(r'^.*?CHALKBOARD.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'CHALKBOARD', new_df['description_category'])

    pattern = re.compile(r'^.*?DOILY.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'DOILY', new_df['description_category'])

    pattern = re.compile(r'^.*?CAKE.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'CAKE', new_df['description_category'])

    pattern = re.compile(r'^.*?JAR.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'JAR', new_df['description_category'])

    pattern = re.compile(r'^.*?ORNAMENT.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'ORNAMENT', new_df['description_category'])

    pattern = re.compile(r'^.*?TISSUE.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'TISSUE', new_df['description_category'])

    pattern = re.compile(r'^.*?SAUCER.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'SAUCER', new_df['description_category'])

    pattern = re.compile(r'^.*?CANDLE.*?$')
    list_of_matches = [x for x in new_df['Description'] if pattern.match(x)]
    new_df['description_category'] = np.where(new_df['Description'].isin(list_of_matches), 'CANDLE', new_df['description_category'])

    st.write(new_df.head(5).astype('object'))
    
    st.write('No of unique transactions')
    total_transactions = new_df['InvoiceNo'].nunique()
    total_transactions
    
    st.write('Check for product presence in every transaction/invoice')
    items = list(new_df['description_category'].unique())
    grouped = new_df.groupby('InvoiceNo')
    transaction_level = grouped.aggregate(lambda x: tuple(x)).reset_index()[['InvoiceNo','description_category']]
    transaction_dict = {item:0 for item in items}
    output_dict = dict()
    temp = dict()
    for rec in transaction_level.to_dict('records'):
        invoice_num = rec['InvoiceNo']
        items_list = rec['description_category']
        transaction_dict = {item:0 for item in items}
        transaction_dict.update({item:1 for item in items if item in items_list})
        temp.update({invoice_num:transaction_dict})

    new = [v for k,v in temp.items()]
    transaction_df = pd.DataFrame(new)
    
    transaction_df_T = transaction_df.T
    transaction_df_T['sum'] = transaction_df_T.sum(axis=1)
    transaction_df_T = transaction_df_T.sort_values(by=['sum'], ascending=False)
    transaction_df_T_copy = transaction_df_T.copy()
    transaction_df_T_20 = transaction_df_T[:10]
    transaction_df_T_20_no_drop = transaction_df_T_20.copy()
    transaction_df_T_20 = transaction_df_T_20.drop(['sum'], axis=1)
    trans = transaction_df_T_20.T
    transaction_df_T_20_no_drop['share'] = transaction_df_T_20_no_drop['sum']/total_transactions
    trans = trans.sample(n=500, random_state=42)

    st.write(transaction_df_T_20_no_drop.head().astype('object'))
    sns.barplot(y = transaction_df_T_20_no_drop.index.values, x = transaction_df_T_20_no_drop['sum'].values, color = 'red')
    # sns.barplot(y = transaction_df_T_20_no_drop.index.values, x = transaction_df_T_20_no_drop['share'].values, color = 'red')
    plt.title('Top 10 most bought products')
    plt.xlabel('Transaction Count')
    plt.ylabel('Product Name')
    plt.show()
    st.pyplot()
    
    
    new_df2 = new_df.copy()
    new_df2 = new_df2[new_df2['description_category'].isin(['BAG', 'CAKE' 'T-LIGHT', 'BUNTING', 'CANDLE', 'JAR', 'BOTTLE', 'DOILY', 'WRAP', 'CLOCK'])]
    st.write(new_df2.head().astype('object')) 
    
    frequent_itemsets_ap = apriori(trans, min_support=0.01, use_colnames=True)
    frequent_itemsets_fp = fpgrowth(trans, min_support=0.01, use_colnames=True)

    rules_ap = association_rules(frequent_itemsets_ap, metric="confidence", min_threshold=0.001)
    rules_fp = association_rules(frequent_itemsets_fp, metric="confidence", min_threshold=0.001)
    
    tmp = rules_ap             [['antecedents', 'consequents', 'confidence', 'lift']].sort_values(by = ['lift', 'confidence'], axis = 0, ascending = False)
    st.write(tmp.head().astype('object'))
    
    st.write('Implementing Market Basket Analysis per quarter')
    
    df_q4 = new_df[new_df['quarter'] == 'Q4']

    items = list(df_q4['description_category'].unique())
    grouped = df_q4.groupby('InvoiceNo')
    transaction_level = grouped.aggregate(lambda x: tuple(x)).reset_index()[['InvoiceNo','description_category']]
    transaction_dict = {item:0 for item in items}
    output_dict = dict()
    temp = dict()
    for rec in transaction_level.to_dict('records'):
        invoice_num = rec['InvoiceNo']
        items_list = rec['description_category']
        transaction_dict = {item:0 for item in items}
        transaction_dict.update({item:1 for item in items if item in items_list})
        temp.update({invoice_num:transaction_dict})

    new = [v for k,v in temp.items()]
    transaction_df = pd.DataFrame(new)

    transaction_df_T = transaction_df.T
    transaction_df_T['sum'] = transaction_df_T.sum(axis=1)
    transaction_df_T = transaction_df_T.sort_values(by=['sum'], ascending=False)
    transaction_df_T_copy = transaction_df_T.copy()
    transaction_df_T_20 = transaction_df_T[:10]
    transaction_df_T_20_no_drop = transaction_df_T_20.copy()
    transaction_df_T_20 = transaction_df_T_20.drop(['sum'], axis=1)
    trans = transaction_df_T_20.T
    transaction_df_T_20_no_drop['share'] = transaction_df_T_20_no_drop['sum']/total_transactions
    trans = trans.sample(n=500, random_state=42)
    
    sns.barplot(y = transaction_df_T_20_no_drop.index.values, x = transaction_df_T_20_no_drop['sum'].values, color = 'red')
    # sns.barplot(y = transaction_df_T_20_no_drop.index.values, x = transaction_df_T_20_no_drop['share'].values, color = 'red')
    plt.title('Top 10 most bought products for Q4')
    plt.xlabel('Transaction Count')
    plt.ylabel('Product Name')
    plt.show()
    
    st.pyplot()
    
    df_q4_2 = df_q4.copy()
    df_q4_2 = df_q4_2[df_q4_2['description_category'].isin(['BAG', 'CAKE' 'T-LIGHT', 'BUNTING', 'CANDLE', 'JAR', 'BOTTLE', 'DOILY', 'WRAP', 'CLOCK'])]
    df_q4_2.head()
    
    frequent_itemsets_ap = apriori(trans, min_support=0.01, use_colnames=True)
    frequent_itemsets_fp = fpgrowth(trans, min_support=0.01, use_colnames=True)

    rules_ap = association_rules(frequent_itemsets_ap, metric="confidence", min_threshold=0.001)
    rules_fp = association_rules(frequent_itemsets_fp, metric="confidence", min_threshold=0.001)
    
    tmp = rules_ap             [['antecedents', 'consequents', 'confidence', 'lift']].sort_values(by = ['lift', 'confidence'], axis = 0, ascending = False)
    # tmp['rule'] = (str(tmp['antecedents']) + ' + ' + str(tmp['consequents']))[4:]
    tmp

else:
    get_contributors()

