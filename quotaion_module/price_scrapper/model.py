import json
import re
from langchain.schema import Document
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama


def initialize_llm(api_key: str, temperature: int = 0, model_name: str = "qwen-2.5-32b") -> ChatGroq:
    """
    Initialize and return the ChatGroq LLM instance.
    """
    return ChatGroq(groq_api_key=api_key, temperature=temperature, model_name=model_name)


def initialize_llm_ollam(base_url: str = "http://127.0.0.1:11435", temperature: int = 0, model: str = "qwen2.5:14b") -> ChatOllama:
    """
    Initialize and return the ChatOllama LLM instance.
    """
     # Set context window to 32768 tokens
    return ChatOllama(base_url=base_url, model=model, temperature=temperature)

def process_query_across_chunks(query: str, chunked_docs: list, llm: ChatGroq) -> list:
    """
    Process the query across document chunks using the LLM.
    """
    responses = []
    for i, chunk in enumerate(chunked_docs):
        context = chunk["page_content"]
        metadata = chunk["metadata"]
        prompt_with_context = f"""
        Query: {query}
        Context: {context}
        Metadata: {metadata}
        Provide the most accurate and concise response based on the context and query:
        """
        try:
            response = llm.invoke(prompt_with_context)
            responses.append({"response": response.content, "metadata": metadata})
        except Exception as e:
            print(f"Error processing chunk {i + 1}: {e}")
    return responses

def extract_product_data(responses: list) -> list:
    """
    Extracts and normalizes product data from LLM responses.
    For any missing field in the JSON, the field is set to "Null ".
    """
    final_data = []
    for res in responses:
        # Find JSON-like arrays in the response
        json_matches = re.findall(r'\[.*?\]', res["response"], re.DOTALL)
        for match in json_matches:
            try:
                products = json.loads(match)
                for product in products:
                    # For each field, provide a default value "Null " if the key is missing
                    product_name = product.get("product_name", "Null ")
                    price = product.get("price", "Null ")
                    currency = product.get("currency", "Null ")
                    source = product.get("source", "Null ")
                    vat_status = product.get("vat_status", "Null ")
                    payment_type = product.get("payment_type", "Null ")
                    features_of_product = product.get("features_of_product", "Null ")
                    vendor_name = product.get("vendor_name", "Null ")
                    customer_rating = product.get("customer_rating", "Null ")

                    # Clean and convert the price if it is not missing
                    if price != "Null ":
                        cleaned_price = re.sub(r'[^\d.]', '', str(price))
                        try:
                            price_val = float(cleaned_price) if '.' in cleaned_price else int(cleaned_price)
                        except ValueError:
                            print(f"Invalid price format: {price}")
                            price_val = "Null "
                    else:
                        price_val = "Null "

                    final_data.append({
                        "product_name": product_name,
                        "price": price_val,
                        "currency": currency,
                        "source": source,
                        "vat_status": vat_status,
                        "payment_type": payment_type,
                        "features_of_product": features_of_product,
                        "vendor_name": vendor_name,
                        "customer_rating": customer_rating
                    })
            except json.JSONDecodeError:
                print(f"Invalid JSON found: {match}")

    # Sort products by price (lowest first). Products with a missing price ("Null ") are placed at the end.
    final_data.sort(key=lambda x: x["price"] if isinstance(x["price"], (int, float)) else float('inf'))
    return final_data
