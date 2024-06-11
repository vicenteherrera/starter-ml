# rag_langchain_openai

Retrieval Augmented Generation (RAG) using a [FAISS vector database](https://github.com/facebookresearch/faiss), [LangChain](https://www.langchain.com/) and [OpenAI GPT-4](https://openai.com/) for inference.

Check the generic instructions for requirements at parent [README.md](../../README.md).

It loads `data/scalexi.txt` information file, split it in chunks, send them to `OpenAIEmbeddings` to convert them into embeddings, and stores it in FAISS.

Then, calls `ConversationalRetrievalChain.from_llm` to answer a prompt, giving it access to retrieve information from the vector database.

Run it with:
```
make
```
