<<<<<<< HEAD
﻿# Phần mềm phòng mạch tư

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
  
=======
# Phần mềm phòng mạch tư
Tác giả: Bs Vương Kiến Thanh
email: thanhstardust@outlook.com

## Chức năng:
- Quản lý bệnh nhân và các lượt khám.
- Quản lý kho thuốc.
- Tìm kiếm tên bệnh nhân và tên thuốc
- Tất cả dữ liệu nằm database SQLite: bạn có thể tải phần mềm https://sqlitestudio.pl để truy cập vào database.
- Được viết bằng ngôn ngữ python nên chạy được trên Win, Macos, Linux.

## Hướng dẫn quản lý kho thuốc:
Kho thuốc được lưu vào database ở bảng `drugwarehouse`, với từng cột tương ứng với:
- `id`: mã thuốc.
- `name`: tên thuốc, mỗi mã tương ứng với một tên để tránh lỗi nhận diện thuốc.
- `element`: thành phần của thuốc, khi search thuốc, app sẽ dùng cột `element` và `name`.
- `quantity`: số lượng, nếu bạn không quan tâm đến số lượng, có thể đặt -1, tức là vô hạn.
- `usage_unit`: đơn vị sử dụng như viên, ml, giọt,...
- `sale_unit`: đơn vị bán như viên, chai, lọ,...
- `purchase_price`: giá mua vào
- `sale_price`: giá bán ra
- `usage`: cách dùng như uống, nhỏ mũi,..

Bạn có thể dùng app sqlitestudio để chỉnh sửa các giá trị trong bảng này. Bạn cũng có thể áp dụng tương tự với những bảng khác.

## Screenshots
![](/screenshots/ss1.png)

## Hướng dẫn cài đặt:
>>>>>>> bsloi
