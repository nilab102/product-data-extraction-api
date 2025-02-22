import json
import requests
import traceback

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from email_scrapper.config import (
    SERPER_API_KEY,
    LLM_API_KEY,
    SERPER_URL,
    SERPER_LOCATION,
    SERPER_GL,
    ALLOWED_DOMAINS,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)
from email_scrapper.model import initialize_llm, extract_email_data
from email_scrapper.util import clean_text
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import BM25Retriever
router = APIRouter()
class SearchRequest(BaseModel):
    query: str

def fetch_search_results(query: str) -> dict:
    """
    Uses the Serper API to fetch search results for the given query.
    """
    payload = {
        "q": query,
        "location": SERPER_LOCATION,
        "gl": SERPER_GL
    }
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(SERPER_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching search results: {response.status_code}")

def filter_links(search_data: dict) -> List[str]:
    """
    Extracts and filters links from search results based on allowed domains,
    ensuring each link is unique.
    """
    links = []
    for item in search_data.get("organic", []):
        link = item.get("link")
        if link:
            links.append(link)
    # Deduplicate links while preserving order
    unique_links = list(dict.fromkeys(links))
    print(f"number of links {unique_links}")
    return unique_links


@router.post("/search")
async def search_endpoint(request: SearchRequest):
    query = request.query
    try:
        # Fetch search results from the Serper API
        search_data = fetch_search_results(query)
        links = filter_links(search_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    if not links:
        raise HTTPException(status_code=404, detail="No matching links found for the query.")

    # Process each link to extract cleaned text from the document
    documents = []
    for url in links:
        try:
            text_content = clean_text(url,method="notzenrows")
            # Limit document length if necessary
            documents.append(Document(page_content=(text_content[:5000] + text_content[-5000:]), metadata={"source": url}))
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    if not documents:
        raise HTTPException(status_code=404, detail="No documents could be processed.")

    # Split documents into smaller chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunked_docs = []
    for doc in documents:
        chunks = splitter.split_text(doc.page_content)
        for chunk in chunks:
            chunked_docs.append({"page_content": chunk, "metadata": doc.metadata})
    print(f"Total chunks created: {len(chunked_docs)}")
    # Initialize BM25 Retriever on the document chunks
    bm25_retriever = BM25Retriever.from_documents(
        [Document(page_content=chunk["page_content"], metadata=chunk["metadata"]) for chunk in chunked_docs]
    )
    bm25_retriever.k = 40  # Retrieve top 10 relevant chunks
    retrieved_chunks = bm25_retriever.get_relevant_documents("email")
    
    # Define the detailed query prompt for extraction
    query_prompt = '''
    Extract all valid email addresses from the provided document. Do not guess or fabricate any details; only include information that is complete, unambiguous, and reliable. Provide the results in **JSON format** with the following specifications:

    ### Fields:
    1. **"email"**: The complete and properly formatted email address (e.g., example@domain.com). Exclude any addresses that are incomplete or improperly formatted.
    2. **"source"**: The URL of the document from which the email address was extracted, taken from the document metadata.

    ### Output Style:
    [
        {
            "email": "example@domain.com",
            "source": "URL of the document"
        },
        {
            "email": "another@example.com",
            "source": "URL of the document"
        }
    ]

    ### Important Notes:
    1. Extract data strictly based on the provided document chunks. Do not infer or create information beyond what is present.
    2. Include entries only when both **"email"** and **"source"** fields are complete and reliable. Exclude any entry where either field is missing or uncertain.
    3. Ensure that each email address adheres to standard email formatting rules.
    4. For the **"source"** field, use the URL provided in the document metadata.
    5. If no valid information is available in the document chunks, output an empty JSON array:
      ```json
      []
    '''



    # Initialize the LLM (ChatGroq in this case)
    llm = initialize_llm(api_key=LLM_API_KEY)
    final_responses = []
    print(len(retrieved_chunks))
    print(f"Chunk size is {CHUNK_SIZE}")
    # Process each retrieved chunk using the LLM
    for i, chunk in enumerate(retrieved_chunks):
        context = chunk.page_content
        metadata = chunk.metadata
        prompt_with_context = f"""
Query: {query_prompt}
Context: {context}
Metadata: {metadata}
Provide the most accurate and concise response based on the context and query:
"""
        try:
            response = llm.invoke(prompt_with_context)
            final_responses.append({"response": response.content, "metadata": metadata})
            print(f"processing chunk {i+1}")
        except Exception as e:
            print(f"Error processing chunk {i+1}: {e}")
    
    # Extract product data from the LLM responses
    final_output = extract_email_data(final_responses)
    
    return {"results": final_output}
