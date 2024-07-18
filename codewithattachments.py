import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from transformers import pipeline

# Setup port number and server name
smtp_port = 587  # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

# Set up the email details
email_from = "b.wassim.belhouene@gmail.com"
email_list = ["b.wassim.belhouene@gmail.com"]

# Define the password (use environment variables or other secure methods in real applications)
pswd = "avls anst tavd iwyt"  # Replace with your actual password

# Name the email subject
subject = "Thank You for Your Help"

# Initialize the text generation pipeline using GPT-Neo
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

def generate_email_body(prompt):
    # Generate text using the pipeline
    result = generator(prompt, 
                       max_length=300, 
                       num_return_sequences=1, 
                       temperature=0.7, 
                       top_p=0.9, 
                       truncation=True, 
                       pad_token_id=50256)  # Explicitly set pad_token_id

    text = result[0]['generated_text']

    # Ensure the email text is coherent
    if "Thank you" not in text:
        text = f"{text}\n\nThank you for your assistance. I really appreciate your help. I am very happy with the results. I would like to thank you again.\n\n-Mike"
    return text.strip()

# Define the email function
def send_emails(email_list, subject, body, filename):
    for person in email_list:
        # Create the email object
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(body, 'plain'))

        # Open and attach the file
        try:
            with open(filename, 'rb') as attachment:
                attachment_package = MIMEBase('application', 'octet-stream')
                attachment_package.set_payload(attachment.read())
                encoders.encode_base64(attachment_package)
                attachment_package.add_header('Content-Disposition', f"attachment; filename={filename}")
                msg.attach(attachment_package)
        except FileNotFoundError:
            print(f"The file {filename} was not found.")
            continue

        # Send the email
        text = msg.as_string()
        print("Connecting to the server...")
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as TIE_server:
                TIE_server.starttls()
                TIE_server.login(email_from, pswd)
                print("Successfully connected to the server")
                print()

                print(f"Sending email to: {person}...")
                TIE_server.sendmail(email_from, person, text)
                print(f"Email sent to: {person}")
                print()
        except Exception as e:
            print(f"Failed to send email to {person}. Error: {e}")

# Define the prompt for generating the email body
prompt = (
    "Write a detailed thank-you email to my friend Malek for his help with a recent project. "
    "Mention his specific contributions, such as his advice on project planning, his technical assistance, and his motivational support. "
    "Explain how his help contributed to the project's success and how the project is benefiting others in the community. "
    "Keep the tone personal and appreciative, and end with a strong note of gratitude. "
    "Make sure the email is well-structured and avoids repetition."
)

print("Generating the email body...")
body = generate_email_body(prompt)
print("Generated email body:")
print(body)

filename = "random_data.csv"  # Ensure this file exists in the same directory

# Run the function to send emails
send_emails(email_list, subject, body, filename)
