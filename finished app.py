import streamlit as st
import pickle
import numpy as np

# Load trained model
with open("Models/retail_sales_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Retail Store Sales Prediction")

# User inputs
category = st.selectbox("Category", ['Patisserie', 'Milk Products', 'Butchers', 'Beverages', 'Food','Furniture', 'Electric household essentials','Computers and electric accessories'])
payment_method = st.selectbox("Payment Method", ['Digital Wallet', 'Credit Card', 'Cash'])

location = st.selectbox("Location", ['Online', 'In-store'])

# Define mappings
months = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

weekdays = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
}

# User-friendly selectboxes
month_name = st.selectbox("Month", list(months.keys()))
weekday_name = st.selectbox("Weekday", list(weekdays.keys()))

# Encoded values
month = months[month_name]
weekday = weekdays[weekday_name]

price_per_unit = st.number_input("Price Per Unit", min_value=0.0, value=5.0)

discount_applied_checkbox = st.checkbox("Discount Applied")
discount_applied = 1 if discount_applied_checkbox else 0

# Prepare input
input_data = {
    "Category": category,
    "Payment Method": payment_method,
    "Location": location,
    "month": month,
    "weekday": weekday,
    "Price Per Unit": price_per_unit,
    "Quantity": 4,
    "Discount Applied": discount_applied,
    "Item": "Unknown"
}

# Convert to DataFrame
import pandas as pd
input_df = pd.DataFrame([input_data])

# Predict
if st.button("Predict Total Spent"):
    prediction = model.predict(input_df)
    st.success(f"Predicted Total Spent: ${prediction[0]:.2f}")
