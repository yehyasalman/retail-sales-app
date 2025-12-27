import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

@st.cache_data
def load_data():
    return pd.read_csv("retail_store_sales.csv")

df = load_data()

st.subheader("Data Preview")
st.dataframe(df)

cat_cols = ['Category', 'Payment Method', 'Location', 'month', 'weekday']
num_cols = ['Price Per Unit', 'Quantity', 'Discount Applied']

def chatbot_response(user_input):
    user_input = user_input.lower()

    # Define intents with fuzzy keywords
    intents = {
        "top_category": ["top category", "best category", "popular category"],
        "avg_price": ["average price", "mean price", "unit price"],
        "discount": ["discount", "rebate", "offer", "promotion"],
        "payment": ["payment", "pay method", "transaction type"],
        "location": ["location", "store", "branch"],
        "weekday": ["weekday", "day", "week day"],
        "month": ["month", "season", "time period"],
        "total": ["total", "sum", "overall amount"]
    }

    # Match user input against intents
    matched_intent = None
    for intent, keywords in intents.items():
        for kw in keywords:
            if fuzz.partial_ratio(user_input, kw) > 60:  # fuzzy threshold
                matched_intent = intent
                break
        if matched_intent:
            break

    # Respond based on matched intent
    if matched_intent == "top_category":
        top_cat = df['Category'].value_counts().idxmax()
        return f"The top-selling category is {top_cat}."

    elif matched_intent == "avg_price":
        avg_price = df['Price Per Unit'].mean()
        return f"The average price per unit is {avg_price:.2f}$."

    elif matched_intent == "discount":
        avg_discount = df['Discount Applied'].mode()
        return f"The average discount applied is {avg_discount}."

    elif matched_intent == "payment":
        top_payment = df['Payment Method'].value_counts().idxmax()
        return f"The most common payment method is {top_payment}."

    elif matched_intent == "location":
        top_location = df['Location'].value_counts().idxmax()
        return f"The busiest location is {top_location}."

    elif matched_intent == "total":
        df['Total'] = df['Price Per Unit'] * df['Quantity']
        total_sales = df['Total'].sum()
        return f"The total sales amount is {total_sales:.2f}$"

    return "I can answer questions about category, price, discount, payment, location, or total."

st.title("Retail Sales Chatbot")

user_input = st.text_input("You:", "")
if user_input:
    response = chatbot_response(user_input)
    st.write("Answer:", response)


