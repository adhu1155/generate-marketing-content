import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("API_KEY")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a marketing specialist with over two decades of experience who writes great content for the clients marketing requirements, "
         "you need to take the topic the user gives and create a social media post about that topic which create a lot impressions in the desired format,emotions,target audience,words length user provides."
         "Format means the type of social media user intends to post. "),
        ("user", "Question: {question}")
    ]
)

# Page title and description
st.title('Generate Marketing Content')
st.markdown("""
            Create compelling marketing content effortlessly! 
            Simply fill in the details below and let our AI generate engaging posts for you.
            """)

# Input fields for post parameters
format_type = st.text_input("Format of the Post (e.g., Twitter, LinkedIn, etc.):")
topic = st.text_input("Topic of the Post(e.g., Usage of AI in dailylife etc.):")
emotion = st.selectbox("Emotion of the Post:", ["Positive", "Negative", "Neutral"])
target_audience = st.text_input("Target Audience for this Post(e.g., Students, Senior Citizens etc.):")
word_length = st.text_input("Desired Word Count for the Post (e.g., 150):")

# Button to generate content
if st.button("Generate Content", key="generate_button"):
    # Validate input
    if not all([format_type.strip(), topic.strip(), emotion.strip(), word_length.strip(), target_audience.strip()]):
        st.error("Please fill in all fields.")
    elif not word_length.strip().isdigit():
        st.error("Word count must be a number.")
    else:
        input_text = f"Generate a {format_type.strip()} post on the topic '{topic.strip()}' with a {emotion.strip()} emotion for the target audience {target_audience.strip()} in {word_length.strip()} words."
        llm = Ollama(model="llama3")
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        response = chain.invoke({"question": input_text})
        
        # Display generated content
        st.markdown(f"### Generated Content:")
        st.info(response)

