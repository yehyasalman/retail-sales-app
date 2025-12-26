import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Configure API key securely (set in Streamlit secrets or environment)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

st.title("Ask Questions About Retail Sales Data")

# Load your dataset (make sure this file is in your repo)
df = pd.read_csv("retail_store_sales.csv")

st.write("Preview of your data:")
st.dataframe(df)

# User question
user_question = st.text_area("Ask a question about the data:")

if st.button("Get Answer") and user_question:
    # Summarize data context
    data_summary = df.describe(include="all").to_string()

    # Build prompt
    prompt = f"""
    You are an AI assistant. Here is a dataset summary:
    {data_summary}

    User question: {user_question}
    Please answer clearly and concisely.
    """

    # Create model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate response
    response = model.generate_content(prompt)

    st.write("Answer:")
    st.write(response.text)
