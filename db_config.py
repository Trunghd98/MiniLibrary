import pymongo
from datetime import datetime, timedelta

# Khởi tạo kết nối đến MongoDB (đặt timeout ngắn 2 giây để check cho nhanh)
client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
db = client["LibraryDB"]

# Định nghĩa 3 Collections
students_col = db["students"]
books_col = db["books"]
loans_col = db["loans"]

def check_db_connection():
    """Hàm kiểm tra xem dịch vụ MongoDB Server đã được bật và sẵn sàng chưa"""
    try:
        # Thử lấy thông tin server, nếu không bật sẽ văng ngoại lệ ngay
        client.server_info()
        return True
    except Exception:
        return False

def seed_all_data():
    """Hàm nạp dữ liệu mẫu để Demo hệ thống"""
    students_col.delete_many({})
    books_col.delete_many({})
    loans_col.delete_many({})

    # Nạp Học sinh
    students_col.insert_many([
        {"_id": "HS01", "name": "Nguyễn Văn An", "class": "11A1"},
        {"_id": "HS02", "name": "Trần Thị Bình", "class": "11A2"},
        {"_id": "HS03", "name": "Lê Hoàng Cường", "class": "12A1"}
    ])

    # Nạp Sách
    books_col.insert_many([
        {"_id": "B01", "title": "Lập trình Python cơ bản", "author": "Bộ GD&ĐT", "status": "Sẵn sàng"},
        {"_id": "B02", "title": "Lập trình Python cơ bản", "author": "Bộ GD&ĐT", "status": "Sẵn sàng"},
        {"_id": "B03", "title": "Cơ sở dữ liệu nâng cao", "author": "NXB ĐHQG", "status": "Sẵn sàng"}
    ])

    # Nạp Phiếu mượn mẫu quá hạn 20 ngày
    loans_col.insert_one({
        "_id": "L01",
        "student_id": "HS01",
        "book_id": "B01",
        "borrow_date": datetime.now() - timedelta(days=20),
        "is_returned": False
    })
    books_col.update_one({"_id": "B01"}, {"$set": {"status": "Đã mượn"}})
    
    # Phiếu mượn chưa quá hạn
    loans_col.insert_one({
        "_id": "L02",
        "student_id": "HS02",
        "book_id": "B02",
        "borrow_date": datetime.now() - timedelta(days=1),
        "is_returned": False
    })
    books_col.update_one({"_id": "B02"}, {"$set": {"status": "Đã mượn"}})