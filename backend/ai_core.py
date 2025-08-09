import os
#import time
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader

# Your actual API key needs to be pasted here
API_KEY = "AIzaSyD8jmA6gEF8hSSetwtYnkP89x33eAULBz4"

# --- Setup LLM and Embeddings ---
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=API_KEY, temperature=0.3)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)

# --- CORRECTED: Full DOMAINS dictionary definition ---
DOMAINS = {
    "rti": {
        "description": "Questions related to the Right to Information Act, how to file an RTI, fees, and procedures.",
        "db_path": "db_rti"
    },
    "consumer_protection": {
        "description": "Questions related to consumer rights, unfair trade practices, defects in goods, and consumer complaints.",
        "db_path": "db_consumer_protection"
    },
    "landlord_tenant": {
        "description": "Questions related to leases, rent, eviction, and the rights and duties of landlords and tenants under the Transfer of Property Act.",
        "db_path": "db_landlord_tenant"
    },
    "contract_law": {
        "description": "Questions related to the Indian Contract Act, including agreements, contracts, proposals, acceptance, and remedies for breach of contract.",
        "db_path": "db_contract_law"
    }
}

vector_stores = {}
for domain, info in DOMAINS.items():
    if os.path.exists(info["db_path"]):
        vector_stores[domain] = Chroma(persist_directory=info["db_path"], embedding_function=embeddings)
        print(f"Loaded database for domain: {domain}")

# --- CORRECTED: Full router_template and router_prompt definition ---
router_template = """Your job is to determine the primary legal domain for the user's question from the list below. Choose the single best fit. Respond with ONLY the domain name.

Here are the available domains:
{domains}

User Question:
{question}

Domain:
"""
router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["question"],
    partial_variables={"domains": "\n".join([f"- {name}: {info['description']}" for name, info in DOMAINS.items()])}
)
router_chain = router_prompt | llm | StrOutputParser()


# --- CORRECTED: Full qa_prompt_template and qa_prompt definition ---
qa_prompt_template = """Answer the question as detailed as possible based ONLY on the provided context. If the answer is not in the provided context, just say, "The answer is not available in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
qa_prompt = PromptTemplate(template=qa_prompt_template, input_variables=["context", "question"])


def get_ai_response(query):
    #time.sleep(1) # Delay to help with rate limiting
    
    domain_result = router_chain.invoke({"question": query})
    domain = domain_result.strip().lower().replace("_", " ")
    print(f"--- Router decided domain: {domain} ---")

    if domain in vector_stores:
        retriever = vector_stores[domain].as_retriever(search_kwargs={'k': 3})
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | qa_prompt
            | llm
            | StrOutputParser()
        )
        result = rag_chain.invoke(query)
        return result
    else:
        # Fallback search if routing fails
        print("--- Routing failed. Searching all knowledge bases... ---")
        best_match_retriever = None
        highest_similarity = -1.0
        for domain_name, store in vector_stores.items():
            similar_docs = store.similarity_search_with_score(query, k=1)
            if similar_docs:
                score = similar_docs[0][1]
                print(f"Domain '{domain_name}' similarity score: {score}")
                if score < highest_similarity or highest_similarity == -1.0:
                    highest_similarity = score
                    best_match_retriever = store.as_retriever(search_kwargs={'k': 3})
        
        if best_match_retriever:
            print("--- Found best match. Generating response... ---")
            rag_chain = (
                {"context": best_match_retriever, "question": RunnablePassthrough()}
                | qa_prompt
                | llm
                | StrOutputParser()
            )
            return rag_chain.invoke(query)
        else:
            return "I'm sorry, I could not find a relevant answer in any of the available legal documents."