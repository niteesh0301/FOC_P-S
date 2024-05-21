# -*- coding: utf-8 -*-
"""Niteseh_kumar_Foc_ass_2 .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14WKKAQPNksIu7yVC0MKn6dgAiqqIALrr
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from geopy.distance import geodesic
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import time
from IPython.display import clear_output

# Load the dataset
df = pd.read_csv('train.csv')

# Set the random seed
np.random.seed(8659)

# Sample 100,000 rows
df = df.sample(n=100000)

df.head()

df.describe()

df.dtypes

## Droping rows with nan values
df.dropna(inplace=True)

null_data = df.isnull().sum()
print("null data counts:")
print(null_data)

df.head()

df = df[df['trip_duration'] >= 0]

df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])

df['month'] = df.pickup_datetime.dt.month

df['weekday'] = df['pickup_datetime'].dt.strftime('%A')

df['weekday_num'] = df.pickup_datetime.dt.weekday

df['pickup_hour'] = df.pickup_datetime.dt.hour

df.head()

df.dtypes

df.value_counts()

# Creating dummy variables for store_and_fwd_flag within df2 and droping the first level
df = pd.get_dummies(df, columns=['store_and_fwd_flag'], drop_first=True)

# Create a figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot a bar chart in the first subplot
sns.countplot(data=df, x='vendor_id', ax=axes[0], palette='viridis')
axes[0].set_title('Vendors (Bar Chart)')
axes[0].set_xlabel('Vendor Id')
axes[0].set_ylabel('Count')

# Plot a pie chart in the second subplot
vendor_counts = df['vendor_id'].value_counts()
axes[1].pie(vendor_counts, labels=vendor_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('viridis'))
axes[1].set_title('Vendors (Pie Chart)')

# Adjust layout
fig.tight_layout()

# Show the plots
plt.show()

# Converting 'passenger_count' to integers and then count the values
df['passenger_count'] = df['passenger_count'].astype(int)
passenger_count_counts = df['passenger_count'].value_counts()

# Seting the display format to suppress scientific notation
pd.options.display.float_format = '{:.2f}'.format

# Display the value counts
print(passenger_count_counts)

df = df[df['passenger_count'] > 0]

# Create a single figure with two subplots side by side
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 5))

# Bar plot for passenger count
sns.countplot(data=df, x='passenger_count', ax=axes[0])
axes[0].set_ylabel("Count", fontsize=15)
axes[0].set_xlabel("No. of Passengers", fontsize=15)
axes[0].set_title('Passenger Count (Bar Plot)', fontsize=20)

# Box plot for passenger count
sns.boxplot(data=df, x='passenger_count', orient='h', ax=axes[1])
axes[1].set_title('Passenger Count (Box Plot)', fontsize=20)

# Adjust layout
fig.tight_layout()

# Show the plots
plt.show()

# Replace 'df' with your actual DataFrame
plt.figure(figsize=(20, 5))
sns.boxplot(x=df['trip_duration'])
plt.title('Trip Duration Box Plot', fontsize=16)
plt.xlabel('Trip Duration', fontsize=14)
plt.show()

bin_edges = np.arange(0, df['trip_duration'].max(), 3600)

# Group and count trips based on trip duration bins
trip_counts = df['trip_duration'].groupby(pd.cut(df['trip_duration'], bin_edges)).count()

# Print the trip counts
print(trip_counts)

# Replace 'df' with your actual DataFrame
bin_labels = np.arange(1, 7200, 600)
trip_duration_counts = df['trip_duration'].groupby(pd.cut(df['trip_duration'], bin_labels)).count()

# Create a horizontal bar plot
plt.figure(figsize=(18, 5))
trip_duration_counts.plot(kind='barh')
plt.title('Trip Duration', fontsize=16)
plt.xlabel('Trip Counts', fontsize=14)
plt.ylabel('Trip Duration (seconds)', fontsize=14)
plt.show()

def clock(ax, radii, title, color):
    N = 24  # Number of hours in a day
    bottom = 2  # Bottom position for the bars

    # Create theta for 24 hours
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)

    # Width of each bin on the plot
    width = (2 * np.pi) / N

    # Create bars on the polar plot
    bars = ax.bar(theta, radii, width=width, bottom=bottom, color=color, edgecolor="#999999")

    # Set the label position to start from the top and go clockwise
    ax.set_theta_zero_location("N")  # "N" stands for North (top)
    ax.set_theta_direction(-1)  # Clockwise direction

    # Set the label ticks and format them as hours
    ax.set_xticks(theta)
    ticks = ["{}:00".format(x) for x in range(24)]
    ax.set_xticklabels(ticks)

    # Set the title of the polar plot
    ax.set_title(title)

plt.figure(figsize=(15, 15))
ax = plt.subplot(3, 3, 1, polar=True)

# Calculate the number of trips per hour and convert it to an array
radii = df['pickup_hour'].value_counts().sort_index().values

title = "Hourly trips"
clock(ax, radii, title, "#dc143c")

plt.show()

pip install folium

import folium
from folium.plugins import HeatMap
pickup_map = folium.Map(location=[df['pickup_latitude'].mean(), df['pickup_longitude'].mean()], zoom_start=12)
pickup_map.add_child(folium.plugins.HeatMap(df[['pickup_latitude', 'pickup_longitude']].values, radius=8))
pickup_map.save("pickup_Geo_map.html")
dropoff_map = folium.Map(location=[df['dropoff_latitude'].mean(), df['dropoff_longitude'].mean()], zoom_start=12)
dropoff_map.add_child(folium.plugins.HeatMap(df[['dropoff_latitude', 'dropoff_longitude']].values, radius=8))
dropoff_map.save("dropoff_Geo_map.html")
dropoff_map.save("dropoff_Geo_map.html")

# Create a figure and axes
plt.figure(figsize=(19, 5))

# Create a countplot with custom month labels
ax = sns.countplot(data=df, x='month', palette='viridis')

# Set axis labels and title
ax.set_ylabel('Trip Counts', fontsize=15)
ax.set_xlabel('Months', fontsize=15)
ax.set_title('Trips per Month', fontsize=20)

# Specify the positions and labels for the x-axis ticks
month_positions = list(range(12))
month_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Set the custom tick positions and labels for the x-axis
ax.set_xticks(month_positions)
ax.set_xticklabels(month_labels, rotation=45)

plt.show()

plt.figure(figsize=(12, 4))


group1 = df.groupby('pickup_hour')['trip_duration'].mean().reset_index()

# Create a point plot
point_plot = sns.pointplot(x='pickup_hour', y='trip_duration', data=group1, color='skyblue')

point_plot.set_ylabel('Trip Duration (seconds)', fontsize=10)
point_plot.set_xlabel('Pickup Hour', fontsize=10)
point_plot.set_title('Trip Duration per Hour', fontsize=15)

plt.show()

plt.figure(figsize=(12, 4))

# Group by weekday number and calculate the mean trip duration
group2 = df.groupby('weekday_num')['trip_duration'].mean().reset_index()

# Create a point plot
point_plot = sns.pointplot(x='weekday_num', y='trip_duration', data=group2, color='skyblue')

point_plot.set_ylabel('Trip Duration (seconds)', fontsize=10)
point_plot.set_xlabel('Weekday', fontsize=10)
point_plot.set_title('Trip Duration per Weekday', fontsize=15)

# Set x-axis labels to display the weekday names
weekday_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
point_plot.set_xticklabels(weekday_labels, rotation=45)

plt.show()

plt.figure(figsize=(12, 4))


group3 = df.groupby('month')['trip_duration'].mean().reset_index()

# Create a point plot
point_plot = sns.pointplot(x='month', y='trip_duration', data=group3, color='skyblue')

point_plot.set_ylabel('Trip Duration (seconds)', fontsize=10)
point_plot.set_xlabel('Month', fontsize=10)
point_plot.set_title('Trip Duration per Month', fontsize=15)

plt.show()

group9 = df.groupby('vendor_id')['passenger_count'].mean().reset_index()

plt.figure(figsize=(12, 4))

# Create a bar plot
bar_plot = sns.barplot(x='vendor_id', y='passenger_count', data=group9, color='skyblue')

bar_plot.set_ylabel('Passenger Count', fontsize=10)
bar_plot.set_xlabel('Vendor ID', fontsize=10)
bar_plot.set_title('Passenger Count per Vendor', fontsize=15)

plt.show()

group4 = df.groupby('vendor_id')['trip_duration'].mean().reset_index()

plt.figure(figsize=(12, 4))

# Create a bar plot
bar_plot = sns.barplot(x='vendor_id', y='trip_duration', data=group4, color='skyblue')

bar_plot.set_ylabel('Trip Duration (seconds)', fontsize=10)
bar_plot.set_xlabel('Vendor', fontsize=10)
bar_plot.set_title('Trip Duration per Vendor', fontsize=15)

plt.show()

plt.figure(figsize=(12, 4))

# Create a countplot with custom x-axis labels
count_plot = sns.countplot(data=df, x='weekday_num', palette='viridis')

count_plot.set_xlabel('Weekday', fontsize=15)
count_plot.set_ylabel('Trip Counts', fontsize=15)
count_plot.set_title('Trips per Day', fontsize=20)

# Set the x-axis labels to display weekdays
weekday_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
count_plot.set_xticklabels(weekday_labels, rotation=45)

plt.show()

from sklearn.preprocessing import LabelEncoder

# Create a LabelEncoder object
label_encoder = LabelEncoder()

# Apply label encoding to the 'vendor_id' column and overwrite it
df['vendor_id'] = label_encoder.fit_transform(df['vendor_id'])

df.dtypes

df.head()

from sklearn.preprocessing import MinMaxScaler


scaler = MinMaxScaler()
normalizing_column = ['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']
df[normalizing_column] = scaler.fit_transform(df[normalizing_column])

from sklearn.preprocessing import StandardScaler

# Create a StandardScaler object
scaler = StandardScaler()

# Define the columns to be standardized
columns_to_standardize = ['trip_duration']

# Apply standardization to the selected columns
df[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])

from scipy import stats

# Select the numerical columns for outlier detection
numerical_columns = ['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'trip_duration']

# Calculate the absolute Z-scores for each numerical column
z_scores = np.abs(stats.zscore(df[numerical_columns]))

# Define a threshold for considering data points as outliers (adjust as needed)
z_threshold = 3.0

# Find rows with outliers
outliers = (z_scores > z_threshold).any(axis=1)

# Remove rows with outliers
df_clean = df[~outliers]

# Display the cleaned DataFrame
df_clean.head()

df = df_clean

# Display the cleaned DataFrame
df.head()

df.shape

# Select only the numeric columns in your DataFrame
df2_matrix_columns = df.select_dtypes(include=['number'])
df2_matrix = df2_matrix_columns.corr()

# Creating a heatmap with a different color palette ('viridis' in this case)
plt.figure(figsize=(10, 8))
sns.heatmap(df2_matrix, annot=True, cmap='viridis', linewidths=0.7)
plt.title('Heatmap')
plt.show()

#X = df[predictors]
#y = df[target]
#y = df.iloc[:,9].values
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7294)

from sklearn.decomposition import PCA

# Fit PCA to your training data
pca = PCA()
pca.fit(X_train)

# Calculate the cumulative explained variance
cumulative_explained_variance = np.cumsum(pca.explained_variance_ratio_)

# Create a plot to visualize the cumulative explained variance
plt.figure(figsize=(8, 6))
plt.plot(cumulative_explained_variance, marker='o')
plt.xlabel("Number of Components")
plt.ylabel("Cumulative Explained Variance")
plt.title("Cumulative Explained Variance by Principal Components")
plt.grid()
plt.show()

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import  r2_score



predictors = ['vendor_id', 'passenger_count', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'month', 'weekday_num', 'pickup_hour']
target = 'trip_duration'


X = df[predictors]
y = df.iloc[:,9].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7294)


#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,random_state = 7294)

# Creating a linear regression model
model = LinearRegression()


model.fit(X_train, y_train)


y_pred = model.predict(X_test)


r_2 = r2_score(y_test, y_pred)


coefficients = dict(zip(predictors, model.coef_))
print(" Coefficients:")
print(coefficients)


print("R-squared (R2) Score:", r_2)



cumulative_variance = np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4) * 100)
explained_variance = list(zip(range(1, len(cumulative_variance) + 1), cumulative_variance))
print(explained_variance)

from sklearn.tree import DecisionTreeRegressor

# Create and fit the Decision Tree regression model, measuring the time
start_time = time.time()
dt_regression = DecisionTreeRegressor().fit(X_train, y_train)
end_time = time.time()
dt_time = end_time - start_time

print(f"Time to train Decision Tree model: {dt_time:.2f} seconds")

# Predict on the test data
trips = dt_regression.predict(X_test)

de_t_score = r2_score(y_test, trips)
print(de_t_score)

from sortedcontainers import SortedDict
sorted_trip_data = SortedDict()
for index, row in df.iterrows():
    tr_id = row['id']
    trip_duration = row['trip_duration']
    sorted_trip_data[trip_duration] = (tr_id, row)
new_trp_id = 'new_trp_id'
new_tr_duration = 500
new_tr_data = {
    'vendor_id': 'new_vendor',
    'pickup_datetime': '2023-10-28 10:00:00',
    'dropoff_datetime': '2023-10-28 10:30:00',
    'passenger_count': 3,
    'pickup_longitude': -73.9895,
    'pickup_latitude': 40.7523,
    'dropoff_longitude': -73.9876,
    'dropoff_latitude': 40.7612,
    'store_and_fwd_flag': 'N',
}
sorted_trip_data[new_tr_duration] = (new_trp_id, new_tr_data)
for duration, (tr_id, data) in sorted_trip_data.items():
    print(f"Trip ID: {tr_id}, Duration: {duration} seconds")

import random

random_phone_numbers = [f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}" for _ in range(len(df))]

# Adding the 'phone_number' column to the DataFrame
df['phone_number'] = random_phone_numbers


print(df)

# Check the random phone numbers for the first 3 rows of data
for i in range(3):
    row = df.iloc[i]
    phone_number = row['phone_number']
    print(f"Row {i + 1} - Phone Number: {phone_number}")

df.head()
