from relatorio.templates.opendocument import Template
from os.path import abspath, dirname, join
from datetime import datetime

from util.loader import load_csv_to_dict_list

SIZE_MAP = {
    "quarter": '2" x 5-1/4"',
    "half": '3-3/4" x 5-1/4"',
    "full": '8" x 5-1/4"',
}


def write_invoice_odt(invoice_num, years, advertiser):
    company = advertiser["Sponsor"].replace(".", "").strip()
    print("* generating invoice for %s... " % company, end="")

    ad_recvd_text = advertiser["Ad Recvd"]
    if ad_recvd_text == "":
        print("no sale")
        return False

    if ad_recvd_text == "last year":
        ad_recvd_text = "same ad copy as last year"
    else:
        ad_recvd_text = "ad as received on %s" % ad_recvd_text

    physical_size = SIZE_MAP[advertiser["Size"]]
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
    template = Template(
        source="", filepath=abspath(join(pwd, "util/invoice template.odt"))
    )
    content = template.generate(o=o).render().getvalue()

    # output file name: <INVOICE NUMBER> <ADVERTISER NAME> <YEARS> invoice
    output_filename = "output/%s %s %s.odt" % (invoice_num, company, years)
    open(join(pwd, output_filename), "wb").write(content)
    print(invoice_num)

    return True


if __name__ == "__main__":
    # load the advertiser csv file
    advertisers = load_csv_to_dict_list(
        "input/Directory Sponsors - Sheet1.csv"
    )

    INITIAL_INVOICE_NUM = 4000

    # for each advertiser that has a value in Ad Recvd column
    invoice_num = INITIAL_INVOICE_NUM
    for advertiser in advertisers:
        if write_invoice_odt(invoice_num, "2025-26", advertiser):
            invoice_num += 1
