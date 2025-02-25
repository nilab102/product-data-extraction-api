
from fastapi import FastAPI, HTTPException


# FastAPI app initialization
app = FastAPI(title="Product Data Extraction API")

from servers.price_scrapper_server import router as price_router

app.include_router(price_router, prefix="/price_router", tags=["Price Scrpper APIs"])


from servers.email_scrapper_server import router as email_router

app.include_router(email_router, prefix="/email_router", tags=["Email Scrpper APIs"])

@app.get("/")
async def root():
    return {"message": "Product Data Extraction & Email Extraction API is running."}

# To run via: uvicorn server:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
