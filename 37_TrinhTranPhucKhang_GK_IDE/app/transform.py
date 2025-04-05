import requests
from bs4 import BeautifulSoup

# Gửi yêu cầu đến trang web
url = "https://www.24h.com.vn/gia-vang-hom-nay-c425.html"
response = requests.get(url)

# Phân tích nội dung bằng BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Tìm bảng chứa giá vàng
table = soup.find("table", class_="gia-vang-search-data-table")

# Tìm tất cả các dòng trong bảng (mỗi dòng chứa thông tin của một thương hiệu vàng)
rows = table.find_all("tr")

# Duyệt qua từng dòng và lấy thông tin của từng thương hiệu vàng
for row in rows:
    # Lấy tên thương hiệu vàng
    gold_brand = row.find("h2")
    if gold_brand:
        gold_brand = gold_brand.get_text(strip=True)

        # Lấy các giá trị hôm nay và hôm qua
        cols = row.find_all("td")
        if len(cols) > 4:
            today_buy = cols[1].get_text(strip=True).replace(",", "")
            today_sell = cols[2].get_text(strip=True).replace(",", "")
            yesterday_buy = cols[3].get_text(strip=True).replace(",", "")
            yesterday_sell = cols[4].get_text(strip=True).replace(",", "")

            # In ra dữ liệu đã làm sạch
            print(f"Thương hiệu vàng: {gold_brand}")
            print(f"Giá mua hôm nay: {today_buy} VND")
            print(f"Giá bán hôm nay: {today_sell} VND")
            print(f"Giá mua hôm qua: {yesterday_buy} VND")
            print(f"Giá bán hôm qua: {yesterday_sell} VND")
            print("-" * 40)
