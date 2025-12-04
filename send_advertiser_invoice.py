import configparser

from util.send_email import send_mail
from util.loader import load_csv_to_dict_list


def generate_email_body(advertiser):
    body = (
        f"Hi {advertiser['Contact']},\n"
        f"Thank you for your support of the Kenston PTO Directory!\n"
        f"Attached you will find the invoice for r ad.\n"
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

    advertisers = load_csv_to_dict_list(
        "input/Directory Sponsors - Sheet1.csv"
    )

    for advertiser in advertisers[0:1]:
        body = generate_email_body(advertiser)
        subject = "Kenston PTO Directory Advertisement - Invoice"
        to = advertiser["Email"]

        if TEST_RUN:
            print("%s\n%s\n%s" % (to, subject, body))
            print("---------------------------------------")
        else:
            print("Emailing %s" % (to))
            if send_mail(body, subject, to, secrets):
                print("  Success!")
            else:
                print("  Failure!!!!!")
