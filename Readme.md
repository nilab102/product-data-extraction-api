
# Product Data Extraction API

This repository contains a **Product Data Extraction API** built with [FastAPI](https://fastapi.tiangolo.com/). It leverages multiple tools and services to search for product information online, clean and process HTML content, and extract structured product details using a language model.

## Features

- **Web Search Integration:** Uses the [Serper API](https://serper.dev/) to perform product-related searches.
- **Content Retrieval:** Fetches HTML content from web pages using either Selenium or [ZenRows](https://www.zenrows.com/).
- **HTML Cleaning & Conversion:** Cleans HTML content (removing headers, footers, ads, etc.) and converts it to Markdown for easier text processing.
- **Document Chunking:** Splits lengthy documents into smaller chunks for efficient processing.
- **Relevant Chunk Retrieval:** Uses BM25 retrieval (via Langchain) to select the most relevant document sections.
- **LLM-Powered Extraction:** Leverages a ChatGroq language model to extract product details based on a detailed prompt.
- **Structured Output:** Returns product details in JSON format, including fields such as `product_name`, `price`, `currency`, `vat_status`, `payment_type`, and `source`.

## Prerequisites

- **Python 3.8+**
- [pip](https://pip.pypa.io/en/stable/)
- [Google Chrome](https://www.google.com/chrome/) (for Selenium-based fetching)
- [ChromeDriver](https://chromedriver.chromium.org/) (compatible with your installed version of Chrome)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/guthyb.git
   cd guthyb
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   Ensure you have a `requirements.txt` file listing all necessary packages. Then run:

   ```bash
   pip install -r requirements.txt
   ```

   _Required packages include but are not limited to: `fastapi`, `uvicorn`, `python-dotenv`, `requests`, `beautifulsoup4`, `html2text`, `selenium`, `langchain`, and others._

4. **Configure Environment Variables:**

   Create a `.env` file in the root directory with the following content:

   ```dotenv
   SERPER_API_KEY=your_serper_api_key_here
   LLM_API_KEY=your_llm_api_key_here
   ZENROWS_API_KEY=your_zenrows_api_key_here
   ```

   Replace the placeholder values with your actual API keys.

## Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn server:app --reload
```

The API will be accessible at [http://localhost:8000](http://localhost:8000).

## API Endpoints

### GET `/`

**Description:**  
A simple health check endpoint.

**Response:**

```json
{
  "message": "Product Data Extraction API is running."
}
```

### POST `/search`

**Description:**  
Searches for product data based on a query, processes relevant document chunks, and returns structured product details.

**Request Body Example:**

```json
{
  "query": "latest smartphone deals in Saudi Arabia"
}
```

**Response Example:**

```json
{
  "results": [
    {
      "product_name": "Smartphone XYZ - 128GB, Black",
      "price": 999.99,
      "currency": "SAR",
      "vat_status": "after vat",
      "payment_type": "one time payment",
      "source": "https://example.com/product-page"
    }
    // ... more products
  ]
}
```

If no matching documents or valid data are found, the API returns an appropriate HTTP error.

## Code Structure

- **`server.py`**: Main entry point of the FastAPI application, defining endpoints and request handling.
- **`config.py`**: Contains configuration variables, including API keys, URLs, and settings.
- **`model.py`**: Initializes the ChatGroq LLM and defines functions to process queries and extract product data.
- **`util.py`**: Provides utility functions for HTML cleaning, conversion, and text processing using Selenium or ZenRows.

## Customization

### Switching Between Selenium and ZenRows

By default, HTML content is fetched using Selenium. To use ZenRows instead, modify the method parameter in the `clean_text` function:

```python
text_content = clean_text(url, method="zenrows")
```

### Adjusting the LLM Settings

The LLM is initialized in the `initialize_llm` function (in `model.py`) using default parameters. You can customize the temperature, model name, or other settings as needed.

## Troubleshooting

- **Selenium Issues:**  
  Ensure that ChromeDriver is installed and is compatible with your version of Google Chrome. Also, verify that ChromeDriver is accessible in your system's PATH.

- **API Key Errors:**  
  Double-check your `.env` file to make sure that all API keys (`SERPER_API_KEY`, `LLM_API_KEY`, and `ZENROWS_API_KEY`) are correctly set.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

