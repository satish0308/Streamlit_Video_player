import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Specify the path to your .config file
load_dotenv(dotenv_path=".config")

# Now you can access the variables using os.getenv
var1 = os.getenv("SENDER_EMAIL")
var2 = os.getenv("RECIEVER_EMAIL")
var3=os.getenv("APP_PASSWORD")


def send_email(subject, body, to_email):
    # Your email credentials
    from_email = var1
    password = var3  # or app password if 2FA enabled

    # SMTP server configuration for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # TLS port

    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server using TLS encryption
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection using TLS

        # Login to the server
        server.login(from_email, password)

        # Send email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        server.quit()

# Usage
if __name__ == '__main__':
    send_email(
        subject="Test Subject v3",
        body="This is a test email body.",
        to_email=var2
    )
