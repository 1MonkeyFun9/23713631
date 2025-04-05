import requests
from bs4 import BeautifulSoup

# Send a request to the page
url = "https://www.24h.com.vn/gia-vang-hom-nay-c425.html"
response = requests.get(url)

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find the table containing the gold prices
table = soup.find("table", class_="gia-vang-search-data-table")

# Find all rows in the table (each row contains data for one gold brand)
rows = table.find_all("tr")

# Iterate through each row and extract the gold brand and prices
for row in rows:
    # Extract the gold brand name
    gold_brand = row.find("h2")
    if gold_brand:
        print(f"Gold Brand (HTML): {str(gold_brand)}")

        # Extract the prices for today and yesterday
        cells = row.find_all("td")
        if len(cells) >= 5:  # Ensure there are enough cells
            today_buy = str(cells[1]).strip()
            today_sell = str(cells[2]).strip()
            yesterday_buy = str(cells[3]).strip()
            yesterday_sell = str(cells[4]).strip()

            # Print the extracted data with HTML tags
            print(f"Buy Price Today (HTML): {today_buy}")
            print(f"Sell Price Today (HTML): {today_sell}")
            print(f"Buy Price Yesterday (HTML): {yesterday_buy}")
            print(f"Sell Price Yesterday (HTML): {yesterday_sell}")
            print("-" * 40)
