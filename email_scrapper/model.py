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

def extract_email_data(responses: list) -> list:
    """
    Extracts and normalizes email address from LLM responses.
    """
    final_data = []
    for res in responses:
        # Extract JSON-like sections from the response
        json_matches = re.findall(r'\[.*?\]', res["response"], re.DOTALL)
        for match in json_matches:
            try:
                email_entries = json.loads(match)
                for entry in email_entries:
                    email = entry.get("email")
                    source = entry.get("source")  # Retrieve the source from metadata

                    # Ensure both email and source exist and the email is in a valid format
                    if email and source:
                        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
                            final_data.append({
                                "email": email,
                                "source": source
                            })
                        else:
                            print(f"Invalid email format: {email}")
            except json.JSONDecodeError:
                print(f"Invalid JSON found: {match}")

    # Optionally sort entries alphabetically by email
    final_data.sort(key=lambda x: x["email"])
    return final_data