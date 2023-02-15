# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import seaborn as sns
st.set_page_config(layout="wide")

path = r'C:\Users\kawka\Desktop\Final Assignment\athlete_events.csv'
df = pd.read_csv(path)
#dn = pd.read_csv("noc_regions.csv")
#df=pd.merge(de,dn)

st.title(":chart_with_upwards_trend: Olympian History Dashboard")
st.subheader('Created by Kawkab Shakeel')
st.markdown("------")

#cleaning the data
#not replacing the duplicates in ID because same olympian with same ID participated different years
#replacing all the nan
df['Age'] = df.Age.fillna(df.Age.mean())
df['Height'] = df.Height.fillna(df.Height.mean())
df['Weight'] = df.Weight.fillna(df.Weight.mean())


#creating drop down list of countries
all_countries = sorted(df['NOC'].unique())
selected_country = st.selectbox('Select Country :earth_africa:', all_countries)
subset_country  = df[df['NOC']== selected_country]

#unique count because there were duplicates in ID because same person(ID) participated multiple times
participants = subset_country['ID'].nunique()
gold_medals = subset_country[subset_country['Medal']=='Gold']['ID'].count()
silver_medals = subset_country[subset_country['Medal']=='Silver']['ID'].count()
bronze_medals = subset_country[subset_country['Medal']=='Bronze']['ID'].count()
total_medals = gold_medals + silver_medals + bronze_medals

st.header('Olympics Information - {}'.format(selected_country))

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('No. of Participants', participants)
col2.metric('Total Medals', total_medals)
col3.metric('Gold Medals', gold_medals)
col4.metric('Silver Medals', silver_medals)
col5.metric('Bronze Medals', bronze_medals)
st.markdown("--------")

with st.container():
    left, middle, right = st.columns(3) 
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]

#Medal type count for each country
medal_count = subset_country.groupby('Medal')['ID'].count().sort_values(ascending=False)
plt.bar(x= medal_count.index, height = medal_count.values)
plt.title('Total Medals Secured')
plt.xlabel('Medal Type')
plt.ylabel('Athletes')
left.pyplot()

#Total count of medals season wise
season_medal_count = subset_country.groupby('Season')['Medal'].count().sort_values(ascending =False)
plt.bar(x = season_medal_count.index, height = season_medal_count.values)
plt.title('Medals count by season')
plt.xlabel('Seasons')
plt.ylabel('No.of Medals')
plt.grid()
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










