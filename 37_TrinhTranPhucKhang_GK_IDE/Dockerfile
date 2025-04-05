# Sử dụng image Python chính thức
FROM python:3.8-slim

# Đặt thư mục làm việc
WORKDIR /app

# Cài đặt các thư viện cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn vào trong container
COPY . .

# Chạy ứng dụng khi container khởi động
CMD ["python", "your_script.py"]
