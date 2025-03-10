from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
import smtplib
import ssl
from email.message import EmailMessage
import os
import markdown
from datetime import datetime
from fastapi import FastAPI
router = APIRouter()

class OfferRequest(BaseModel):
    final_offer_letter: str
    candidate_mail: str

app = FastAPI(title="Unified HR & Interview Management System")
@app.post("/send_email_with_offer")
async def generate_and_send_offer(request: OfferRequest):
    try:
        # Generate HTML from Markdown
        offer_html = markdown.markdown(
            request.final_offer_letter,
            extensions=['markdown.extensions.sane_lists', 'markdown.extensions.nl2br']
        )
        current_time = datetime.now().strftime("%A, %B %d, %Y")

        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Employment Offer Letter</title>
          <style>
            /* Include your CSS styles here */
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

        # Send email
        email_sender = os.getenv('EMAIL_SENDER', 'nilabaust102@gmail.com')
        email_password = os.getenv('EMAIL_PASSWORD', 'gaih vjfq zelf zxey')

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = request.candidate_mail
        em['Subject'] = 'Employment Offer Letter'
        em.add_alternative(html_template, subtype='html')

        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(email_sender, email_password)
            server.send_message(em)

        return {"status": "success", "message": "Email sent successfully"}

    except smtplib.SMTPAuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="SMTP Authentication Failed"
        )
    except smtplib.SMTPException as e:
        raise HTTPException(
            status_code=500,
            detail=f"SMTP Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("email_send_api:app", host="0.0.0.0", port=8000, reload=True)