import streamlit as st
import pandas as pd
import google as genai

# Configure your API key (set as environment variable for safety)
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

st.title("Ask Questions About Retail Sales Data")

# Load your dataset
df = pd.read_csv("sales_data.csv")

st.write("Preview of your data:")
st.dataframe(df.head())

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

