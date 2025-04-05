import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

# -------------------------------------
# Cấu hình kết nối PostgreSQL
# -------------------------------------
DB_CONFIG = {
    "host": "localhost",     # nếu chạy trong container Airflow thì dùng 'postgres'
    "port": 5432,
    "user": "airflow",
    "password": "airflow",
    "database": "airflow"
}

# -------------------------------------
# Hàm tạo bảng nếu chưa tồn tại
# -------------------------------------
def create_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_prices (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            brand TEXT,
            today_buy NUMERIC,
            today_sell NUMERIC,
            yesterday_buy NUMERIC,
            yesterday_sell NUMERIC
        );
    """)

# -------------------------------------
# Hàm lưu dữ liệu vào PostgreSQL
# -------------------------------------
def insert_data(cur, data):
    cur.execute("""
        INSERT INTO gold_prices (timestamp, brand, today_buy, today_sell, yesterday_buy, yesterday_sell)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, data)

# -------------------------------------
# Crawl và lưu dữ liệu
# -------------------------------------
def crawl_and_store():
    url = "https://www.24h.com.vn/gia-vang-hom-nay-c425.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="gia-vang-search-data-table")
    rows = table.find_all("tr")
    timestamp = datetime.now()

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    create_table(cur)

    for row in rows:
        gold_brand = row.find("h2")
        if gold_brand:
            brand = gold_brand.text.strip()
            try:
                cols = row.find_all("td")
                today_buy = float(cols[1].text.strip().split("\n")[0].replace(",", ""))
                today_sell = float(cols[2].text.strip().split("\n")[0].replace(",", ""))
                yesterday_buy = float(cols[3].text.strip().replace(",", ""))
                yesterday_sell = float(cols[4].text.strip().replace(",", ""))

                insert_data(cur, (timestamp, brand, today_buy, today_sell, yesterday_buy, yesterday_sell))

                print(f"✅ Lưu: {brand}")
            except Exception as e:
                print(f"⚠️ Lỗi khi xử lý {brand}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Đã lưu toàn bộ dữ liệu vào PostgreSQL.")

if __name__ == "__main__":
    crawl_and_store()