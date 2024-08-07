# ________                .__                                      __
# \______ \   ____ ______ |  |   ____ ___.__. _____   ____   _____/  |_
#  |    |  \_/ __ \\____ \|  |  /  _ <   |  |/     \_/ __ \ /    \   __\
#  |    `   \  ___/|  |_> >  |_(  <_> )___  |  Y Y  \  ___/|   |  \  |
# /_______  /\___  >   __/|____/\____// ____|__|_|  /\___  >___|  /__|
#         \/     \/|__|               \/          \/     \/     \/


# Load package
import streamlit as st
#rom dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader, DataFrameLoader
import pandas as pd
import openai
import os
import keyboard
import time

# Load .env
#load_dotenv()

# Inisialisasi api key
#KEY = os.getenv("MY_KEY")

# Masukan api key
#openai.api_key = KEY

# Buat object embedding
embedding = OpenAIEmbeddings(openai_api_key='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')

# Model
llm = ChatOpenAI(model="gpt-4", openai_api_key='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', temperature=0)

# Load data csv used car
df = pd.read_csv(r'clean_usedcar_data.csv')

# Load data csv FAQ
loader = PyPDFLoader(r"question-answer.pdf")
data_faq = loader.load()

# Buat page seperti pdf dari used car data
loader = DataFrameLoader(df, page_content_column="combined_info")
data_car  = loader.load()

# Memotong karakter pada pdf per 1000 karakter
text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0,
                                               separators=[",","\n\n", "\n", "(?<=\. )", " "],
                                             length_function=len)

# Proses chunk
text_chunk_recom = text_spliter.split_documents(data_car)
text_chunk_faq = text_spliter.split_documents(data_faq)

# Vector DB data used car
vectorStore_recom  = FAISS.from_documents(text_chunk_recom, embedding)
vectorStore_faq = FAISS.from_documents(text_chunk_faq, embedding)

# Merge vectorestore
vectorStore_recom.merge_from(vectorStore_faq)

# Mmbuka file prompt
with open(r'prompt_combined.txt', 'r') as file:
    prompt_template = file.read()

# Membuat objek retriever
retrieve = vectorStore_recom.as_retriever(search_type="similarity", search_kwargs={"k": 3})


#   _________ __                                .__  .__  __
#  /   _____//  |________   ____ _____    _____ |  | |__|/  |_
#  \_____  \\   __\_  __ \_/ __ \\__  \  /     \|  | |  \   __\
#  /        \|  |  |  | \/\  ___/ / __ \|  Y Y  \  |_|  ||  |
# /_______  /|__|  |__|    \___  >____  /__|_|  /____/__||__|
#         \/                   \/     \/      \/

class BotCRC:

    def __init__(self):
        global prompt_template
        global retrieve
        self.prompt = PromptTemplate(input_variables=["context", "question", "chat_history"], template=prompt_template)
        self.memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", return_messages=True)
        self.qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retrieve, memory=self.memory,
                                                              combine_docs_chain_kwargs={'prompt': self.prompt})

    # Fungsi untuk berinteraksi dengan bot recommendation
    def conversation(self, user_input):
        result = self.qa_chain({"question": user_input})
        response = result["answer"]
        return response

    # Fungsi interface
    def chatbot_chain(self):
        USER = "user"
        ASSISTANT = "assistant"

        initial_context = "Anda adalah asisten dari Carsome, platform jual beli mobil bekas. Anda memiliki dua tugas utama: menjawab pertanyaan pelanggan dan memberikan rekomendasi mobil berdasarkan preferensi mereka."
        # self.memory.chat_memory.add_user_message(initial_context)
        self.memory.chat_memory.add_ai_message(
            "Halo! Saya adalah asisten dari Carsome. Bagaimana saya bisa membantu Anda hari ini?")

        exit_input = ['keluar', 'sampai jumpa lagi', 'sampai jumpa kembali', 'bye']


        # Interface dengan streamlit
        st.title("AutoBuddy")
        st.write("Carsome Assistant Chatbot")
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = self.memory.chat_memory
        else:
            self.memory.chat_memory = st.session_state.chat_history





        user_input = st.chat_input("Masukkan pesan yang ingin kamu tulis.", key="chat_input")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            if any(word in user_input.lower() for word in exit_input):
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.chat_message(ASSISTANT).write("Sampai jumpa lagi..", key="chat_output")
                time.sleep(2.5)
                keyboard.press_and_release('ctrl+w')
            else:
                result = self.conversation(user_input)
                # st.session_state.messages.append({"role": "user", "content": user_input})
                # output = st.chat_message(ASSISTANT).write(result, key="chat_output")

                st.session_state.messages.append({"role": "assistant", "content": result})

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

chat = BotCRC()
chat.chatbot_chain()