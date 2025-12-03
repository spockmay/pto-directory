from relatorio.templates.opendocument import Template
from os.path import abspath, dirname, join
from datetime import datetime

from util.loader import load_csv_to_dict_list


def write_invoice_odt(invoice_num, years, advertiser):
    company = advertiser["Sponsor"].replace(".", "").strip()
    physical_size = '1" x 3"'  # TODO
    ad_recvd_text = advertiser["Ad Recvd"]  # TODO

    # TODO: some way to note that customer has already paid

    # https://relatorio.readthedocs.io/en/latest/index.html
    o = {
        "invoice_number": invoice_num,
        "invoice_date": datetime.now().strftime("%m/%d/%Y"),
        "advertiser_contact": advertiser["Contact"],
        "advertiser_name": company,
        "advertiser_address": advertiser["Address"],
        "years": years,
        "ad_size": advertiser["Size"],
        "ad_location": advertiser["Place"],
        "ad_color": "color" if advertiser["Color"] == "Y" else "black & white",
        "ad_recvd": ad_recvd_text,
        "ad_physical_size": physical_size,
        "ad_cost": advertiser["Cost"],
    }
    pwd = dirname(__file__)
    print("* generating invoice for %s... " % company, end="")
    template = Template(
        source="", filepath=abspath(join(pwd, "util/invoice template.odt"))
    )
    content = template.generate(o=o).render().getvalue()

    # output file name: <INVOICE NUMBER> <ADVERTISER NAME> <YEARS> invoice
    output_filename = "output/%s %s %s.odt" % (invoice_num, company, years)
    open(join(pwd, output_filename), "wb").write(content)
    print("done")


if __name__ == "__main__":
    # load the advertiser csv file
    advertisers = load_csv_to_dict_list(
        "input/Directory Sponsors - Sheet1.csv"
    )

    INITIAL_INVOICE_NUM = 4000

    # for each advertiser that has a value in Ad Recvd column
    invoice_num = INITIAL_INVOICE_NUM
    for advertiser in advertisers:
        write_invoice_odt(invoice_num, "2025-26", advertiser)
        invoice_num += 1
