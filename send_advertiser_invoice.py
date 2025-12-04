import configparser

from util.send_email import send_mail
from util.loader import load_csv_to_dict_list
from util.os_tools import find_pdf_files


def generate_email_body(advertiser):
    body = (
        f"Hi {advertiser['Contact']},\n"
        f"Thank you for your support of the Kenston PTO Directory!\n"
        f"Attached you will find the invoice for your ad.\n"
        f"Please let us know if you have any questions.\nThanks\n"
        f"Ryan May\n"
        f"Kenston PTO\npto.directory@kenstonapps.org\n17419 Snyder Rd, Chagrin Falls, OH 44023"
    )
    return body


if __name__ == "__main__":
    TEST_RUN = True

    # load the config file's settings
    config = configparser.ConfigParser()
    config.read("config.ini")
    secrets = dict(config["send_email"])

    invoices = find_pdf_files("output/")

    advertisers = load_csv_to_dict_list(
        "input/Directory Sponsors - Sheet1.csv"
    )

    for advertiser in advertisers[0:2]:
        body = generate_email_body(advertiser)
        subject = "Kenston PTO Directory Advertisement - Invoice"
        to = advertiser["Email"]

        # find the invoice pdf file to attach to the email
        invoice_num = advertiser["Invoice #"]
        invoice_fn = []
        if invoice_num:
            invoice_fn = [
                f"output/{x}" for x in invoices if x.startswith(invoice_num)
            ]
        if len(invoice_fn) > 1:
            raise ValueError(
                f"Too many pdf files found for invoice #{invoice_num}"
            )

        if TEST_RUN:
            print("%s\n%s\n%s\n%s" % (to, subject, body, invoice_fn))
            print("---------------------------------------")
        else:
            print("Emailing %s..." % (to), end="")
            if send_mail(body, subject, to, secrets, invoice_fn):
                print("Success!")
            else:
                print("Failure!!!!!")
