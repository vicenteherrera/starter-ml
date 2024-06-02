
# Google Colab Notebook at: https://colab.research.google.com/drive/13oFA9M103askqjD80wq3Z7coNMC-TiAS#

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter

import os
from dotenv import dotenv_values

# Set OpenAI API key
config = dotenv_values('env.txt')

# Model to use
# llm_model = "gpt-3.5-turbo"
llm_model = "gpt-4"

print("# Load the document as splitted chunks of text")
txt_file_path='./data/scalexi.txt'
loader = TextLoader(file_path=txt_file_path, encoding="utf-8")
data = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
data = text_splitter.split_documents(data)

# Show the contents of the loaded document
# print(data)

# Create vector store and put the document in it
embeddings = OpenAIEmbeddings(api_key=config['OPENAI_API_KEY'])
vectorstore = FAISS.from_documents(data, embedding=embeddings)

# Create conversation chain
llm = ChatOpenAI(temperature=0.7, model_name=llm_model, api_key=config['OPENAI_API_KEY'])
memory = ConversationBufferMemory(
memory_key='chat_history', return_messages=True)
conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        memory=memory
        )

# Test question 1
query = "What is ScaleX Innovation?"
print("\nQUERY: " + query)
result = conversation_chain.invoke({"question": query})
answer = result["answer"]
print("\nANSWER: " + answer)

# Test question 2
query = "What is the contact information?"
print("\nQUERY: " + query)
result = conversation_chain.invoke({"question": query})
answer = result["answer"]
print("\nANSWER: " + answer)

# Test question 3
query = "What are the main activities of ScaleX Innovation. Write is as three bullet points."
print("\nQUERY: " + query)
result = conversation_chain.invoke({"question": query})
answer = result["answer"]
print("\nANSWER: " + answer)
