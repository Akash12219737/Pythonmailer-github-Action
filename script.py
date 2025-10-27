import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_mail(workflow_name, repo_name, workflow_run_id):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    if not all([sender_email, sender_password, receiver_email]):
        print(" Missing email credentials! Check your GitHub Secrets.")
        return

    subject = f"Workflow {workflow_name} failed for repo {repo_name}"
    body = (
        f"Hi,\n\n"
        f"The workflow '{workflow_name}' failed for the repository '{repo_name}'.\n"
        f"Please check the logs for more details.\n\n"
        f"Run ID: {workflow_run_id}\n"
    )

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(" Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

send_mail(
    os.getenv("WORKFLOW_NAME"),
    os.getenv("REPO_NAME"),
    os.getenv("WORKFLOW_RUN_ID")
)
