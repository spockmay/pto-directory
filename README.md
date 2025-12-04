# PTO Directory

These scripts are tools to help me manage the creation of the Kenston PTO Directory as well as automate some of the interactions with advertisers.

## Installation
Clone the repo locally and install the various modules with
```
pip install -r requirements.txt   
```

## directory.py
This code takes an xls file from the Board of Education and produces an xls file that is structured correctly for the printer. After generating the output xls you still have to manually review the data to mark split families as well as making sure that none of the automations went amok.
As an interim step, a sqlite database is generated with a cleaned version of the BOE data.

To use:
1. Place the xls file from the BOE into the input folder.
2. Update the value of `source_excel` with the name of the file.
3. Run the Python code
4. The output xls file will be stored at the location specified by `final_output`

## initial_advertiser_email.py
This code is used at the start of the advertiser season to send an email to previous or new advertisers to gauge their interest in running an ad. 

To use:
1. Update the config.ini file with the proper credentials to send emails
2. Download the Directory Sponsors Google Sheet as a csv file and place it in the input folder
3. Update the value of the argument passed to the `load_csv_to_dict_list` function with the name of the file
4. Set `TEST_RUN` to `True`
5. Run the script, validate that the output is structure the way you want. If you want to change the body of the emails, that is done in the `body` variables in `generate_email_body`
6. When ready to actually send the email, test your credentials by running the `util/send_email.py` script. Make sure the email sends as expected.
7. Change `TEST_RUN` to `False` and run the script. The sent emails will appear in your Gmail Sent mail folder.

## create_invoices.py
This code is used to generate invoices for each of the advertisers that purchased an ad. 

To use:
1. Download the Directory Sponsors Google Sheet as a csv file and place it in the input folder
2. Update the value of the argument passed to the `load_csv_to_dict_list` function with the name of the file
3. Set the values of `INITIAL_INVOICE_NUM` and `DIRECTORY_YEAR` as desired.
4. Run the code. The invoice for each advertiser will appear in the `output` folder.

If you want to change the content of the invoice, you need to edit the `invoice_template.odt` file in the `util` directory. The template is filled using the [relatorio module](https://relatorio.readthedocs.io/en/latest/index.html).

Unfortunately once the invoices are generated they are all saved as .odt files. This is not ideal, as we'd prefer something like pdf. However, the conversion from odt to pdf is non-trivial. Instead you can open each file in LibreOffice and save as a pdf. Alternately you can select all the files, right click, and select Print to PDF. You have to then select where to save each file, but it is a little easier.
