# Phần mềm phòng mạch tư
Tác giả: Bs Vương Kiến Thanh
email: thanhstardust@outlook.com

## Chức năng:
- Quản lý bệnh nhân và các lượt khám.
- Quản lý kho thuốc.
- Tìm kiếm tên bệnh nhân và tên thuốc
- Tất cả dữ liệu nằm database SQLite: bạn có thể tải phần mềm https://sqlitestudio.pl để truy cập vào database.
- Được viết bằng ngôn ngữ python nên chạy được trên Win, Macos, Linux.
- **Chỉ sử dụng được cho một máy local**.


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
Tải về tại https://github.com/vuongkienthanh/pmpktn/releases/
- MacOS: Nếu bạn bị lỗi developer cannot be verified, thì bạn dùng menu chuột phải -> open. Những lần sau sẽ không cần bước này nữa.

## Liên hệ:
- facebook.com/vuongkienthanh
- thanhstardust@outlook.com
