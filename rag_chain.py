from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


from logger import logger


embedding_model = "BAAI/bge-large-en"
vector_store_path= "vector_store"
retrieve_method ="max_marginal_relevance"

# ------------ Retrieval -----------------------------------------------------
def retrieve(retrieve_method:str):
    """
    Load FAISS vector store and return retriever.
    """
    logger.info(f"Initializing retriever using {embedding_model} and method: {retrieve_method}")
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    logger.debug("Embeddings model loaded successfully.")

    #load vector store
    vector_store = FAISS.load_local(vector_store_path,embeddings,allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_type="mmr")
    logger.debug(f"Vector store loaded from path: {vector_store_path}")


    return retriever


# --------------- Answer Generation -------------------------------------------
def generate_answer(question,retriever):
    """
    Generate an answer using RAG pipeline.
    """

    try:
        logger.info(f"Generating answer for question: {question}")

        retrieved_docs=retriever.invoke(question)
        print(retrieved_docs)
        context="\\n".join([d.page_content for d in retrieved_docs])

        logger.debug(f"retrived content: {context}")
        logger.info("documents retrieved successfully")
        
        # Define a chat prompt template composed of system and user messages
        chat_template= ChatPromptTemplate.from_messages([
        {"role": "system", "content": """Using the information contained in the context,
        give a comprehensive answer to the question.
        Respond only to the question asked, response should be concise and relevant to the question.
        Provide the number of the source document when relevant.
        If the answer cannot be deduced from the context, do not give an answer."""},
        {"role": "user", "content": f"""Context:
        {context}
        ---
        Now here is the question you need to answer.

        Question: {question}"""},
        ])

        logger.debug("Chat prompt template created.")

        logger.info("Initializing Ollama model...")
        llm= ChatOllama(
            model="llama3.2", 
            messages=chat_template,
            think=False,
            options={
                "num_predict": 4096,
                "temperature": 0.6,
                "top_p": 0.95,
                "top_k": 20,
                "repeat_penalty": 1.05,
            }    
        )
        logger.info("Ollama model initialized successfully.")

        chain = chat_template|llm
        answer = chain.invoke({"question": question})
        logger.info("Answer generated successfully.")
        print(answer.content)

        #convert the retrieved_doc to a list of strings
        references =[]
        for docs in retrieved_docs:
            references.append(docs.page_content)
        return answer.content, references
    except Exception as e:
        logger.exception(f"Error generating answer: {e}")
        raise