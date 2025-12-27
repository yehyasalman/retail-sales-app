import streamlit as st
import pandas as pd

st.title("Rule-Based Chatbot for Retail Sales Data")

# 1. Load dataset (or use placeholder if missing)
try:
    df = pd.read_csv("retail_store_sales.csv")
    st.write("Preview of your data:")
    st.dataframe(df.head())
    context = df.describe(include="all").to_string()
except Exception:
    st.warning("Dataset not found. Using placeholder context.")
    df = None
    context = "Placeholder dataset summary goes here."

# 2. Chat interface
user_question = st.text_area("Ask a question about the data:")

if st.button("Get Answer") and user_question:
    answer = "Sorry, I don't understand that question."

    # 3. Rule-based responses
    q = user_question.lower()

    if "total sales" in q:
        if df is not None:
            total_sales = df["sales"].sum()
            answer = f"The total sales are {total_sales}."
        else:
            answer = "Dataset not available to calculate total sales."

    elif "average sales" in q or "mean sales" in q:
        if df is not None:
            avg_sales = df["sales"].mean()
            answer = f"The average sales are {avg_sales:.2f}."
        else:
            answer = "Dataset not available to calculate average sales."

    elif "highest sales" in q or "max sales" in q:
        if df is not None:
            max_sales = df["sales"].max()
            answer = f"The highest sales value is {max_sales}."
        else:
            answer = "Dataset not available to calculate highest sales."

    elif "lowest sales" in q or "min sales" in q:
        if df is not None:
            min_sales = df["sales"].min()
            answer = f"The lowest sales value is {min_sales}."
        else:
            answer = "Dataset not available to calculate lowest sales."

    elif "describe" in q or "summary" in q:
        answer = f"Here is a dataset summary:\n{context}"

    # 4. Display answer
    st.write("Answer:")
    st.write(answer)


    # 5. Display answer
    st.write("Answer:")
    st.write(response.text)

