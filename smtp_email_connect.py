import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    # Your email credentials
    from_email = "sadasdasda"
    password = "asdasda8"  # or app password if 2FA enabled

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
        subject="Test Subject",
        body="This is a test email body.",
        to_email="sadasdasdasd@gmail.com"
    )
