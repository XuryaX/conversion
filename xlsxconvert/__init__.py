import logging

import azure.functions as func
import pandas
import requests
from pandas.io.excel import ExcelWriter
from io import StringIO, BytesIO

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    url = req.params.get('url')
    if not url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            url = req_body.get('url')

    if url:
        binary_data = convert_url_to_xlsx(url)
        return func.HttpResponse(binary_data)
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )


def convert_url_to_xlsx(url):
    logging.info("URL: %s", url)
    
    csv_dataframe = pandas.read_csv(url)


    logging.info("Read CSV Successfully")


    with BytesIO() as output:
        with pandas.ExcelWriter(output, engine='xlsxwriter') as writer:
            logging.info("Start Conversion")
            csv_dataframe.to_excel(writer, sheet_name='WS Data')


        data = output.getvalue()

        logging.info("Conversion Started")



    return data
