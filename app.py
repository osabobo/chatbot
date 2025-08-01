from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage,HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()
#groq_api_key = os.getenv('GROQ_API_KEY')
groq_api_key = st.secrets["GROQ_API_KEY"]
def get_llm_response(query,chat_history):
    #groq_api_key = st.secrets["GROQ_API_KEY"]
    template = """
    You are a helpful and concise AI assistant. Use the chat history to provide contextually relevant and accurate answers. If the user's question relates to something previously discussed, reference it. If you don't know the answer, say so honestly.

    Chat history:
    {chat_history}

    User question:
    {user_question}

    Your response:
    """

    prompt = ChatPromptTemplate.from_template(template)


    llm = ChatGroq(model="llama-3.3-70b-versatile",groq_api_key=groq_api_key, temperature=0.8)


    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history":chat_history,
        "user_question":query
    })


def main():

    st.set_page_config(page_title='Streaming Chatbot',page_icon='🤖')

    st.header("Streaming Chatbot")


    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content='Hello, I am a Bot. How can i help you? ')
        ]

    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message,AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message,HumanMessage):
            with st.chat_message('Human'):
                st.write(message.content)


    user_input = st.chat_input('Type your message here...')

    if user_input is not None and user_input != "":
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        with st.chat_message("Human"):
            st.markdown(user_input)

        with st.chat_message("AI"):
            response = st.write_stream(get_llm_response(user_input,st.session_state.chat_history))


        st.session_state.chat_history.append(AIMessage(content=response))



if __name__=="__main__":
    main()
