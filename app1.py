from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()
# Get the GROQ_API_KEY from environment variables
# Get the GROQ_API_KEY from environment variables
#groq_api_key = os.getenv('GROQ_API_KEY')
groq_api_key = st.secrets["GROQ_API_KEY"]
# Check if the API key is present
if groq_api_key is None:
    raise ValueError("Did not find groq_api_key, please add an environment variable `GROQ_API_KEY` which contains it, or pass `groq_api_key` as a named parameter.")


# Function to get LLM response
def get_llm_response(user_input, chat):
    # Assuming this function uses groq_api_key in some way
    # Use the groq_api_key as needed
    # Placeholder implementation for the function
    template = """
        You are a helpful assistant. Answer the following questions considering the history of the conversation:

        Chat history : {chat_history}

        User question : {user_question}

        """
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGroq(model="llama-3.3-70b-versatile")

    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat,
        "user_question": user_input
    })


# Main function
def main():
    st.title("Streaming Chatbot")
    user_input = st.text_input("You: ", "")

    if user_input:
        response = get_llm_response(user_input, st.session_state.get('chat', []))
        if 'chat' not in st.session_state:
            st.session_state['chat'] = []
        st.session_state.chat.append({"user": user_input, "response": response})
        st.write(response)


if __name__ == "__main__":
    main()
