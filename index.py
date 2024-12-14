import argparse
import os
import requests
import sys

parser = argparse.ArgumentParser(
    description="Fetch invoices from mojeuslugi.play.pl and saves them as PDF files"
)
parser.add_argument(
    "--base-url",
    required=False,
    help="base URL for mojeuslugi.play.pl API, default is https://mojeuslugi.play.pl",
    default="https://mojeuslugi.play.pl",
)
parser.add_argument("--token", required=True, help="user tohen for mojeuslugi.play.pl API")
parser.add_argument(
    "--amount", required=False, help="amount of bills to fetch, default is 17", default=17
)
parser.add_argument(
    "--output",
    required=False,
    help="output directory, default is relative directorty invoices/",
    default="invoices",
)

args = parser.parse_args()
base_url = args.base_url
token = args.token
amount = args.amount
output = args.output

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": None,  # Explicitly set User-Agent to None to omit it
}
params = {"amount": amount}
bill_history_response = requests.get(
    f"{base_url}/api/invoice/client/bill-history", headers=headers, params=params
)

if bill_history_response.status_code == 200:
    bill_history = bill_history_response.json()["billHistoryPayment"]
    for bill_key, bill_value in bill_history.items():
        invoice_id = bill_value["invoiceId"]
        invoice_number = bill_value["invoiceNumber"]
        status = bill_value["status"]
        invoice_date = bill_value["invoiceDate"]
        pay_due_date = bill_value["payDue"]
        print(
            f"Invoice ID: {invoice_id}, Invoice number: {invoice_number}, "
            f"Status: {status}, Invoice date: {invoice_date}, Pay due date: {pay_due_date}"
        )

        invoice_response = requests.get(
            f"{base_url}/api/invoice/client/invoice-pdf/{invoice_id}", headers=headers
        )
        if invoice_response.status_code == 200:
            content_disposition = invoice_response.headers.get("content-disposition")
            directory_name = f"{output}/{bill_key}"
            if os.path.exists(directory_name):
                print(f"Directory {directory_name} already exists, skipping")
                continue
            if content_disposition:
                if not os.path.exists(directory_name):
                    os.makedirs(directory_name)
                filename = content_disposition.split("filename=")[-1].strip('"')
                filepath = os.path.join(directory_name, filename)
                with open(filepath, "wb") as file:
                    file.write(invoice_response.content)
                print(f"Downloaded {filepath}")
            else:
                print(
                    "ERROR: Filename not found in content-disposition header for invoice",
                    invoice_id,
                    file=sys.stderr,
                )
        else:
            print(
                f"ERROR: Failed to download PDF for invoice {invoice_id}: ",
                f"{invoice_response.status_code} ",
                invoice_response.text,
                file=sys.stderr,
            )
else:
    print(
        f"ERROR: Failed to fetch bill history: {bill_history_response.status_code} ",
        bill_history_response.text,
        file=sys.stderr,
    )
