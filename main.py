import sys
import os
from fastapi import FastAPI




#Quotation Module
from quotaion_module.servers.price_scrapper_server import router as price_router
from quotaion_module.servers.email_scrapper_server import router as email_router

from quotaion_module.servers.price_scraper_withUpdate import router as price_router2
from quotaion_module.servers.email_scraper_withUpdate import router as email_router2



app = FastAPI(title="Unified HR & Interview Management System")


url_port=os.getenv("url")
if not url_port:
    raise ValueError("url environment variable is not set.")

#Quotation Module
app.include_router(price_router, prefix="/price_router", tags=["Price Scrpper APIs"])
app.include_router(email_router, prefix="/email_router", tags=["Email Scrpper APIs"])

app.include_router(price_router2, prefix="/price_router2", tags=["Price Scrpper APIs"])
app.include_router(email_router2, prefix="/email_router2", tags=["Email Scrpper APIs"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Combined API!"}
if __name__ == "__main__":
    # job_info,job_info_dup = collect_job_information()
    # print("Job Info", job_info)
    # print("Job Info Dup", job_info_dup)
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9100, reload=True)