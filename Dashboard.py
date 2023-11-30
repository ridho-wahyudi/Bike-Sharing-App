import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_style("whitegrid")

def create_daily_rents_df(df):
    daily_rents_df = df.resample(rule='D', on='dteday').agg({
        "weekday": "median",
        "casual": "sum",
        "registered": "sum",
        "cnt_daily": "mean"
    })
    daily_rents_df = daily_rents_df.reset_index()
    daily_rents_df.rename(columns={
        "dteday": "Date",
        "weekday": "Day",
        "cnt_daily": "Daily_Users"
    }, inplace=True)
    
    return daily_rents_df

def create_byhour_df(df):
    byhour_df = df.groupby("hr").cnt_hourly.mean().sort_values(ascending=False).reset_index()
    return byhour_df

def create_byseason_df(df):
    byseason_df = df.groupby("season")["cnt_daily"].mean().sort_values(ascending=False).reset_index()
    season_name = [[1,"Spring"], [2,"Summer"], [3,"Fall"], [4,"Winter"]]
    season_df = pd.DataFrame(season_name, columns=["number", "names"])
    byseason_df.season = byseason_df.season.map(dict(zip(season_df.number,season_df.names)))
    return byseason_df

def create_byweather_df(df):
    byweather_df = df.groupby("weathersit")["cnt_daily"].mean().sort_values(ascending=False).reset_index()
    weather_name = [[1,"Clear"], [2,"Mist"], [3,"Light Rain"], [4,"Heavy Rain/Snow"]]
    weather_df = pd.DataFrame(weather_name, columns=["number", "names"])
    byweather_df.weathersit = byweather_df.weathersit.map(dict(zip(weather_df.number,weather_df.names)))
    return byweather_df

def create_byholiday_df(df):
    byholiday_df = df.groupby("workingday").cnt_daily.mean().sort_values(ascending=False).reset_index()
    holiday_innit = [[1,"Workingday"], [0,"Holiday"]]
    holiday_df = pd.DataFrame(holiday_innit, columns=["number", "names"])
    byholiday_df.workingday = byholiday_df.workingday.map(dict(zip(holiday_df.number,holiday_df.names)))
    return byholiday_df


bike_rent_df = pd.read_csv("main_data.csv")
bike_rent_df['dteday'] = pd.to_datetime(bike_rent_df['dteday'])

min_date = bike_rent_df["dteday"].min()
max_date = bike_rent_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://cdn1.iconfinder.com/data/icons/bike-hire/64/RENTAL-bicycle-cycling-transportation-1024.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    

main_df = bike_rent_df[(bike_rent_df["dteday"] >= str(start_date)) & 
                (bike_rent_df["dteday"] <= str(end_date))]



daily_rents_df = create_daily_rents_df(main_df)
rents_byhour_df = create_byhour_df(main_df)
rents_byseason_df = create_byseason_df(bike_rent_df)
rents_byweather_df = create_byweather_df(main_df)
rents_byholiday_df = create_byholiday_df(main_df)


st.header('Bike Renting Dashboard')

st.subheader('Total Rents by Date')
 
col1, col2, col3 = st.columns([1,1,1])
 
with col1:
    date = daily_rents_df.Date.nunique()
    st.metric("Total Days", value=date)
 
with col2:
    total_renters = int(daily_rents_df.Daily_Users.sum())
    st.metric("Total Rents", value=total_renters)
    
with col3:
    option= st.selectbox("View Rents by:", ["Casual Users", "Registered Users", "All Users"])
    
if option == "Casual Users":
    fig, ax = plt.subplots(figsize=(35, 15))
    ax.plot(
        daily_rents_df["Date"],
        daily_rents_df["casual"],
        marker='o', 
        linewidth=1.5,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=30)
    ax.tick_params(axis='x', labelsize=30)
    st.pyplot(fig)
elif option == "Registered Users":
    fig, ax = plt.subplots(figsize=(35, 15))
    ax.plot(
        daily_rents_df["Date"],
        daily_rents_df["registered"],
        marker='o', 
        linewidth=1.5,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=30)
    ax.tick_params(axis='x', labelsize=30)
    st.pyplot(fig)
else:
    fig, ax = plt.subplots(figsize=(35, 15))
    ax.plot(
        daily_rents_df["Date"],
        daily_rents_df["Daily_Users"],
        marker='o', 
        linewidth=1.5,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=30)
    ax.tick_params(axis='x', labelsize=30)
    st.pyplot(fig)



st.subheader('Average Daily Rents by Hour')
fig, ax = plt.subplots(figsize=(16, 4))

sns.barplot(
    x='hr', 
    y='cnt_hourly', 
    data=rents_byhour_df, 
)
ax.set_ylabel(None)
ax.set_xlabel("Hour", fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


st.subheader("Average Rents by Weathers and Seasons")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="cnt_daily", 
        x="weathersit",
        data=rents_byweather_df,
        palette=colors
    )
    ax.set_title("Rents by Weathers", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="cnt_daily", 
        x="season",
        data=rents_byseason_df,
        palette=colors
    )
    ax.set_title("Rents by Seasons", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)
    

st.subheader("Average Rents by Work/Holiday")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="cnt_daily", 
        x="workingday",
        data=rents_byholiday_df,
        palette=colors
    )
    ax.set_title("Rents by Holiday", loc="center", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)
    
st.caption('Copyright (c) Ridhow 2023')
