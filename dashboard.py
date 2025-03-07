import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='darkgrid')

# Memuat data
all_df = pd.read_csv("main_data.csv")

# Sidebar untuk judul dan logo
st.sidebar.markdown("<h1 style='text-align: center; font-size: 50px;'>🚴</h1>", unsafe_allow_html=True)
st.sidebar.title("Bike Rentals Dashboard")

# Sidebar untuk filter tahun
year_options = all_df['yr'].unique()
selected_years = st.sidebar.multiselect("Select years", year_options, default=year_options)

# Filter data berdasarkan tahun yang dipilih
year_df = all_df[all_df['yr'].isin(selected_years)]

# Header untuk statistik tahun yang dipilih
st.header("Statistics for the Selected Years")

# Menghitung total rentals untuk tahun yang dipilih
total_casual = year_df['casual'].sum()
total_registered = year_df['registered'].sum()
total_rentals = year_df['cnt'].sum()

# Membuat tiga kolom untuk tahun yang dipilih
col1, col2, col3 = st.columns(3)

# Menampilkan statistik dalam kolom
with col1:
    st.metric(label="Casual Rentals", value=total_casual)
with col2:
    st.metric(label="Registered Rentals", value=total_registered)
with col3:
    st.metric(label="Total Rentals", value=total_rentals)

# Groupby data berdasarkan tahun dan bulan
monthly_trend = year_df.groupby(['yr', 'mnth']).agg({'cnt': 'sum'}).reset_index()

# Plot tren bulanan
fig, ax = plt.subplots(figsize=(10, 6))
palette = sns.color_palette("husl", len(selected_years)) 
sns.lineplot(data=monthly_trend, x='mnth', y='cnt', hue='yr', ax=ax, marker='o', palette=palette)
ax.set_title('Monthly Bike Rentals Trend', fontsize=16)
ax.set_xlabel('Month', fontsize=14)
ax.set_ylabel('Total Rentals', fontsize=14)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=12)
ax.legend(title='Year', fontsize=12)
ax.grid(True)

st.pyplot(fig)

# Header untuk statistik hari yang dipilih
st.header("Statistics for the Selected Date")

# Sidebar untuk memilih tanggal
selected_date = st.sidebar.date_input("Select a date", pd.to_datetime("2011-01-01"))

# Filter data berdasarkan tanggal yang dipilih
selected_date_str = selected_date.strftime('%Y-%m-%d')
filtered_df_selected = all_df[all_df['dteday'] == selected_date_str]

# Menghitung total rentals untuk tanggal yang dipilih
total_casual_date = filtered_df_selected['casual'].sum()
total_registered_date = filtered_df_selected['registered'].sum()
total_rentals_date = filtered_df_selected['cnt'].sum()

# Membuat tiga kolom untuk tanggal yang dipilih
col1, col2, col3 = st.columns(3)

# Menampilkan statistik dalam kolom
with col1:
    st.metric(label="Casual Rentals", value=total_casual_date)
with col2:
    st.metric(label="Registered Rentals", value=total_registered_date)
with col3:
    st.metric(label="Total Rentals", value=total_rentals_date)

# Filter data berdasarkan tanggal sebelumnya
previous_date = selected_date - pd.Timedelta(days=1)
previous_date_str = previous_date.strftime('%Y-%m-%d')
filtered_df_previous = all_df[all_df['dteday'] == previous_date_str]

# Membuat dua kolom untuk plot
col1, col2 = st.columns(2)

# Plot the line chart pada kolom pertama
with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=filtered_df_selected, x='hr', y='casual', ax=ax, label='Casual', marker='o')
    sns.lineplot(data=filtered_df_selected, x='hr', y='registered', ax=ax, label='Registered', marker='o')
    ax.set_title(f'Hourly Rentals on {selected_date.strftime("%Y-%m-%d")}', fontsize=16)
    ax.set_xlabel('Hour', fontsize=14)
    ax.set_ylabel('Number of Rentals', fontsize=14)
    ax.set_xticks(range(24))  
    ax.set_xticklabels(range(24), fontsize=12)  
    ax.legend(fontsize=12)
    ax.grid(True)
    st.pyplot(fig)

# Plot the bar chart pada kolom kedua
with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=filtered_df_selected, x='hr', y='cnt', ax=ax, label=f'Total Rentals on {selected_date_str}', marker='o')
    sns.lineplot(data=filtered_df_previous, x='hr', y='cnt', ax=ax, label=f'Total Rentals on {previous_date_str}', marker='o')
    ax.set_title(f'Hourly Rentals Comparison on {selected_date_str} and {previous_date_str}', fontsize=16)
    ax.set_xlabel('Hour', fontsize=14)
    ax.set_ylabel('Total Rentals', fontsize=14)
    ax.set_xticks(range(24))  
    ax.set_xticklabels(range(24), fontsize=12)  
    ax.legend(fontsize=12)
    ax.grid(True)
    st.pyplot(fig)

# Header untuk rata-rata rentals per hari
st.header("Average Rentals per Day of the Week")

# Menghitung rata-rata rentals per hari
average_rentals = all_df.groupby('weekday').agg({'casual': 'sum', 'registered': 'sum'}).reset_index()

# Menghitung jumlah hari unik untuk setiap hari
unique_days = all_df.groupby('weekday')['dteday'].nunique().reset_index()
unique_days.columns = ['weekday', 'unique_days']

# Menggabungkan data rata-rata rentals dan jumlah hari unik
average_rentals = pd.merge(average_rentals, unique_days, on='weekday')

# Menghitung rata-rata rentals per hari
average_rentals['casual'] = average_rentals['casual'] / average_rentals['unique_days']
average_rentals['registered'] = average_rentals['registered'] / average_rentals['unique_days']

# Mengurutkan data berdasarkan hari
average_rentals['weekday'] = pd.Categorical(average_rentals['weekday'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)

# Plot bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
bar1 = ax.bar(average_rentals['weekday'], average_rentals['casual'], bar_width, label='Casual')
bar2 = ax.bar(average_rentals['weekday'], average_rentals['registered'], bar_width, bottom=average_rentals['casual'], label='Registered')
ax.set_title('Average Rentals per Day of the Week', fontsize=16)
ax.set_xlabel('Day of the Week', fontsize=14)
ax.set_ylabel('Average Rentals', fontsize=14)
ax.legend(title='Rental Type', fontsize=12)
ax.grid(True)

st.pyplot(fig)
