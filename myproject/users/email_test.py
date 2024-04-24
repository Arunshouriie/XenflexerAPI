# # Test email script
import smtplib
from email.mime.text import MIMEText

# Prepare the email
msg = MIMEText("This is a test email body.")
msg["Subject"] = "Test Email"
msg["From"] = "arunshowriinguva@gmail.com"
msg["To"] = "nilesh.71450@gmail.com"

# SMTP configuration
smtp_server = "smtp.gmail.com"  # Your SMTP server
smtp_port = 587  # Port for TLS
smtp_user = "arunshowriinguva@gmail.com"  # SMTP login
smtp_password = "ihrj rmai nipp uamw"  # SMTP password

# Initialize the SMTP server instance
server = None

try:
    server = smtplib.SMTP(smtp_server, smtp_port)  # Connect to the SMTP server
    server.starttls()  # Upgrade connection to TLS
    server.login(smtp_user, smtp_password)  # Log in to SMTP
    server.sendmail("arunshowriinguva@gmail.com", "nilesh.71450@gmail.com", msg.as_string())  # Send email
    print("Email sent successfully!")
except Exception as e:
    print("Error sending email:", e)  # Handle exceptions
finally:
    if server:  # Check if server was initialized
        server.quit()  # Ensure server is closed






# import smtplib
# from email.mime.text import MIMEText

# msg = MIMEText("Test email body")
# msg["Subject"] = "Test Email"
# msg["From"] = "arunshowriinguva@gmail.com"
# msg["To"] = "arun.inguva@coherencehealth.ai"

# # SMTP configuration
# smtp_server = "smtp.gmail.com"
# smtp_port = 465
# smtp_user = "arunshowriinguva@gmail.com"
# smtp_password = "ihrj rmai nipp uamw"

# try:
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()  # Start TLS
#     server.login(smtp_user, smtp_password)  # Login
#     server.sendmail("arunshowriinguva@gmail.com", ["arun.inguva@coherencehealth.ai"], msg.as_string())
#     print("Email sent successfully!")
# except Exception as e:
#     print("Error:", e)
# finally:
#     server.quit()
