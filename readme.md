# 📖 HƯỚNG DẪN CHẠY DỰ ÁN QUẢN LÝ THƯ VIỆN MINI

Dự án sử dụng kiến trúc 3 lớp với **MongoDB** làm cơ sở dữ liệu và **Streamlit** làm giao diện người dùng. Vui lòng thực hiện theo các bước sau để khởi chạy hệ thống.

## 🛠️ 1. Chuẩn bị môi trường

Đảm bảo máy tính của bạn đã cài đặt các thành phần sau:

- **Python**: Phiên bản 3.10 trở lên.

- **MongoDB Community Server**: Đang chạy dưới dạng dịch vụ hệ thống.

- **MongoDB Compass**: Để kiểm tra dữ liệu trực quan (tùy chọn).

## 📂 2. Cấu trúc thư mục mã nguồn

Tất cả các file sau phải nằm chung trong một thư mục dự án:

1. `db_config.py`: Cấu hình kết nối và khởi tạo database.

2. `core_logic.py`: Xử lý các nghiệp vụ CRUD cơ bản.

3. `advanced_features.py`: Xử lý tìm kiếm nâng cao và thống kê.

4. `main_ui.py`: Giao diện người dùng chính.

## ⚙️ 3. Cài đặt thư viện hỗ trợ

Mở Terminal hoặc Command Prompt tại thư mục dự án và chạy lệnh sau để cài đặt các thư viện Python cần thiết:

```bash
pip install pymongo streamlit pandas

```

Lưu ý: Nếu gặp lỗi lệnh `pip` không được nhận diện, hãy sử dụng `python -m pip install...`.

## 🚀 4. Các bước khởi chạy

### Bước 1: Bật dịch vụ MongoDB

Đảm bảo dịch vụ MongoDB đã được khởi động trong **Task Manager** (thẻ Services). Nếu dịch vụ chưa chạy, hãy chuột phải vào `MongoDB` và chọn **Start**.

### Bước 2: Chạy ứng dụng Streamlit

Tại thư mục dự án, thực hiện lệnh sau để mở giao diện web:

```bash
streamlit run main_ui.py

```

Hệ thống sẽ tự động mở trình duyệt tại địa chỉ `http://localhost:8501`.

### Bước 3: Khởi tạo dữ liệu mẫu

Khi giao diện web hiện lên lần đầu, dữ liệu sẽ trống. Bạn cần:

1. Nhìn vào thanh menu bên trái (Sidebar).

2. Nhấn nút **"⚙️ Nạp dữ liệu mẫu"**.

3. Hệ thống sẽ tự động tạo các bản ghi học sinh, sách và phiếu mượn giả lập để bạn kiểm thử các chức năng.

## ❓ 5. Xử lý lỗi thường gặp

- **Lỗi kết nối CSDL**: Kiểm tra xem MongoDB Server đã được bật chưa. Hệ thống có tích hợp sẵn bảng thông báo hướng dẫn bật dịch vụ ngay trên giao diện nếu kết nối thất bại.

- **Dữ liệu không cập nhật**: Trong MongoDB Compass, hãy nhấn nút **Refresh** (biểu tượng xoay tròn) để tải lại dữ liệu mới nhất từ server.

- **Lỗi ràng buộc**: Bạn không thể xóa học sinh hoặc sách nếu đối tượng đó đang có phiếu mượn chưa trả. Phải thực hiện trả sách trước khi xóa.
