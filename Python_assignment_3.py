# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 22:48:19 2023

@author: kawka
"""

import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(layout='wide')

file_athletes = pd.read_csv('athlete_events.csv')
file_noc = pd.read_csv('noc_regions.csv')
df = pd.merge(file_athletes, file_noc, left_on=('NOC'), right_on=('NOC'), how='outer')


st.title(":chart_with_upwards_trend: Olympian History Dashboard")
st.subheader('Created by Kawkab Shakeel')
st.markdown("------")

#cleaning the data
#replacing all the nan
df['Age']=df.Age.fillna(df.Age.mean())
df['Weight']=df.Weight.fillna(df.Weight.mean())
df['Height']=df.Height.fillna(df.Height.mean())
#removing the duplicates
df = df.drop_duplicates( keep='last')


#Creating drop down list of countries
countries = df['region'].unique()
selected_country = st.selectbox('Select Country :earth_africa:', countries)
subset_country = df[df['region']== selected_country]

#metrics count
participants = subset_country['ID'].nunique()
gold_medals = subset_country[subset_country['Medal']=='Gold']['ID'].count()
silver_medals = subset_country[subset_country['Medal']=='Silver']['ID'].count()
bronze_medals = subset_country[subset_country['Medal']=='Bronze']['ID'].count()
total_medals = gold_medals + silver_medals + bronze_medals
 

st.header('Olympics Information - {}'.format(selected_country))

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('No. of Participants', participants)
col3.metric('Gold Medals', gold_medals)
col4.metric('Silver Medals', silver_medals)
col5.metric('Bronze Medals', bronze_medals)
col2.metric('Total Medals', total_medals)
st.markdown("--------")


with st.container():
    left, middle, right = st.columns(3) 
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use('ggplot')

#Medal type count for each country
medal_count = subset_country.groupby('Medal')['ID'].count().sort_values(ascending=False)
plt.bar(x= medal_count.index, height = medal_count.values)
plt.title('Total Medals Secured')
plt.xlabel('Medal Type')
plt.ylabel('Athletes')
left.pyplot()

#Total count of medals season wise
season_medal_count = subset_country.groupby('Season')['ID'].count().sort_values(ascending =False)
plt.bar(x = season_medal_count.index, height = season_medal_count.values)
plt.title('Medals count by season')
plt.xlabel('Seasons')
plt.ylabel('No.of Medals')
right.pyplot()

#Medals secured by athletes over the years
sns.lineplot(x = subset_country['Year'], y = subset_country['Medal'])
plt.title('Medals over Years')
middle.pyplot()

#Histogram of Medals by Grouped data by Age
medal_age_count = subset_country.groupby('Age')['Medal'].count().sort_values(ascending=False)
plt.hist((medal_age_count).values, bins = 10)
plt.xlabel('Medal Distribution')
plt.ylabel('Grouped Data - Age')
right.pyplot()

#pie chart summary of medals by gender
gender_medal_count = subset_country.groupby('Sex')['Medal'].count()
fig = plt.pie(gender_medal_count, labels=gender_medal_count.index, autopct='%.2f')
left.pyplot()

#top 5 sports with highest no of medals
middle.write('Sports with highest count of medals - Top 5')
famous_sports= subset_country.groupby('Sport', as_index= False)['Medal'].count()
top_five = famous_sports.sort_values(by='Medal', ascending=False).head(5)
middle.dataframe(top_five, use_container_width = True)

