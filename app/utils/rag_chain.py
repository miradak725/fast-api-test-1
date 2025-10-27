from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# from main import llm


from core.logger import logger


embedding_model = "BAAI/bge-large-en"
vector_store_path= "vector_store"
retrieve_method = "mmr"
# retrieve_method ="top_k"
# retrieve_method ="similarity_score_threshold"

llm=None
retriever=None
#-------------------------Initialize LLM-------------------------------
def load_llm():
    """
    Loads and initializes the Ollama LLM model globally.
    """
    global llm

    # load ML model
    try:                             
        logger.info("Initializing Ollama model...")
        # global llm
        llm= ChatOllama(
                model="llama3.2", 
                think=False,
                options={
                    "num_predict": 4096,
                    "temperature": 0.6,
                    "top_p": 0.95,
                    "top_k": 20,
                    "repeat_penalty": 1.05,
                }    
            )
    
        logger.info(f"Ollama model initialized successfully.{llm}")
        # Verify initialization
        if llm is None:
            raise ValueError("Model initialization returned None — check Ollama server status or model name.")
        logger.info(f"Ollama model initialized successfully: {llm.model}")
        return llm

    except Exception as e:
        # Catch all exceptions to prevent startup crashes
        logger.error(f"Failed to initialize model.: {e}")


# #--------------Initialize vector store-------------------------------
# def load_vector_store():
#     """
#     Loads and initializes the FAISS vector store globally.
#     """
#     global vector_store
#     try:
#         # Load embeddings model
#         embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
#         logger.debug("Embeddings model loaded successfully.")

#         # Load vector store        
#         vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
#         if vector_store is None:
#             raise ValueError("Vector store loading returned None.")
#         logger.info(f"Vector store loaded successfully from: {vector_store_path}")
#         return vector_store
#     except Exception as e:
#         logger.error(f"Failed to load vector store: {e}")
#         raise

# ------------ Retrieval -----------------------------------------------------
def load_retriever(retrieve_method:str):
    """
    Load FAISS vector store and return retriever.
    """
    try:
        logger.info(f"Initializing retriever using : {retrieve_method}")
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        logger.debug("Embeddings model loaded successfully.")

        #load vector store
        vector_store = FAISS.load_local(vector_store_path,embeddings,allow_dangerous_deserialization=True)
        logger.debug(f"Vector store loaded from path: {vector_store_path}")

        global retriever
        if retrieve_method == "similarity_score_threshold":
            retriever = vector_store.as_retriever(
                search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
            )
        elif retrieve_method == "top_k":
            retriever = vector_store.as_retriever(search_kwargs={"k": 1})     
        elif retrieve_method == "mmr":
            retriever = vector_store.as_retriever(search_type="mmr")           
        elif retriever is None:
            raise ValueError("Retriever initialization returned None.")
        logger.info(f"Retriever initialized successfully: {retriever}")


        return retriever
    except Exception as e:
        logger.error(f"Error initializing retriever: {e}")
        raise


# --------------- Answer Generation -------------------------------------------
def generate_answer(question):
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

        
        # llm= ChatOllama(
        #     model="llama3.2", 
        #     messages=chat_template,
        #     think=False,
        #     options={
        #         "num_predict": 4096,
        #         "temperature": 0.6,
        #         "top_p": 0.95,
        #         "top_k": 20,
        #         "repeat_penalty": 1.05,
        #     }    
        # )

        # chat_llm=request.app.state.llm

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