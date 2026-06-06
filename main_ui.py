import streamlit as st
import pandas as pd

# --- IMPORT CÁC HÀM TỪ CÁC MODULE ---
from db_config import seed_all_data, check_db_connection
from core_logic import (
    add_student, get_all_students, 
    add_book, get_all_books, 
    borrow_book, return_book
)
from advanced_features import (
    get_overdue_loans, get_trending_books, 
    search_students_with_history, search_books_with_history
)

# Cấu hình trang cơ bản
st.set_page_config(page_title="Thư Viện Mini", layout="wide")
st.title("📚 Hệ Thống Quản Lý Thư Viện Mini")

# ==============================================================================
# KIỂM TRA KẾT NỐI CSDL TRƯỚC KHI CHẠY GIAO DIỆN (BẢO VỆ HỆ THỐNG)
# ==============================================================================
if not check_db_connection():
    st.error("❌ LỖI: KHÔNG THỂ KẾT NỐI TỚI CƠ SỞ DỮ LIỆU MONGODB!")
    st.warning("Hệ thống phát hiện dịch vụ MongoDB Server trên máy tính của thầy/cô hiện đang TẮT.")
    
    st.markdown("""
    ### ⚙️ Hướng dẫn bật lại Cơ sở dữ liệu trên Windows:
    1. Nhấn tổ hợp phím **Ctrl + Shift + Esc** để mở **Task Manager** (Trình quản lý tác vụ).
    2. Chuyển sang thẻ **Services** (Dịch vụ) ở thanh danh mục.
    3. Tìm dịch vụ có tên là **MongoDB** hoặc **MongoDBServer**.
    4. Kích chuột phải vào dịch vụ đó và chọn **Start** (Khởi chạy).
    5. Quay lại đây và bấm nút **F5** để tải lại trang Web này.
    """)
    st.stop() # Lệnh dừng toàn bộ chương trình phía dưới để tránh crash code

# ==============================================================================
# MENU THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR) - CHỈ HIỆN KHI DB ONLINE
# ==============================================================================
st.sidebar.title("Điều hướng")
menu = st.sidebar.radio(
    "Chọn chức năng:", 
    ("Dashboard", "Mượn / Trả Sách", "Quản lý Sách", "Quản lý Độc giả", "Tra cứu Nâng cao")
)

st.sidebar.markdown("---")
if st.sidebar.button("⚙️ Nạp dữ liệu mẫu"):
    seed_all_data()
    st.sidebar.success("Đã nạp lại toàn bộ dữ liệu mẫu!")

# ==============================================================================
# MÀN HÌNH 1: DASHBOARD (THỐNG KÊ & CẢNH BÁO)
# ==============================================================================
if menu == "Dashboard":
    st.header("Bảng điều khiển & Thống kê")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔥 Top Sách Phổ Biến")
        trending = get_trending_books(top_n=5)
        if trending:
            df_trend = pd.DataFrame([{
                "Tên Sách": item["_id"], 
                "Lượt mượn": item["total_borrows"]
            } for item in trending])
            st.bar_chart(df_trend.set_index("Tên Sách"))
        else:
            st.info("Chưa có dữ liệu mượn sách để thống kê.")
            
    with col2:
        st.subheader("⚠️ Cảnh báo sách quá hạn (>14 ngày)")
        overdues = get_overdue_loans(days_allowed=14)
        if overdues:
            for od in overdues:
                student_name = od['student_info'][0]['name'] if od['student_info'] else "Không rõ"
                book_title = od['book_info'][0]['title'] if od['book_info'] else "Không rõ"
                date_str = od['borrow_date'].strftime('%d/%m/%Y')
                st.error(f"Học sinh **{student_name}** chưa trả cuốn **{book_title}** (Mượn từ ngày: {date_str})!")
        else:
            st.success("Tuyệt vời! Không có cuốn sách nào bị quá hạn.")

# ==============================================================================
# MÀN HÌNH 2: THAO TÁC MƯỢN TRẢ
# ==============================================================================
elif menu == "Mượn / Trả Sách":
    st.header("Quầy Nghiệp Vụ (Mượn / Trả Sách)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📤 Cho Mượn Sách")
        with st.form("form_borrow"):
            l_id = st.text_input("Mã phiếu mới (VD: L03)")
            s_id_borrow = st.text_input("Mã Học Sinh")
            b_id_borrow = st.text_input("Mã Sách vật lý")
            if st.form_submit_button("Xác nhận Cho mượn"):
                if l_id and s_id_borrow and b_id_borrow:
                    success, msg = borrow_book(l_id, s_id_borrow, b_id_borrow)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Vui lòng nhập đầy đủ thông tin phiếu mượn!")

    with col2:
        st.subheader("📥 Nhận Trả Sách")
        with st.form("form_return"):
            b_id_return = st.text_input("Mã Sách khách trả")
            if st.form_submit_button("Xác nhận Thu hồi"):
                if b_id_return:
                    success, msg = return_book(b_id_return)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Vui lòng nhập mã sách cần trả!")

# ==============================================================================
# MÀN HÌNH 3: QUẢN LÝ SÁCH
# ==============================================================================
elif menu == "Quản lý Sách":
    st.header("Kho Sách Thư Viện")
    
    with st.expander("➕ Thêm sách mới"):
        with st.form("form_add_book", clear_on_submit=True):
            col_b1, col_b2, col_b3 = st.columns(3)
            b_id = col_b1.text_input("Mã sách (ID)")
            b_title = col_b2.text_input("Tên sách")
            b_author = col_b3.text_input("Tác giả")
            
            submitted = st.form_submit_button("Lưu Sách")
            if submitted:
                if b_id and b_title and b_author:
                    success, msg = add_book(b_id, b_title, b_author)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Vui lòng nhập đủ thông tin!")
                    
    st.subheader("Danh sách toàn bộ sách trong kho")
    books = get_all_books()
    if books:
        st.dataframe(pd.DataFrame(books), use_container_width=True)
    else:
        st.info("Kho sách đang trống.")

# ==============================================================================
# MÀN HÌNH 4: QUẢN LÝ ĐỘC GIẢ
# ==============================================================================
elif menu == "Quản lý Độc giả":
    st.header("Danh sách Độc giả (Học sinh)")
    
    with st.expander("➕ Thêm học sinh mới"):
        with st.form("form_add_student", clear_on_submit=True):
            col_s1, col_s2, col_s3 = st.columns(3)
            s_id = col_s1.text_input("Mã học sinh")
            s_name = col_s2.text_input("Họ và Tên")
            s_class = col_s3.text_input("Lớp học")
            
            submitted = st.form_submit_button("Lưu Học sinh")
            if submitted:
                if s_id and s_name and s_class:
                    success, msg = add_student(s_id, s_name, s_class)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Vui lòng nhập đủ thông tin học sinh!")
                    
    st.subheader("Danh sách Độc giả hiện tại")
    students = get_all_students()
    if students:
        st.dataframe(pd.DataFrame(students), use_container_width=True)
    else:
        st.info("Danh sách độc giả đang trống.")

# ==============================================================================
# MÀN HÌNH 5: TRA CỨU NÂNG CAO TÍCH HỢP LỊCH SỬ DỮ LIỆU
# ==============================================================================
elif menu == "Tra cứu Nâng cao":
    st.header("Tìm kiếm")
    search_type = st.radio("Loại tra cứu:", ["Học Sinh", "Sách"])
    keyword = st.text_input("Nhập từ khóa tìm kiếm (Mã ID, Tên, Lớp, Tác giả... )")
    
    if st.button("Tìm kiếm"):
        if not keyword.strip():
            st.warning("Vui lòng điền từ khóa trước khi bấm tìm kiếm!")
        else:
            if search_type == "Học Sinh":
                results = search_students_with_history(keyword)
                
                if len(results) == 0:
                    st.warning("Không tìm thấy Học sinh nào phù hợp với từ khóa!")
                else:
                    st.success(f"Tìm thấy {len(results)} học sinh phù hợp!")
                    for hs in results:
                        with st.expander(f"👤 {hs['name']} - Lớp {hs['class']} (ID: {hs['_id']})", expanded=True):
                            if hs['borrowing_history']:
                                st.write("**Lịch sử mượn sách của học sinh này:**")
                                for h in hs['borrowing_history']:
                                    b_title = h['book_details'][0]['title'] if h['book_details'] else "Không rõ tựa sách"
                                    status = "Đã trả ✅" if h['is_returned'] else "Chưa trả ❌"
                                    st.write(f"- Sách: **{b_title}** | Tình trạng: {status}")
                            else: 
                                st.write("Học sinh này chưa mượn sách lần nào.")
            else:
                results = search_books_with_history(keyword)
                
                if len(results) == 0:
                    st.warning("Không tìm thấy Sách nào phù hợp với từ khóa!")
                else:
                    st.success(f"Tìm thấy {len(results)} bản sao sách phù hợp!")
                    for bk in results:
                        with st.expander(f"📕 {bk['title']} - Tác giả: {bk['author']} (ID: {bk['_id']})", expanded=True):
                            st.write(f"Trạng thái hiện tại: **{bk['status']}**")
                            if bk.get('loan_history'):
                                st.write("**Lịch sử độc giả đã mượn cuốn vật lý này:**")
                                for h in bk['loan_history']:
                                    s_name = h['student_details'][0]['name'] if h['student_details'] else "Không rõ độc giả"
                                    status = "Đã trả" if h['is_returned'] else "Chưa trả"
                                    st.write(f"- Độc giả **{s_name}** mượn | Tình trạng: {status}")
                            else: 
                                st.write("Bản sao cuốn sách này chưa từng có lịch sử mượn.")