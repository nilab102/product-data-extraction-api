    
    # Define the detailed query prompt for extraction
query_prompt = f'''
Extract details of product from the provided document. If any information is incomplete, ambiguous, or missing, do not guess or fabricate details. Only include information that you are confident is accurate and complete. Provide the results in **JSON format** with the following specifications:

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






import json
import re
from langchain.schema import Document
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

def initialize_llm_ollam(base_url: str = "http://127.0.0.1:11435/", temperature: int = 0, model: str = "qwen2.5:7b") -> ChatOllama:
    """
    Initialize and return the ChatOllama LLM instance.
    """
    # Set context window to 32768 tokens
    return ChatOllama(base_url=base_url, model=model, temperature=temperature)
llm=initialize_llm_ollam()













import json

def process_text(text: str):
    # Check if the given text is valid JSON
    try:
        json.loads(text)
        # If valid, return True
        return text
    except json.JSONDecodeError:
        prompt_with_context = f"""
Query: {query_prompt}
Context: {text}
Provide the most accurate and concise response based on the context and query:
"""
        # Try invoking the LLM up to 3 times to get valid JSON
        for _ in range(3):
            response = llm.invoke(prompt_with_context, options={"num_ctx": 20000})
            try:
                json.loads(response.content)
                # If valid JSON, return the response content
                return response.content
            except json.JSONDecodeError:
                continue
        return False

