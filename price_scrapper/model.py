import json
import re
from langchain.schema import Document
from langchain_groq import ChatGroq

def initialize_llm(api_key: str, temperature: int = 0, model_name: str = "llama3-8b-8192") -> ChatGroq:
    """
    Initialize and return the ChatGroq LLM instance.
    """
    return ChatGroq(groq_api_key=api_key, temperature=temperature, model_name=model_name)

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
    """
    final_data = []
    for res in responses:
        # Find JSON-like arrays in the response
        json_matches = re.findall(r'\[.*?\]', res["response"], re.DOTALL)
        for match in json_matches:
            try:
                products = json.loads(match)
                for product in products:
                    product_name = product.get("product_name")
                    price = product.get("price")
                    currency = product.get("currency")
                    source = product.get("source")
                    vat_status = product.get("vat_status")
                    payment_type = product.get("payment_type")
                    if product_name and price and currency and source:
                        # Clean and convert the price
                        cleaned_price = re.sub(r'[^\d.]', '', str(price))
                        try:
                            price_val = float(cleaned_price) if '.' in cleaned_price else int(cleaned_price)
                        except ValueError:
                            print(f"Invalid price format: {price}")
                            continue

                        final_data.append({
                            "product_name": product_name,
                            "price": price_val,
                            "currency": currency,
                            "source": source,
                            "vat_status" : vat_status,
                            "payment_type" : payment_type 
                        })
            except json.JSONDecodeError:
                print(f"Invalid JSON found: {match}")

    # Sort products by price (lowest first)
    final_data.sort(key=lambda x: x["price"])
    return final_data
