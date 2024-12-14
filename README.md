# fetch-mojeuslugi-play-pl-invoices
Fetch invoices from mojeuslugi.play.pl and saves them as PDF files

## Usage

```bash
$ python index.py -h
usage: index.py [-h] [--base-url BASE_URL] --token TOKEN [--amount AMOUNT] [--output OUTPUT]

Fetch invoices from mojeuslugi.play.pl and saves them as PDF files

options:
  -h, --help           show this help message and exit
  --base-url BASE_URL  base URL for mojeuslugi.play.pl API, default is https://mojeuslugi.play.pl
  --token TOKEN        for mojeuslugi.play.pl API
  --amount AMOUNT      amount of bills to fetch, default is 17
  --output OUTPUT      output directory, default is relative directorty invoices/
```

1. Install required Python version from `.python-version` file
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Copy the JSON Web Token from the browser:
   1. Chrome:
      1. Open the Developer Tools (F12)
      2. Go to the "Network" tab
      3. Select the "Fetch/XHR" filter
      4. Copy the value of the "Authorization: Bearer" header
4. Run the script:
```bash
python index.py --token "<your_token>"
```
