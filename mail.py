import smtplib
from email.message import EmailMessage


SUPPORT_EMAIL_ADDRESS = 'adhd.treatment.braude@gmail.com'
SUPPORT_EMAIL_PASSWORD = 'vnqwwnmmdunqvfyv'

# When will be deployed - change to tth address of deployment
URL = f"http://127.0.0.1:5000"
# URL = os.environ.get('ENV_HOST_ADDRESS')


def send_mail_notification(receiver_email, receiver_name):
    """
    Generates and sends automatic email notification to a customer
    Uses SMTP.gmail API
    Email created and sent from SUPPORT_EMAIL_ADDRESS
    The message contents Notification that file uploaded to storage
    or text string to DB, link to wideKey and expiration date

    :param receiver_email:  receiver email address
    :param receiver_name:

    :raises: SMTPException
    """
    mail_content = f'''        
        <h3><b><center>Hello, {receiver_name}.A new treatment program was shared with you.</center></b></h3><br>
        <center></center><br>

        <center><a href="{URL}">Click here </a> to view it.</center><br>

        <center>In order to access this program you have to login with your email address.<center><br>
        <center>Regards, Teaching stuff<center><br>
        '''

    sender_address = SUPPORT_EMAIL_ADDRESS
    sender_pass = SUPPORT_EMAIL_PASSWORD
    receiver_address = receiver_email

    message = EmailMessage()
    message.set_content(mail_content, subtype='html', charset='utf-8')
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'AHDH Program'  # The subject line

    try:
        # Create SMTP session for sending the mail
        mail_session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        mail_session.starttls()  # enable security
        mail_session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        mail_session.sendmail(sender_address, receiver_address, text)
        mail_session.quit()
    except smtplib.SMTPException as e:
        print(e)


if __name__ == '__main__':
    send_mail_notification("docmat63@gmail.com", "Nikita Matatov")