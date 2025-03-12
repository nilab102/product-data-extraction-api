from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import markdown
import ssl
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

quoatation_name = os.getenv("Quoatation_name")
if not quoatation_name:
    raise ValueError("base_url environment variable is not set.")

quoatation_email = os.getenv("Quoatation_email")
if not quoatation_email:
    raise ValueError("base_url environment variable is not set.")

quotation_company_name=os.getenv("Quoatation_company_name")
if not quoatation_email:
    raise ValueError("base_url environment variable is not set.")

# Define a Product model for each item in the product list.
class Product(BaseModel):
    name: str
    quantity: int

# Define a request model for the wholesale inquiry.
class WholesaleInquiryRequest(BaseModel):
    recipient_email: str  # Email address to which the inquiry will be sent
    product_list: List[Product]

@app.post("/send_wholesale_inquiry_email")
async def send_wholesale_inquiry(request: WholesaleInquiryRequest):
    try:
        # Build the Markdown content from the payload.
        product_lines = "\n".join(
            [f"- **{product.name}**: {product.quantity} units" for product in request.product_list]
        )
        markdown_content = f"""
Subject: Wholesale Price Inquiry from {quotation_company_name}

Hello,

My name is {quoatation_name} and I represent {quotation_company_name}. We are interested in obtaining wholesale pricing for the following products:

{product_lines}

Could you please provide us with your wholesale pricing, including any bulk order discounts, lead times, payment terms, and shipping details? We are looking to establish a long-term partnership and would appreciate any additional information you can offer.

Thank you for your time and consideration. I look forward to your prompt response.

Best regards,

{quoatation_name}
Esap AI  
{quoatation_email}
        """

        # Convert Markdown to HTML
        offer_html = markdown.markdown(
            markdown_content,
            extensions=['markdown.extensions.sane_lists', 'markdown.extensions.nl2br']
        )
        current_time = datetime.now().strftime("%A, %B %d, %Y")

        # HTML email template
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Wholesale Price Inquiry from Esap AI</title>
          <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .header img {{ width: 200px; }}
            .content {{ margin-top: 30px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <img src="https://static.wixstatic.com/media/630bc7_735bc25dffe645ed99a04c3bff90ec28~mv2.png" alt="Company Logo">
              <p>{current_time}</p>
            </div>
            <div class="content">
              {offer_html}
            </div>
          </div>
        </body>
        </html>
        """

        # Get email credentials from environment variables
        email_sender = os.getenv('EMAIL_SENDER', 'nilabaust102@gmail.com')
        email_password = os.getenv('EMAIL_PASSWORD', 'gaih vjfq zelf zxey')

        # Setup the email message
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = request.recipient_email
        em['Subject'] = 'Wholesale Price Inquiry from Esap AI'
        em.add_alternative(html_template, subtype='html')

        # Connect to the SMTP server and send the email
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(email_sender, email_password)
            server.send_message(em)

        return {"status": "success", "message": "Email sent successfully"}

    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="SMTP Authentication Failed")
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f"SMTP Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
@app.get("/")
async def root():
    return {"message": "Welcome to the Combined API!"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("quotation_make:app", host="0.0.0.0", port=9100, reload=True)