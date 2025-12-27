import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# 1. Configure API key (use Streamlit Secrets or environment variable)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

st.title("AI Chatbot for Retail Sales Data")

# 2. Load your dataset (replace with your actual file or source)
# Put your dataset in the repo root or adjust the path
try:
    df = pd.read_csv("retail_store_sales.csv")
    st.write("Preview of your data:")
    st.dataframe(df.head())
    # Create a placeholder context from the dataset
    context = df.describe(include="all").to_string()
except Exception as e:
    st.warning("Dataset not found. Using placeholder context.")
    context = "Placeholder dataset summary goes here."

# 3. Chat interface
user_question = st.text_area("Ask a question about the data:")

if st.button("Get Answer") and user_question:
    # Build prompt with context
    prompt = f"""
    You are an AI assistant. Here is the dataset context:
    {context}

    User question: {user_question}
    Please answer clearly and concisely.
    """

    # 4. Create model and generate response
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # 5. Display answer
    st.write("Answer:")
    st.write(response.text)
