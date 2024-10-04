import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import warnings
from babel.numbers import format_currency
sns.set(style='dark')

st.write(
    """
    # Bike Sharing Dashboard
    Bike Sharing Data Analysis Project
    """
)

with st.sidebar:
    st.image('./assets/Sumire Persona 5.jpg')
    st.write(
        """
            # Akmal Nuur Fauzan | ML - 47
        """
    )


dfd = pd.read_csv('./data/day.csv')

dfd_new = dfd.copy()
dfd_new['dteday'] = pd.to_datetime(dfd_new['dteday'])

dfh = pd.read_csv('./data/hour.csv')

dfh_new = dfh.copy()
dfh_new['dteday'] = pd.to_datetime(dfh_new['dteday'])


# Renaming all the column
dfd.rename(columns={'yr':'year',
                    'mnth':'month',
                    'hum':'humidity',
                    'cnt':'count',
                    'dteday':'Datetime'
                    }, inplace=True)

# Capitalize each column name
dfd_new.columns = dfd.columns.str.title()

# Change the 'Datetime' data type from object to datetime
dfd['Datetime'] = pd.to_datetime(dfd_new['Datetime'])

# dfd_new['dteday'] = pd.to_datetime(dfd_new['dteday'])
# Grouping the data by Registered users and calculating RFM metrics
rfm_df = dfd_new.groupby(by='Registered', as_index=False).agg({
    'Datetime': 'max',  # take last rent date
    'Instant': 'nunique',  # calculate the number of rent
    'Count': 'sum'       # calculate the amount of revenue generated
})

# calculate when the customer last made a transaction (day)
rfm_df.columns = ['Registered', 'max_rent_timestamp', 'Frequency', 'Monetary']
rfm_df['max_rent_timestamp'] = rfm_df['max_rent_timestamp'].dt.date
recent_date = dfd_new['Datetime'].dt.date.max()
rfm_df['Recency'] = rfm_df['max_rent_timestamp'].apply(lambda x: (recent_date - x).days)

rfm_df.drop('max_rent_timestamp', axis=1, inplace=True)

warnings.simplefilter(action='ignore', category=FutureWarning)
# Map seasons to their names
dfd_new['Season'] = dfd_new['Season'].map({
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
})

# Create a box plot for rentals across seasons
st.title('Bike Rentals Analysis')

# Box plot for rentals across seasons
st.subheader('Bike Rentals Across Different Seasons')
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.boxplot(x='Season', y='Count', data=dfd_new, palette='Set3', ax=ax1)
ax1.set_title('Bike Rentals Across Different Seasons', fontsize=16)
ax1.set_xlabel('Season', fontsize=12)
ax1.set_ylabel('Bike Rentals Count', fontsize=12)
st.pyplot(fig1)  # Display the plot in Streamlit

# Box plot for rentals across months
st.subheader('Bike Rentals Across Different Months')
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.boxplot(x='Month', y='Count', data=dfd_new, palette='Set2', ax=ax2)
ax2.set_title('Bike Rentals Across Different Months', fontsize=16)
ax2.set_xlabel('Month', fontsize=12)
ax2.set_ylabel('Bike Rentals Count', fontsize=12)
st.pyplot(fig2)  # Display the plot in Streamlit


# Group data by holiday and calculate the average number of bike rentals
df_grouped = dfd_new.groupby(by='Holiday')['Count'].mean().reset_index()

# Map holiday values for better readability
df_grouped['day_type'] = df_grouped['Holiday'].map({
    0: 'Working Day',
    1: 'Holiday'
})

# Create a bar plot
fig = px.bar(
    df_grouped,
    x='day_type',
    y='Count',
    title='Average Bike Rentals on Holidays vs. Working Days',
    labels={'Count': 'Average Bike Rentals', 'day_type': 'Day Type'},
    color='Holiday',
    color_discrete_map={'0': '#636EFA', '1': '#EF553B'},  # Note that colors are based on the original values
)

# Update layout
fig.update_layout(
    width=800,
    height=500,
    xaxis_title='Day Type',
    yaxis_title='Average Bike Rentals',
    showlegend=False,
)

# Create title for the Streamlit app
st.title('Average Bike Rentals Analysis')

# Display the bar plot in the Streamlit app
st.plotly_chart(fig)

st.title('Visualizing Registered and Casual Users Over Time')

fig = go.Figure()

fig.add_trace(go.Scatter(x=dfd_new['Datetime'], y=dfd_new['Registered'], mode='lines', name='Registered', marker_color='#636EFA'))

fig.add_trace(go.Scatter(x=dfd_new['Datetime'], y=dfd_new['Casual'], mode='lines', name='Casual', marker_color='#EF553B'))

fig.update_layout(
    width=1000,
    height=600,
    title='Registered and Casual Users Over Time',
    xaxis_title='Datetime',
    yaxis_title='Count',
    hovermode='x unified',  # Display hover for both traces simultaneously
    xaxis=dict(
        tickformat='%Y-%m-%d',  # Date format for better readability
        rangeslider_visible=True  # Enable range slider
    )
)

st.plotly_chart(fig)


st.subheader('Best Customer Based on RFM Parameters')

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.Recency.mean(), 1)
    st.metric('Average Recency (days)', value=avg_recency)
    
with col2:
    avg_frequency = round(rfm_df.Frequency.mean(), 2)
    st.metric('Average Frequency', value=avg_frequency)
    
with col3:
    avg_frequency = format_currency(rfm_df.Monetary.mean(), 'AUD', locale='es_Co')
    st.metric('Average Monetary', value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
 
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
 
sns.barplot(y="Recency", x="Registered", data=rfm_df.sort_values(by="Recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel('Made Purchase')
ax[0].set_xlabel('Users Registered')
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)
 
sns.barplot(y="Frequency", x="Registered", data=rfm_df.sort_values(by="Frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel('Make purchase')
ax[1].set_xlabel('Users Registered')
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)
 
sns.barplot(y="Monetary", x="Registered", data=rfm_df.sort_values(by="Monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel('Spend Money')
ax[2].set_xlabel('Users Registered')
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
st.caption('Copyright©️ Akmal Nuur Fauzan 2024')
