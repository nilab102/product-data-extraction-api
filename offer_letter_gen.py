import markdown
from datetime import datetime

api_response = {
    "final_offer_letter": "**Employment Offer Letter**\n\nEsap ai  \n123 Innovation Drive, Tech City, TC 98765  \nJane Doe, Senior HR Manager  \nContact: jane.doe@esapai.com | +1-555-123-4567  \n\n**Subject:** Employment Offer for John Smith\n\nDear John Smith,\n\nWe are pleased to extend an offer for the position of **Python Developer** at Esap ai. We are confident that your skills and experience will be valuable to our team.\n\n**Position Details:**\n- **Employment Type:** Full-time\n- **Work Scope:** \n  - Design, develop, and maintain AI-driven products using Python programming language.\n  - Collaborate with cross-functional teams to identify and prioritize project requirements.\n  - Develop and implement efficient algorithms and data structures to ensure optimal performance.\n  - Troubleshoot and debug code to ensure high-quality deliverables.\n  - Stay up-to-date with industry trends and best practices in Python development.\n\n**Compensation:**\n- **Salary:** $80,000.00 per annum\n- **Bonuses:** Eligible for annual performance-based bonuses, subject to company policy and individual performance.\n\n**Benefits & Perks:**\n- **Health Insurance:** Comprehensive health insurance plan.\n- **Retirement Plan:** 401(k) with a matching contribution of up to 3%.\n- **Paid Time Off (PTO):** 20 days per year, plus holidays.\n- **Professional Development:** Access to training and development programs.\n\n**Contract Terms:**\n- **Confidentiality Clause:** Employee agrees not to disclose proprietary information during or after employment.\n- **Non-Compete Duration:** 12 months post-termination\n- **Probationary Period:** 3 months\n- **Notice Period:** 30 days\n- **Remote Work Policy:** Hybrid (3 days remote, 2 days in-office)\n\n**Legal Considerations:**\n- **Background Check Required:** Yes\n- **Reference Check Required:** No\n- **Compliance Note:** Must comply with GDPR and local labor laws\n\nPlease review this offer and confirm your acceptance by signing and returning a copy of this letter within two business days. If you have any questions, feel free to reach out.\n\nWe look forward to welcoming you to our team!\n\nSincerely,\n\nJane Doe  \nSenior HR Manager  \nEsap ai  \n\n[Signature]  \nJohn Smith\n\n---\n\n**Note:** Please sign and return a copy of this letter by [Response Deadline].",
    "candidate_mail": "johndoe@example.com"
}
# Convert Markdown to HTML with proper list handling
offer_html = markdown.markdown(api_response["final_offer_letter"], 
                             extensions=['markdown.extensions.sane_lists',
                                         'markdown.extensions.nl2br'])


time = datetime.now().strftime("%A, %B %d, %Y")

# Build HTML template with enhanced styling
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Employment Offer Letter</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      margin: 0;
      padding: 0;
    }}
    
    .container {{
      max-width: 800px;
      margin: 0 auto;
      padding: 40px;
      border: 1px solid #ddd;
      border-radius: 10px;
      background: #fff;
    }}
    
    .header {{
      text-align: center;
      margin-bottom: 30px;
      padding-bottom: 20px;
      border-bottom: 1px solid #eee;
    }}
    
    .header img {{
      max-width: 200px;
      height: auto;
      margin-bottom: 15px;
    }}
    
    h1 {{
      color: #2c3e50;
      margin-top: 0;
    }}
    
    h2 {{
      color: #2c3e50;
      border-bottom: 2px solid #eee;
      padding-bottom: 5px;
      margin-top: 30px;
    }}
    
    ul {{
      list-style-type: disc;
      margin-left: 25px;
      margin-bottom: 15px;
    }}
    
    ul ul {{
      list-style-type: circle;
      margin-left: 25px;
      margin-top: 5px;
    }}
    
    .signature {{
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #eee;
      line-height: 1.2;
    }}
    
    .footer-note {{
      font-size: 0.9em;
      color: #777;
      margin-top: 20px;
      padding-top: 15px;
      border-top: 1px dashed #ddd;
    }}
    
    /* Print-specific styles */
    @media print {{
      body {{
        font-size: 12pt;
      }}
      
      .container {{
        max-width: 100%;
        padding: 20px;
        border: none;
        box-shadow: none;
      }}
      
      .header img {{
        display: none;
      }}
      
      .footer-note {{
        border-top: 1px solid #000;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="https://static.wixstatic.com/media/630bc7_735bc25dffe645ed99a04c3bff90ec28~mv2.png" alt="Company Logo">
      <p>{time}</p>
    </div>
    
    <div class="content">
      {offer_html}
    </div>
  </div>
</body>
</html>
"""

# Write HTML to file
with open("offer_letter.html", "w", encoding="utf-8") as file:
    file.write(html_template)

print("Offer letter generated successfully as offer_letter.html")


