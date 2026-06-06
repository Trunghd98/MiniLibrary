from datetime import datetime, timedelta
from db_config import loans_col, students_col, books_col

def get_overdue_loans(days_allowed=14):
    """Lấy danh sách quá hạn dùng $lookup"""
    overdue_date = datetime.now() - timedelta(days=days_allowed)
    pipeline = [
        {"$match": {"is_returned": False, "borrow_date": {"$lt": overdue_date}}},
        {"$lookup": {"from": "students", "localField": "student_id", "foreignField": "_id", "as": "student_info"}},
        {"$lookup": {"from": "books", "localField": "book_id", "foreignField": "_id", "as": "book_info"}}
    ]
    return list(loans_col.aggregate(pipeline))

def get_trending_books(top_n=5):
    """Thống kê đầu sách phổ biến (Xử lý Item-level tracking)"""
    pipeline = [
        {"$lookup": {"from": "books", "localField": "book_id", "foreignField": "_id", "as": "book_details"}},
        {"$unwind": "$book_details"},
        {"$group": {
            "_id": "$book_details.title", 
            "total_borrows": {"$sum": 1}
        }},
        {"$sort": {"total_borrows": -1}},
        {"$limit": top_n}
    ]
    return list(loans_col.aggregate(pipeline))

def search_students_with_history(keyword):
    """Tìm kiếm học sinh linh hoạt bằng $regex và lồng lịch sử mượn"""
    query = {
        "$or": [
            {"_id": {"$regex": keyword, "$options": "i"}},
            {"name": {"$regex": keyword, "$options": "i"}},
            {"class": {"$regex": keyword, "$options": "i"}}
        ]
    }
    students = list(students_col.find(query))
    for student in students:
        pipeline = [
            {"$match": {"student_id": student["_id"]}},
            {"$lookup": {"from": "books", "localField": "book_id", "foreignField": "_id", "as": "book_details"}}
        ]
        student["borrowing_history"] = list(loans_col.aggregate(pipeline))
    return students

def search_books_with_history(keyword):
    """Tìm kiếm sách linh hoạt bằng $regex"""
    query = {
        "$or": [
            {"_id": {"$regex": keyword, "$options": "i"}},
            {"title": {"$regex": keyword, "$options": "i"}},
            {"author": {"$regex": keyword, "$options": "i"}}
        ]
    }
    books = list(books_col.find(query))
    for book in books:
        pipeline = [
            {"$match": {"book_id": book["_id"]}},
            {"$lookup": {"from": "students", "localField": "student_id", "foreignField": "_id", "as": "student_details"}}
        ]
        book["loan_history"] = list(loans_col.aggregate(pipeline))
    return books