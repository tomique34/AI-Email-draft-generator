import os
import openai
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model='Meta-Llama-3.1-8B-Instruct',
    messages=[{"role":"user",
               "content":"Draft an email following up with a customer"},
              {"role":"assistant",
               "content":"Here's a sample email:\n\nSubject: Follow-up on Your Inquiry/Order\n\nDear [Customer's Name],\n\nI hope this email finds you well. I am writing to follow up on your [inquiry/order] that we received on [Date]. We appreciate the interest you have shown in our [product/service] and would like to ensure that you have all the information you need to move forward.\n\nAs a quick recap, we discussed [briefly mention the details of the inquiry or order, including any specific requirements or concerns the customer had]. We believe that our [product/service] would be a great fit for your [specific need or goal], and we would be happy to answer any additional questions you may have.\n\nIf you are ready to proceed, please let us know and we will guide you through the next steps. If you have any further questions or concerns, please don't hesitate to reach out. We are here to help.\n\nAlternatively, if you would like to schedule a call to discuss your [inquiry/order] in more detail, please let us know a convenient time and date for you, and we will make sure to schedule it accordingly.\n\nThank you for considering our [product/service]. We look forward to hearing back from you soon.\n\nBest regards,\n\n[Your Name]\n[Your Company]\n[Contact Information]\n\nThis is just a sample email, and you can modify it to fit your specific needs and the tone you want to convey. Remember to include the following:\n\n* A clear subject line that indicates the purpose of the email\n* A personalized greeting and introduction\n* A brief summary of the customer's inquiry or order\n* An offer to answer any additional questions or concerns\n* A clear call-to-action (e.g. scheduling a call or proceeding with the order)\n* A professional closing and signature\n\nFeel free to adjust the email to fit your company's brand and voice."}],
    temperature =  0.1,
    top_p = 0.1
)

print(response.choices[0].message.content)
      