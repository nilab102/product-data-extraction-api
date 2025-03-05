import json
import requests
import traceback

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from quotaion_module.price_scrapper.config import (
    SERPER_API_KEY,
    LLM_API_KEY,
    SERPER_URL,
    SERPER_LOCATION,
    SERPER_GL,
    ALLOWED_DOMAINS,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)
from quotaion_module.price_scrapper.model import initialize_llm, extract_product_data
from quotaion_module.price_scrapper.util import clean_text,process_url
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    Extracts and filters links from search results based on allowed domains.
    """
    links = []
    for item in search_data.get("organic", []):
        link = item.get("link")
        # if link and any(domain in link for domain in ALLOWED_DOMAINS):
        #     links.append(link)
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
    errors = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all tasks
        futures = {
            executor.submit(process_url, url, "notzenrows"): url
            for url in links
        }
        
        # Process results as they complete
        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
                if isinstance(result, tuple):  # Error case
                    errors.append(result)
                else:
                    documents.append(result)
            except Exception as e:
                errors.append((url, str(e)))

    # Print errors after processing
    for url, error in errors:
        print(f"Error processing {url}: {error}")

    # Split documents into smaller chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunked_docs = []
    for doc in documents:
        chunks = splitter.split_text(doc.page_content)
        for chunk in chunks:
            chunked_docs.append({"page_content": chunk, "metadata": doc.metadata})
    
    # Initialize BM25 Retriever on the document chunks
    bm25_retriever = BM25Retriever.from_documents(
        [Document(page_content=chunk["page_content"], metadata=chunk["metadata"]) for chunk in chunked_docs]
    )
    bm25_retriever.k = 20  # Retrieve top 10 relevant chunks
    retrieved_chunks = bm25_retriever.get_relevant_documents(query)
    
    # Define the detailed query prompt for extraction
    query_prompt = f'''
    Extract details of {query} from the provided document. If any information is incomplete, ambiguous, or missing, do not guess or fabricate details. Only include information that you are confident is accurate and complete. Provide the results in **JSON format** with the following specifications:

    ### Fields:
    1. **"product_name"**: The full and properly formatted name of the product, including brand and relevant specifications. Avoid truncation or abbreviation. Exclude any entries where the product name is incomplete or unclear.
    2. **"price"**: The exact total price of the product should be represented as a decimal number, reflecting the complete, one-time cost. **Do not include any monthly installment, financing, or partial payment amounts.** Ensure the number is preserved as it is without currency symbols, commas, or any other formatting characters.
    3. **"currency"**: The currency in which the price is denominated, extracted from the document.
    4. **"vat_status"**: A string indicating whether the price is after vat or before vat. Only include this field if the document explicitly provides this information.
    5. **"payment_type"**: A string that indicates whether the payment is a "one time payment" or an "installment", based on explicit information in the document. If the payment type is not explicitly provided, do not include this field.
    6. **"vendor_name"**: The name of the vendor selling the product, exactly as provided in the document. Exclude this field if the vendor name is incomplete or not explicitly stated.
    7. **"features_of_product"**: Details on the features of the product as provided in the document. Include this field only if the information is complete and reliable.
    8. **"source"**: The URL of the document from which the product details were extracted.
    9. **"customer_rating"**: The customer rating for the product as provided in the document. Include this field only if the information is explicitly stated and complete.


    ### Output Style:
    [
        {{
            "product_name": "Full product name with accurate details",
            "price": price,
            "currency": "Currency code (e.g., USD, SAR)",
            "vat_status": "after vat / before vat",
            "payment_type": "one time payment / installment",
            "vendor_name": "Vendor name as per document",
            "features_of_product": "Product features details, if provided",
            "source": "URL of the document",
            "customer_rating": "Customer rating details if available"
        }},
        {{
            "product_name": "Another valid product name",
            "price": price,
            "currency": "Currency code (e.g., USD, SAR)",
            "vat_status": "after vat / before vat",
            "payment_type": "one time payment / installment",
            "vendor_name": "Vendor name as per document",
            "features_of_product": "Product features details, if provided",
            "source": "URL of the document",
            "customer_rating": "Customer rating details if available"
        }}
    ]

    ### Important Notes:
    1. Extract data strictly based on the provided document chunks. Do not infer or create information beyond what is present.
    2. Include entries only when all fields are complete and reliable.
    3. Properly format product names with capitalization and full details.
    4. For the "price" field, ensure that only the full product price is provided, excluding any installment or financing details.
    5. For the "currency" field, use the currency explicitly mentioned in the document.
    6. For the "vat_status" field, extract the information indicating if the price is before vat or after vat as stated in the document. If not explicitly stated, do not include this field.
    7. For the "payment_type" field, determine if the payment method is one time payment or installment as explicitly mentioned in the document. If not explicitly mentioned, do not include this field.
    8. For the "vendor_name" field, include the vendor name exactly as it appears in the document if it is complete and reliable.
    9. For the "product_quality_review" field, include product review or quality information only if it is explicitly provided and complete.
    10. For the "source" field, use the URL provided in the document metadata.
    11. If no valid information is available, output an empty JSON array.
    '''



    # Initialize the LLM (ChatGroq in this case)
    llm = initialize_llm(api_key=LLM_API_KEY)
    final_responses = []
    
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
    final_output = extract_product_data(final_responses)
    
    return {"results": final_output}
