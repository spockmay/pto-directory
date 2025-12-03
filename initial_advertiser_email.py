import configparser

from util.send_email import send_mail
from util.loader import load_csv_to_dict_list


def generate_email_body(advertiser):
    last_year = advertiser["Last Year"]
    color = "color" if advertiser["Color"] == "Y" else "black & white"

    if last_year == "Y":
        body = (
            "Hello %s,<br><br>"
            "I hope this email finds you doing well and enjoying this beautiful start to fall. Now that the students (and families!) are settled into their school routine we are beginning work on the 2025-2026 Kenston Parent/Student Directory. As you know, the Kenston PTO funds this book every year to provide a copy to all the families in the district.<br>"
            "We would like to know if you are interested in placing an ad for %s in the Kenston School Directory again this year. You placed a %s page %s ad on the %s of the directory last year at a cost of %s. Prices are the same for this year. If you would like to change the ad, please just let us know. New artwork would be needed by October 17th.<br>"
            "Whether you are interested or not, if you could please let us know at your earliest convenience, we would appreciate it.<br><br>"
            "Thanks for your continuing support!<br>"
            "Ryan May<br>"
            "Kenston PTO<br>"
            "pto.directory@kenstonapps.org<br>"
            "17419 Snyder Rd, Chagrin Falls, OH 44023"
            % (
                advertiser["Contact"],
                advertiser["Sponsor"],
                advertiser["Size"],
                color,
                advertiser["Place"],
                advertiser["Cost"],
            )
        )
    else:
        body = (
            "Hello %s,<br>"
            "As a representative for the Kenston Local School District PTO, I am reaching out to see if you would be interested in placing an advertisement in the Kenston Student/Parent Directory this year. We are currently looking for new advertisers to help support the directory and keep it fresh and new.<br>"
            "As always, this year's book will contain information on all 2,000 Kenston families with kids in preschool through 12th grade.  We will distribute one FREE book to each Kenston family, plus one to each faculty member, school board member, as well as the staff of Kenston Community Education. We produce one book each year in the fall and most families rely heavily on it, using the information frequently throughout the year.<br><br>"
            "Our ad rates are as follows for our directory which measures 8½” x 5½”:<br>"
            " - A quarter-page inside the book (2” x 5 ¼”) = $200 (or color for $250)<br>"
            " - A half page inside the book or a half page inside the back cover (3 ¾” x 5 ¼”) = $300 (or color for $350)<br>"
            " - The whole inside of the back cover, or a whole page inside the book (8” x 5 ¼”) = $500 (or color for $550)<br>"
            " - The whole back cover or inside the front cover (8” x 5 ¼”) = $600 (or color for $650)<br>"
            "Please note: Some of these spots may already be taken by last year's advertisers, who have first choice of placement this year.<br>"
            "Payment is due within 30 days of receiving our invoice.<br><br>"
            "We are looking to finalize advertising space soon and would love to add your business to the directory.<br><br>"
            "We look forward to working with you and thank you for supporting the Kenston Local School District.<br>"
            "Ryan May<br>"
            "Kenston PTO<br>"
            "pto.directory@kenstonapps.org<br>"
            "17419 Snyder Rd, Chagrin Falls, OH 44023"
            % (advertiser["Contact"],)
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

    for advertiser in advertisers:
        body = generate_email_body(advertiser)
        subject = "Kenston PTO Directory Advertisement"
        to = advertiser["Email"]

        if TEST_RUN:
            print("%s<br>%s<br>%s" % (to, subject, body))
            print("---------------------------------------")
        else:
            print("Emailing %s" % (to))
            if send_mail(body, subject, to, secrets):
                print("  Success!")
            else:
                print("  Failure!!!!!")
