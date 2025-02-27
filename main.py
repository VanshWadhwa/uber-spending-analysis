import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title='Uber Trip Analysis', layout='wide')
st.title('🚖 Uber Trip Data Analysis')

st.markdown("""
    This project provides an interactive dashboard for analyzing Uber trip data. It includes a variety of visualizations and insights into trip details, such as:
    - Total trips
    - Total distance traveled
    - Total fare spent
    - Average fare, distance, and duration across cities and product types
    - Trip trends based on time of day, day of the week, and more.
    
    **Note**: You will need to upload a CSV file containing your Uber trip data to interact with this dashboard.
    
    🔹 **How to Get Your Uber Trip Data?**

    1️⃣ **Open the Uber app**  
    2️⃣ **Go to Settings**  
    Navigate to Settings in the Uber app.  
    3️⃣ **Select Privacy**  
    Tap on Privacy and then choose **Download Your Data**.  
    4️⃣ **Request CSV Export**  
    Request a CSV export of your trip history.  

    **Ensure your dataset includes these columns** for compatibility with the app:
    - `request_time`: Timestamp when the ride was requested
    - `begin_trip_time`: Timestamp when the trip began
    - `dropoff_time`: Timestamp when the trip ended
    - `city`: City where the trip occurred
    - `product_type`: Type of Uber ride
    - `distance`: Total distance of the trip
    - `fare_amount`: The fare amount charged for the trip
    - `status`: Status of the trip

    ### How to Use This App
    1. **Upload your Uber trip data CSV file `Rider/trips_data-0.csv`** using the file uploader.
    2. **Explore visualizations** to gain insights into trip trends, fare analysis, and more.
    
    ### My Profile Links
    - **LinkedIn**: [Vansh Wadhwa - LinkedIn](https://www.linkedin.com/in/vansh-wadhwa)
    - **GitHub**: [Vansh Wadhwa - GitHub](https://github.com/VanshWadhwa)
    - **Twitter**: [@VanshWadhwa](https://twitter.com/VanshWadhwa_)
""")

file = st.file_uploader("Upload your Uber trip data CSV (Rider/trips_data-0.csv)", type=['csv'])
if file:
    df = pd.read_csv(file, parse_dates=['request_time', 'begin_trip_time', 'dropoff_time'])
    
    df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
    df['fare_amount'] = pd.to_numeric(df['fare_amount'], errors='coerce')
    df['hour'] = df['request_time'].dt.hour
    df['day_of_week'] = df['request_time'].dt.day_name()
    df['month'] = df['request_time'].dt.month_name()
    df['ride_duration'] = (df['dropoff_time'] - df['begin_trip_time']).dt.total_seconds() / 60
    
    city = st.sidebar.selectbox("Select City", ['All'] + list(df['city'].unique()))
    product_type = st.sidebar.selectbox("Select Product Type", ['All'] + list(df['product_type'].unique()))
    
    if city != 'All':
        df = df[df['city'] == city]
    if product_type != 'All':
        df = df[df['product_type'] == product_type]
    
    st.subheader("Key Trip Insights")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Trips", len(df))
    col2.metric("Total Distance Traveled (km)", round(df['distance'].sum(), 2))
    col3.metric("Total Fare Spent", f"{df['fare_amount'].sum():,.2f}")
    
    st.subheader("Trip Status Distribution")
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    status_fig = px.pie(status_counts, names='Status', values='Count', title="Trip Status Distribution")
    st.plotly_chart(status_fig)

    st.subheader("Average Fare per City")
    avg_fare_city = df.groupby('city')['fare_amount'].mean().reset_index()
    avg_fare_city_fig = px.bar(avg_fare_city, x='city', y='fare_amount', labels={'fare_amount': 'Average Fare'})
    st.plotly_chart(avg_fare_city_fig)

    st.subheader("Average Distance per Product Type")
    avg_distance_product = df.groupby('product_type')['distance'].mean().reset_index()
    avg_distance_product_fig = px.bar(avg_distance_product, x='product_type', y='distance', labels={'distance': 'Average Distance (km)'})
    st.plotly_chart(avg_distance_product_fig)

    st.subheader("Average Ride Duration per City")
    avg_duration_city = df.groupby('city')['ride_duration'].mean().reset_index()
    avg_duration_city_fig = px.bar(avg_duration_city, x='city', y='ride_duration', labels={'ride_duration': 'Average Duration (mins)'})
    st.plotly_chart(avg_duration_city_fig)

    st.subheader("Fare per Kilometer")
    df['fare_per_km'] = df['fare_amount'] / df['distance']
    fare_per_km_fig = px.histogram(df, x='fare_per_km', nbins=30, labels={'fare_per_km': 'Fare per Kilometer (INR)'})
    st.plotly_chart(fare_per_km_fig)

    st.subheader("Trips in Different Hour Ranges")
    hour_ranges = ['Morning (6-12)', 'Afternoon (12-18)', 'Evening (18-24)', 'Night (0-6)']
    df['hour_range'] = pd.cut(df['hour'], bins=[0, 6, 12, 18, 24], labels=hour_ranges, right=False)
    hour_range_counts = df['hour_range'].value_counts().reset_index()
    hour_range_counts.columns = ['Hour Range', 'Count']
    hour_range_fig = px.bar(hour_range_counts, x='Hour Range', y='Count', labels={'Count': 'Trip Count'})
    st.plotly_chart(hour_range_fig)

    st.subheader("High-Fare vs Low-Fare Distribution by City")
    high_fare_threshold = df['fare_amount'].quantile(0.75)
    df['fare_category'] = np.where(df['fare_amount'] > high_fare_threshold, 'High Fare', 'Low Fare')
    high_low_fare_city = df.groupby(['city', 'fare_category']).size().reset_index(name='Count')
    high_low_fare_city_fig = px.bar(high_low_fare_city, x='city', y='Count', color='fare_category', barmode='stack', labels={'Count': 'Trip Count'})
    st.plotly_chart(high_low_fare_city_fig)

    st.subheader("City with the Longest Average Distance")
    avg_distance_city = df.groupby('city')['distance'].mean().reset_index()
    longest_distance_city = avg_distance_city.loc[avg_distance_city['distance'].idxmax()]
    st.write(f"The city with the longest average distance is {longest_distance_city['city']} with an average of {longest_distance_city['distance']} km.")

    st.subheader("Ride Duration vs Fare")
    duration_fare_fig = px.scatter(df, x='ride_duration', y='fare_amount', labels={'ride_duration': 'Duration (mins)', 'fare_amount': 'Fare Amount'}, trendline="ols")
    st.plotly_chart(duration_fare_fig)

    st.subheader("Trips with Zero Fare")
    zero_fare_trips = df[df['fare_amount'] == 0]
    if not zero_fare_trips.empty:
        st.write(zero_fare_trips[['city', 'product_type', 'request_time', 'begin_trip_time', 'dropoff_time']])
    else:
        st.write("No trips with zero fare.")
    
    st.subheader("Trip Count per City")
    city_counts = df['city'].value_counts().reset_index()
    city_counts.columns = ['City', 'Count']
    city_fig = px.bar(city_counts, x='City', y='Count', labels={'City': 'City', 'Count': 'Trip Count'})
    st.plotly_chart(city_fig)
    
    st.subheader("Trip Count per Hour")
    hour_fig = px.histogram(df, x='hour', nbins=24, labels={'hour': 'Hour', 'count': 'Count'})
    st.plotly_chart(hour_fig)
    
    st.subheader("Trips per Day of the Week")
    day_counts = df['day_of_week'].value_counts().reset_index()
    day_counts.columns = ['Day', 'Count']
    day_fig = px.bar(day_counts, x='Day', y='Count', labels={'Day': 'Day', 'Count': 'Trip Count'})
    st.plotly_chart(day_fig)
    
    st.subheader("Ride Duration Analysis")
    duration_fig = px.histogram(df, x='ride_duration', nbins=30, labels={'ride_duration': 'Duration (mins)', 'count': 'Frequency'})
    st.plotly_chart(duration_fig)
    
    st.subheader("Fare Distribution")
    fare_fig = px.histogram(df, x='fare_amount', nbins=30, labels={'fare_amount': 'Fare Amount', 'count': 'Frequency'})
    st.plotly_chart(fare_fig)
    
    st.subheader("Distance vs Fare")
    scatter_fig = px.scatter(df, x='distance', y='fare_amount', labels={'distance': 'Distance (km)', 'fare_amount': 'Fare Amount'}, trendline="ols")
    st.plotly_chart(scatter_fig)
    
    st.subheader("Monthly Trip Trends")
    month_counts = df['month'].value_counts().reset_index()
    month_counts.columns = ['Month', 'Count']
    month_fig = px.line(month_counts, x='Month', y='Count', labels={'Month': 'Month', 'Count': 'Trip Count'})
    st.plotly_chart(month_fig)
    
    st.subheader("Peak Travel Times")
    peak_hour = df['hour'].value_counts().idxmax()
    peak_day = df['day_of_week'].value_counts().idxmax()
    st.write(f"Most frequent travel hour: **{peak_hour}:00**")
    st.write(f"Most frequent travel day: **{peak_day}**")
    
    st.subheader("Most Expensive Trips")
    expensive_trips = df.nlargest(5, 'fare_amount')
    st.write(expensive_trips[['city', 'fare_amount', 'distance', 'request_time', 'dropoff_time']])
    
    st.subheader("Cheapest Trips")
    cheap_trips = df.nsmallest(5, 'fare_amount')
    st.write(cheap_trips[['city', 'fare_amount', 'distance', 'request_time', 'dropoff_time']])
