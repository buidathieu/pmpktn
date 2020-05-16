# Phần mềm phòng mạch tư

## Chức năng
- Database bằng SQLite, dễ dàng chỉnh sửa bằng tools như sqlstudio,..
- Tạo toa mẫu và ra toa nhanh chóng.
- Dùng cho những phòng mạch nhỏ một máy tính.
- Sử dụng miễn phí
- Dùng được cho MacOS

## Phiên bản mở rộng:
- Database server để kết nối nhiều máy
- In toa thuốc bằng cách tạo PDF tự động.

## Requirements:
python=3.7  
sqlalchemy  
wxpython=4.0.7  
sqlite

## Hướng dẫn bắt đầu sử dụng:

0. Cài đặt python và các packages, hoặc conda với env `app`

1. Configurations:
- Một số configs trong `setting.json`.
- Ví dụ: công khám bệnh là 50.000

2. Quản lý kho thuốc:

Dùng tools vào database, trong bảng DrugWareHouse có các cột như sau:
- `name`: tên thuốc
- `quantity`: số lượng
- `usage_unit`: đơn vị dùng
- `sale_unit`: đơn vị bán
- `purchase_price`: giá mua
- `sale_price`: giá bán
- `usage`: cách dùng

Có thể chỉnh sửa trong bảng khi có nhập thuốc mới vào kho.

3. File scripts/main.py
- Dùng để chạy app
- option `-n` để tạo database mới
- option `-s` để tạo database mới có data sẵn

4. Dùng các file batch và VBScript để giấu cửa sổ `cmd`

## Liên hệ:
- facebook.com/vuongkienthanh
- thanhstardust@outlook.com
  
