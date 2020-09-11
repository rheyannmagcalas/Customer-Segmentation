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

# In[27]:


st.title('Customer Segmentation')


# In[25]:


data_load_state = st.text('Loading data...')


@st.cache(allow_output_mutation=True)  
def get_data():
#     raw_data = pd.read_excel('../C_Online_Retail.xlsx')
#     clean_data = pd.read_csv('..//H_new_df.csv')
#     remove_null = pd.read_csv('..//NullCustomer.csv')
    raw_data = pd.read_excel('https://eskwelabs.s3.amazonaws.com/C_Online_Retail.xlsx')
    clean_data = pd.read_csv('https://eskwelabs.s3.amazonaws.com/H_new_df.csv')
    remove_null = pd.read_csv('https://eskwelabs.s3.amazonaws.com/NullCustomer.csv')
    return raw_data, clean_data, remove_null


# In[ ]:


def get_contributors():
    st.write('Contributors')
    df = pd.DataFrame([['Albert Yumol'], ['Elissa Mae Cabal'],  ['Emerson Chua'],  ['Gabriel Ong'], 
                       ['Franz Taborlupa'], ['Janina Reyes'], ['Jonas Beltran'], ['John Barrion'], 
                       ['Joleil Villena'], ['Justine Guino'], ['Kemp Po'], ['Kenrick Nocom'],  ['Paul Allen Chavit'], 
                       ['Raileen Mae Ferrer'], ['Robert Banadera'], ['Ruth Ann Cabria'], ['William Raymond Revilla']],
                     columns=['Name'])
    st.table(df)  


# In[66]:


from PIL import Image
data_load_state.text('')

image = Image.open('eskwelabs.png')
st.sidebar.image(image, caption='', use_column_width=True)
st.sidebar.markdown("<h1 style='text-align: center;margin-bottom:50px'>DS Cohort V</h1>", unsafe_allow_html=True)

raw_data, clean_data, remove_null = get_data()

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
    
    custom_color = ['#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980', 
                   '#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980', 
                   '#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980', 
                   '#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980', 
                   '#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980']
    
    
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
    clean_column_values = list(remove_null.columns)
    clean_column_null_count = list(remove_null.count())
    
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
    
    #st.table(df_uk.groupby('hour')['InvoiceNo'].nunique())
    #st.table(df_nonuk.groupby('hour')['InvoiceNo'].nunique())
    #st.write(clean_data.shape)
    
#     clean_data['Hour'] = clean_data['InvoiceDate'].dt.hour
#     clean_data['Day'] = clean_data['InvoiceDate'].dt.day
#     clean_data['Week'] = clean_data['InvoiceDate'].dt.weekday
#     clean_data['Month'] = clean_data['InvoiceDate'].dt.month
    
#     df_hour = clean_data.groupby(['InvoiceNo','Hour']).count().reset_index()['Hour']
#     df_hour_values = df_hour.value_counts().sort_index()
#     df_hour_values = df_hour_values.reset_index()

    
#     custom_color = ['#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980', 
#                    '#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980', 
#                    '#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980', 
#                    '#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980', 
#                    '#140D35', '#3B0F6F', '#63197F', '#8C2980', '#140D35', '#3B0F6F', '#63197F', '#8C2980']
    
#     source1 = ColumnDataSource(data=dict(column_values=list(df_hour_values['index']), 
#                                         column_null_count=list(df_hour_values['Hour']), color=custom_color))
#     hourly_transaction = figure(x_range=(5,24), plot_height=500, plot_width=600, title='Hourly Transactions')
    
#     hourly_transaction.vbar(x='column_values', top='column_null_count', width=0.5,
#                             legend_field='column_values', color='color', source=source1)
    
#     hourly_transaction.xaxis.axis_label = 'Hour'
#     hourly_transaction.yaxis.axis_label = 'Counts'
#     hourly_transaction.xaxis.major_label_orientation = 1.2
#     st.bokeh_chart(hourly_transaction)
    
    
    
#     day_transaction = clean_data.groupby(['InvoiceNo','Day']).count().reset_index()['Day']
#     df_day_values = day_transaction.value_counts().sort_index()
    
#     source1 = ColumnDataSource(data=dict(column_values=list(df_day_values.index), 
#                                         column_null_count=list(df_day_values.values)))
#     day_transaction_plot = figure(x_range=(0,32), plot_height=600, title='Day Transactions')
    
#     day_transaction_plot.vbar(x='column_values', top='column_null_count', width=0.5,
#                             legend_field='column_values',source=source1)
    
#     day_transaction_plot.xaxis.axis_label = 'Day'
#     day_transaction_plot.yaxis.axis_label = 'Counts'
#     day_transaction_plot.xaxis.major_label_orientation = 1.2
#     day_transaction_plot.legend.visible = False
#     st.bokeh_chart(day_transaction_plot)
    
    
#     df_week = clean_data.groupby(['InvoiceNo','Week']).count().reset_index()['Week']
#     df_week_values = df_week.value_counts().sort_index()
    
#     source1 = ColumnDataSource(data=dict(column_values=list(df_week_values.index), 
#                                         column_null_count=list(df_week_values.values)))
#     day_transaction_plot = figure(x_range=(-1,8), plot_height=600, title='Weekly Transactions')
    
#     day_transaction_plot.vbar(x='column_values', top='column_null_count', width=0.5,
#                             legend_field='column_values', source=source1)
    
#     day_transaction_plot.xaxis.axis_label = 'Day'
#     day_transaction_plot.yaxis.axis_label = 'Counts'
#     day_transaction_plot.xaxis.major_label_orientation = 1.2
#     st.bokeh_chart(day_transaction_plot)
    
    
#     df_month = clean_data.groupby(['InvoiceNo','Month']).count().reset_index()['Month']
#     df_month_values = df_month.value_counts().sort_index()
    
#     source1 = ColumnDataSource(data=dict(column_values=list(df_month_values.index), 
#                                         column_null_count=list(df_month_values.values), color=custom_color))
#     day_transaction_plot = figure(x_range=(0,13), plot_height=600, title='Average Monthly Transactions')
    
#     day_transaction_plot.vbar(x='column_values', top='column_null_count', width=0.5,
#                             legend_field='column_values', color='color', source=source1)
    
#     day_transaction_plot.xaxis.axis_label = 'Month'
#     day_transaction_plot.yaxis.axis_label = 'Average Transaction'
#     day_transaction_plot.xaxis.major_label_orientation = 1.2
#     st.bokeh_chart(day_transaction_plot)
    
#     jan = clean_data[clean_data['Month'] == 1].groupby('Description')['Quantity'].sum().sort_values(ascending = False).head(10)
#     jan = jan.reset_index()
    
    
#     jan_month = list(jan['Quantity'])
#     st.write(jan_month[0])
#     source1 = ColumnDataSource(data=dict(column_values=list(jan['Description']), 
#                                         column_null_count=list(jan['Quantity'])))
#     day_transaction_plot = figure(x_range=list(jan['Description']), plot_height=600, title='Most Bought Product for JANUARY')
    
#     day_transaction_plot.vbar(x='column_values', top='column_null_count', width=0.5,
#                             legend_field='column_values', source=source1)
    
#     day_transaction_plot.xaxis.axis_label = 'Product'
#     day_transaction_plot.yaxis.axis_label = 'Average Transaction'
#     day_transaction_plot.xaxis.major_label_orientation = 1.2
#     day_transaction_plot.legend.visible = False
#     st.bokeh_chart(day_transaction_plot)
    
elif add_selectbox == 'RFM Model':
    st.subheader('RFM Model')
    st.write('\n\n1. Recency: How much time has elapsed since a customer’s last activity or transaction with the brand')
    st.write('2. Frquency: How often has a customer transacted or interacted with the brand during a particular period of time')
    st.write('3. Monetary: How much a customer has spent with the brand during a particular period of time. ')
    
elif add_selectbox == 'K-Means Clustering and Validation':
    st.write('hello1')
    
elif add_selectbox == 'Market Basket Analysis':
    st.write('hello2')

else:
    get_contributors()

