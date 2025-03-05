# Product Data Extraction API

This repository contains a **Product Data Extraction API** built with [FastAPI](https://fastapi.tiangolo.com/). It leverages multiple tools and services to search for product information online, clean and process HTML content, and extract structured product details using a language model.

## Features

- **Web Search Integration:** Uses the [Serper API](https://serper.dev/) to perform product-related searches.
- **Content Retrieval:** Fetches HTML content from web pages using either Selenium or [ZenRows](https://www.zenrows.com/).
- **HTML Cleaning & Conversion:** Cleans HTML content (removing headers, footers, ads, etc.) and converts it to Markdown for easier text processing.
- **Document Chunking:** Splits lengthy documents into smaller chunks for efficient processing.
- **Relevant Chunk Retrieval:** Uses BM25 retrieval (via Langchain) to select the most relevant document sections.
- **LLM-Powered Extraction:** Leverages a ChatGroq language model to extract product details based on a detailed prompt.
- **Structured Output:** Returns product details in JSON format, including fields such as `product_name`, `price`, `currency`, `vat_status`, `payment_type`, `features_of_product`,`customer_rating`,`vendor_name` and `source`.

## Prerequisites

- **Python 3.8+**
- [pip](https://pip.pypa.io/en/stable/)
- [Google Chrome](https://www.google.com/chrome/) (for Selenium-based fetching)
- [ChromeDriver](https://chromedriver.chromium.org/) (compatible with your installed version of Chrome)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/ESAP-Base-ERP/ESAP_HR_AI/tree/hr_merge_code
   cd ESAP_HR_AI
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
python main.py
```

The API will be accessible at [http://localhost:9100](http://localhost:9100).

## curl
curl -N -X POST http://127.0.0.1:9100/price_router/search -H "Content-Type: application/json" -d "{\"query\": \"Sony Bravia 55-inch 4K UHD Smart LED TV\"}"

## API Endpoints

### POST `/price_router/search`

**Description:**  
Searches for product data based on a query, processes relevant document chunks, and returns structured product details.

**Request Body Example:**

```json
{
  "query": "Sony Bravia 55-inch 4K UHD Smart LED TV"
}
```

**Response Example:**

```json
{
  "results": [
        {
            "product_name": "Sony Bravia 55-inch 4K UHD Smart LED TV, Google TV, KD55X75K; Built-in Wi-Fi, HDR, Bluetooth, Built-in Chromecast, Dolby Atmos",
            "price": 3850000,
            "currency": "UGX",
            "source": "https://www.abanista.com/product/sony-bravia-55-4k-uhd-smart-led-tv/?srsltid=AfmBOorX0onsM-58e9u666tubOB0kIiuJ8deILNRZvaLJRxgqDPxOuPl",
            "vat_status": "Not specified",
            "payment_type": "One time payment",
            "features_of_product": "4K Ultra HD LED Smart Google TV with Dolby Vision, Built-in Wi-Fi, HDR, Bluetooth, Built-in Chromecast, Dolby Atmos",
            "vendor_name": "Abanista",
            "customer_rating": "4.67 out of 5 based on 3 customer ratings"
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

