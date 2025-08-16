import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- IMPORTANT: The same key from your ai_core.py file ---
# In a real app, this would be in a single .env file.
API_KEY = ""

# The main folder containing all the domain-specific sub-folders
KNOWLEDGE_BASE_DIR = "knowledge_base"

def create_vector_db_for_domain(domain_folder, db_persist_path):
    """
    Loads all PDFs from a folder, splits them, creates embeddings,
    and saves them to a persistent ChromaDB store.
    """
    print(f"--- Processing domain: {domain_folder} ---")

    # Load all PDF files from the given folder
    all_docs = []
    for filename in os.listdir(domain_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(domain_folder, filename)
            print(f"Loading PDF: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            all_docs.extend(loader.load())

    if not all_docs:
        print(f"No PDF files found in {domain_folder}. Skipping.")
        return

    # Split the documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(all_docs)
    print(f"Split into {len(texts)} chunks.")

    # Create embeddings and the vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)
    vector_store = Chroma.from_documents(texts, embeddings, persist_directory=db_persist_path)

    print(f"Successfully created database for {domain_folder} at {db_persist_path}")

# Main function to process all domain folders
if __name__ == '__main__':
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        print(f"Error: Directory '{KNOWLEDGE_BASE_DIR}' not found.")
    else:
        # Loop through each sub-folder in the knowledge_base directory
        for domain in os.listdir(KNOWLEDGE_BASE_DIR):
            domain_path = os.path.join(KNOWLEDGE_BASE_DIR, domain)
            if os.path.isdir(domain_path):
                db_path = f"db_{domain}" # e.g., db_rti, db_consumer_protection
                create_vector_db_for_domain(domain_path, db_path)
        print("\n--- All knowledge bases have been set up successfully! ---")
