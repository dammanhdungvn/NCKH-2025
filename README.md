# Hệ Thống Phân Tích Kết Quả Học Tập Sinh Viên

## Giới Thiệu
Hệ thống này được thiết kế để phân tích và đánh giá kết quả học tập của sinh viên thông qua việc kết hợp dữ liệu khảo sát và bảng điểm. Hệ thống sử dụng công nghệ AI (LLM) để đưa ra các phân tích chi tiết và đề xuất cải thiện.

## Tính Năng Chính
1. **Quản Lý Khảo Sát**
   - Thu thập thông tin cá nhân sinh viên
   - Đánh giá các kỹ năng học tập qua 10 tiêu chí
   - Tính toán điểm phần trăm cho từng kỹ năng

2. **Xử Lý Bảng Điểm**
   - Hỗ trợ upload file Excel bảng điểm
   - Chuyển đổi dữ liệu sang định dạng JSON
   - Phân tích điểm số theo học kỳ

3. **Phân Tích AI**
   - Phân tích kỹ năng học tập
   - Đánh giá kết quả học tập
   - Tổng hợp và đề xuất cải thiện
   - Tương tác trò chuyện với AI

## Cấu Trúc Dự Án
```
├── Backend/
│   ├── app/
│   │   ├── LLM/           # Mô-đun xử lý AI
│   │   ├── templates/     # Templates cho backend
│   │   ├── app.py         # Server chính
│   │   ├── diem_converter.py  # Xử lý bảng điểm
│   │   └── process_excel.py   # Xử lý file Excel
│   └── requirements.txt    # Dependencies
├── Frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Các trang chính
│   │   └── App.js        # Component gốc
│   └── package.json      # Dependencies frontend
└── Database/             # Thư mục lưu trữ dữ liệu
```

## Yêu Cầu Hệ Thống
- Python 3.8+
- Node.js 14+
- Ollama (cho LLM)

## Cài Đặt

### Backend
1. Tạo môi trường ảo:
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Chạy server:
```bash
python app/app.py
```

### Frontend
1. Cài đặt dependencies:
```bash
cd Frontend
npm install
```

2. Chạy ứng dụng:
```bash
npm start
```

## Cấu Hình
- Backend chạy tại `http://localhost:5000`
- Frontend chạy tại `http://localhost:3000`
- Ollama API URL mặc định: `http://192.168.2.114:11434/api/chat`

## Sử Dụng
1. Truy cập giao diện web tại `http://localhost:3000`
2. Điền thông tin khảo sát
3. Upload bảng điểm Excel
4. Xem phân tích và tương tác với AI

## Đóng Góp
Mọi đóng góp đều được hoan nghênh. Vui lòng tạo issue hoặc pull request để đóng góp.

## Giấy Phép
Dự án này được phát hành dưới giấy phép MIT. 