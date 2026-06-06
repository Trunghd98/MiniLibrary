from db_config import students_col, books_col, loans_col
from datetime import datetime

# ================== QUẢN LÝ HỌC SINH ==================
def add_student(student_id, name, class_name):
    if students_col.find_one({"_id": student_id}):
        return False, "Lỗi: Mã học sinh đã tồn tại!"
    students_col.insert_one({"_id": student_id, "name": name, "class": class_name})
    return True, "Thêm học sinh thành công!"

def get_all_students():
    return list(students_col.find())

def delete_student(student_id):
    if loans_col.find_one({"student_id": student_id, "is_returned": False}):
        return False, "Lỗi: Học sinh đang mượn sách chưa trả, không thể xóa!"
    students_col.delete_one({"_id": student_id})
    return True, "Xóa học sinh thành công!"

# ================== QUẢN LÝ SÁCH ==================
def add_book(book_id, title, author):
    if books_col.find_one({"_id": book_id}):
        return False, "Lỗi: Mã sách đã tồn tại!"
    books_col.insert_one({"_id": book_id, "title": title, "author": author, "status": "Sẵn sàng"})
    return True, "Thêm sách thành công!"

def get_all_books():
    return list(books_col.find())

def delete_book(book_id):
    book = books_col.find_one({"_id": book_id})
    if book and book.get("status") == "Đã mượn":
        return False, "Lỗi: Sách đang được mượn, không thể xóa khỏi kho!"
    books_col.delete_one({"_id": book_id})
    return True, "Xóa sách thành công!"

# ================== NGHIỆP VỤ MƯỢN TRẢ ==================
def borrow_book(loan_id, student_id, book_id):
    if not students_col.find_one({"_id": student_id}):
        return False, "Lỗi: Mã học sinh không tồn tại!"
    
    book = books_col.find_one({"_id": book_id})
    if not book:
        return False, "Lỗi: Mã sách không tồn tại!"
    if book["status"] == "Đã mượn":
        return False, "Lỗi: Cuốn sách này đang có người mượn!"
    if loans_col.find_one({"_id": loan_id}):
        return False, "Lỗi: Mã phiếu mượn đã tồn tại!"

    # Giao dịch
    loans_col.insert_one({
        "_id": loan_id,
        "student_id": student_id,
        "book_id": book_id,
        "borrow_date": datetime.now(),
        "is_returned": False
    })
    books_col.update_one({"_id": book_id}, {"$set": {"status": "Đã mượn"}})
    return True, "Cho mượn sách thành công!"

def return_book(book_id):
    loan = loans_col.find_one({"book_id": book_id, "is_returned": False})
    if not loan:
        return False, "Lỗi: Không tìm thấy phiếu mượn nào chưa trả của cuốn sách này!"
    
    # Giao dịch
    loans_col.update_one({"_id": loan["_id"]}, {"$set": {"is_returned": True}})
    books_col.update_one({"_id": book_id}, {"$set": {"status": "Sẵn sàng"}})
    return True, "Nhận trả sách thành công!"