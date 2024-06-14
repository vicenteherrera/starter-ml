import os
# from dotenv import load_dotenv
# from langchain_openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import dotenv_values

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter

CONFIG_FILE = os.getenv("CONFIG_FILE")
if CONFIG_FILE == None or CONFIG_FILE == "":
    CONFIG_FILE = "config/env.txt"
print(f"Using CONFIG_FILE={CONFIG_FILE}")
config = dotenv_values(CONFIG_FILE)
if not "OPENAI_API_KEY" in config:
    print("OPENAI_API_KEY config not found")
    exit()

# Model to use
# llm_model = "gpt-3.5-turbo"
llm_model = "gpt-4"

print("# Load the document as splitted chunks of text")
txt_file_path='./data/scalexi.txt'
loader = TextLoader(file_path=txt_file_path, encoding="utf-8")
data = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
data = text_splitter.split_documents(data)

# Create vector store and put the document in it
embeddings = OpenAIEmbeddings(api_key=config['OPENAI_API_KEY'])
vectorstore = FAISS.from_documents(data, embedding=embeddings)

# Create conversation chain
llm = ChatOpenAI(temperature=0.7, model_name=llm_model, api_key=config['OPENAI_API_KEY'])
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    memory=memory
    )

def invoke(prompt):
    result = conversation_chain.invoke({"question": prompt})
    return result["answer"]

app = Flask(__name__)
@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.json.get('question')
    response = invoke(prompt)
    return jsonify({"answer": response})

# Run the Flask app
if __name__ =='__main__':
    app.run(host='0.0.0.0', port=3000)
