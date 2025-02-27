# Uber Data Analysis

This project provides an interactive dashboard for analyzing Uber trip data using **Streamlit**. It includes various visualizations and insights into trip details such as:

- **Total trips**
- **Total distance traveled**
- **Total fare spent**
- **Average fare, distance, and duration across cities and product types**
- **Trip trends based on time of day, day of the week, and more**

![Dashboard](<img/img (3).jpg>)


## 🚀 Features
- **Upload Uber trip data CSV**
- **Interactive charts and graphs**
- **City and product-type comparisons**
- **Time-based trip trends**

## 📌 How to Get Your Uber Trip Data?

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

![Uber Data Sample](image_placeholder)

---

## 🔹 How to Use This App

1. **Upload your Uber trip data CSV file** (e.g., `Rider/trips_data-0.csv`) using the file uploader.
2. **Explore visualizations** to gain insights into trip trends, fare analysis, and more.

![Upload CSV](image_placeholder)

---

## 💻 Installation & Usage

### Prerequisites
- **Python 3.7+**
- **Streamlit**

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
streamlit run main.py
```

---

## 🌟 My Profile Links
- **LinkedIn**: [Vansh Wadhwa - LinkedIn](https://www.linkedin.com/in/vansh-wadhwa)
- **GitHub**: [Vansh Wadhwa - GitHub](https://github.com/VanshWadhwa)
- **Twitter**: [@VanshWadhwa](https://twitter.com/VanshWadhwa_)

![alt text](<img/img (2).jpg>)
![alt text](<img/img (1).jpg>)
![alt text](<img/img (4).jpg>)
![alt text](<img/img (5).jpg>)
![alt text](<img/img (6).jpg>)
![alt text](<img/img (7).jpg>)