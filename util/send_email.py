import smtplib
import configparser

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_mail(
    text: str, subject: str, to: str, secrets: dict, filenames=[]
) -> bool:
    """
    Send an email from a Gmail account.

    :param text: The body text of the email you will send
    :type text: str
    :param subject: email subject, keep short
    :type subject: str
    :param to: a semicolon delimited string of email addresses
    :type to: str
    :param secrets: a dict with from_address, user, password keys
    :type secrets: dict
    :param filenames: a list of files to attach to the email
    :type filenames: list
    :return: success sending the email
    :rtype: bool
    """
    msg = MIMEMultipart()
    msg["From"] = secrets["from_address"]
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(text, "plain"))

    # attach any files
    for filename in filenames:
        attachment = open(filename, "rb")
        clean = filename.split("/")[-1]

        p = MIMEBase("application", "octet-stream")

        # To change the payload into encoded form
        p.set_payload(attachment.read())

        encoders.encode_base64(p)

        p.add_header("Content-Disposition", "attachment; filename= %s" % clean)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

    gmail_user = secrets["user"]
    gmail_password = secrets["password"]

    # send the email
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        # sending the mail
        server.sendmail(gmail_user, to, msg.as_string())

        # terminating the session
        server.quit()
        return True
    except Exception as e:
        print("Something went wrong: %s" % e)
        return False


if __name__ == "__main__":
    # load the config file's settings
    config = configparser.ConfigParser()
    config.read("config_secrets.ini")
    secrets = dict(config["send_email"])

    # send test email
    SEND_TO = "YOUR@EMAIL.COM"
    send_mail(
        "hi there, this is a test!",
        "testing 1 2 3",
        SEND_TO,
        secrets,
    )
