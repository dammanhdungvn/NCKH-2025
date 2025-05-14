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

# Giải Thích Chi Tiết Hệ Thống Phân Tích Kết Quả Học Tập

## 1. Tổng Quan Hệ Thống

Hệ thống này là một ứng dụng web được thiết kế để phân tích và đánh giá kết quả học tập của sinh viên thông qua việc kết hợp dữ liệu khảo sát và bảng điểm. Hệ thống sử dụng công nghệ AI (LLM - Large Language Model) để đưa ra các phân tích chi tiết và đề xuất cải thiện.

## 2. Kiến Trúc Hệ Thống

### 2.1. Backend (Python/Flask)
- **Server chính (app.py)**: Xử lý các API endpoints và điều phối luồng dữ liệu
- **Xử lý bảng điểm (diem_converter.py)**: Chuyển đổi dữ liệu từ Excel sang JSON
- **Tích hợp LLM**: Sử dụng Ollama API để phân tích dữ liệu và tương tác với người dùng

### 2.2. Frontend (React)
- Giao diện người dùng hiện đại và thân thiện
- Xử lý form khảo sát và upload file
- Hiển thị kết quả phân tích và tương tác với AI

### 2.3. Cơ Sở Dữ Liệu
- Lưu trữ dữ liệu dưới dạng file JSON
- Bao gồm dữ liệu khảo sát và bảng điểm

## 3. Chi Tiết Chức Năng

### 3.1. Quản Lý Khảo Sát
- **Thu thập thông tin cá nhân**:
  - Mã số sinh viên
  - Giới tính
  - Khoa
  - Năm học
  - Họ tên

- **Đánh giá kỹ năng học tập** (10 tiêu chí):
  1. Thái độ học tập
  2. Sử dụng mạng xã hội
  3. Gia đình & Xã hội
  4. Bạn bè
  5. Môi trường học tập
  6. Quản lý thời gian
  7. Tự học
  8. Hợp tác nhóm
  9. Tư duy phản biện
  10. Tiếp thu & xử lý kiến thức

### 3.2. Xử Lý Bảng Điểm
- **Upload file Excel**:
  - Hỗ trợ định dạng .xlsx
  - Kiểm tra tính hợp lệ của file
  - Chuyển đổi sang JSON

- **Cấu trúc dữ liệu điểm**:
  - Thông tin học kỳ
  - Danh sách môn học
  - Điểm số và kết quả
  - Thống kê tổng hợp

### 3.3. Phân Tích AI (LLM)
- **Giai đoạn 1**: Phân tích kỹ năng học tập
  - Đánh giá từng tiêu chí
  - Xác định điểm mạnh/yếu
  - Đề xuất cải thiện

- **Giai đoạn 2**: Phân tích kết quả học tập
  - Đánh giá điểm số
  - Phân tích xu hướng
  - So sánh với chuẩn

- **Giai đoạn 3**: Tổng hợp và đề xuất
  - Kết hợp phân tích kỹ năng và điểm số
  - Đưa ra đề xuất cụ thể
  - Tương tác trò chuyện với AI

## 4. Luồng Xử Lý Dữ Liệu

1. **Thu thập dữ liệu**:
   - Người dùng điền form khảo sát
   - Upload file bảng điểm Excel

2. **Xử lý dữ liệu**:
   - Chuyển đổi định dạng
   - Tính toán điểm phần trăm
   - Chuẩn hóa dữ liệu

3. **Phân tích AI**:
   - Stream kết quả phân tích
   - Tương tác trò chuyện
   - Cập nhật đề xuất

4. **Hiển thị kết quả**:
   - Biểu đồ thống kê
   - Báo cáo chi tiết
   - Đề xuất cải thiện

## 5. Công Nghệ Sử Dụng

### 5.1. Backend
- Python 3.8+
- Flask 2.3.3
- Pandas 2.1.0
- Ollama API (Gemma 2B)

### 5.2. Frontend
- React
- Node.js 14+
- Các thư viện UI/UX

### 5.3. Công Cụ Phát Triển
- Git
- VS Code
- WSL (Windows Subsystem for Linux)

## 6. Bảo Mật và Hiệu Suất

- **Bảo mật**:
  - Xác thực người dùng
  - Mã hóa dữ liệu
  - Kiểm tra tính hợp lệ của input

- **Hiệu suất**:
  - Xử lý bất đồng bộ
  - Stream kết quả phân tích
  - Tối ưu hóa tài nguyên

## 7. Hướng Phát Triển

1. **Mở rộng tính năng**:
   - Thêm biểu đồ phân tích
   - Tích hợp nhiều mô hình AI
   - Hỗ trợ nhiều định dạng file

2. **Cải thiện UI/UX**:
   - Giao diện responsive
   - Tối ưu hóa trải nghiệm người dùng
   - Thêm tính năng tương tác

3. **Nâng cao hiệu suất**:
   - Caching dữ liệu
   - Tối ưu hóa truy vấn
   - Xử lý đồng thời

## 8. Chi Tiết Kỹ Thuật

### 8.1. Backend Functions

#### 8.1.1. Xử Lý Khảo Sát (app.py)
```python
@app.route('/api/submit-survey', methods=['POST'])
```
- **Chức năng**: Xử lý việc gửi form khảo sát
- **Input**: JSON chứa thông tin cá nhân và điểm đánh giá
- **Xử lý**:
  - Trích xuất thông tin cá nhân (MSSV, giới tính, khoa, năm học, họ tên)
  - Tính toán điểm phần trăm cho 10 tiêu chí kỹ năng
  - Lưu kết quả vào file JSON
- **Output**: JSON chứa kết quả đã xử tại và lưu vào thư mục Database/khaosat.json

#### 8.1.2. Xử Lý Bảng Điểm (diem_converter.py)
```python
def convert_excel_to_json(excel_filepath, json_filepath)
```
- **Chức năng**: Chuyển đổi file Excel bảng điểm sang JSON
- **Input**: Đường dẫn file Excel và file JSON đầu ra
- **Xử lý**:
  - Đọc file Excel sử dụng Pandas
  - Trích xuất thông tin học kỳ
  - Xử lý điểm số từng môn học
  - Tính toán thống kê tổng hợp
- **Output**: File JSON chứa dữ liệu đã được cấu trúc hóa và lưu vào thư mục Database/diem.json

```python
def extract_hoc_ky_code(ten_hoc_ky_str)
```
- **Chức năng**: Trích xuất mã học kỳ từ chuỗi tên học kỳ
- **Input**: Chuỗi chứa tên học kỳ (VD: "Học kỳ 1 - Năm học 2022-2023")
- **Xử lý**: Sử dụng regex để trích xuất thông tin
- **Output**: Mã học kỳ dạng "YYYYX" (năm học + số học kỳ)

#### 8.1.3. Phân Tích AI (LLM)
```python
@app.route('/api/start-llm-analysis', methods=['GET', 'POST'])
```
- **Chức năng**: Bắt đầu quá trình phân tích AI
- **Xử lý**:
  - Giai đoạn 1: Phân tích kỹ năng học tập
  - Giai đoạn 2: Phân tích kết quả học tập
  - Giai đoạn 3: Tổng hợp và đề xuất
- **Output**: Stream kết quả phân tích theo thời gian thực

```python
@app.route('/api/llm-chat', methods=['POST'])
```
- **Chức năng**: Xử lý tương tác trò chuyện với AI
- **Input**: Tin nhắn từ người dùng
- **Xử lý**: Gửi tin nhắn đến Ollama API và stream phản hồi
- **Output**: Stream phản hồi từ AI

### 8.2. Frontend Components

#### 8.2.1. Form Khảo Sát
- **Chức năng**: Thu thập thông tin và đánh giá kỹ năng
- **Components**:
  - Form thông tin cá nhân
  - 10 bảng đánh giá kỹ năng
  - Nút gửi và xác nhận

#### 8.2.2. Upload Bảng Điểm
- **Chức năng**: Upload và xử lý file Excel
- **Components**:
  - Khu vực kéo thả file
  - Hiển thị tiến trình upload
  - Thông báo kết quả xử lý

#### 8.2.3. Hiển Thị Kết Quả
- **Chức năng**: Hiển thị kết quả phân tích
- **Components**:
  - Biểu đồ thống kê
  - Bảng điểm chi tiết
  - Khu vực chat với AI

### 8.3. Cấu Trúc Dữ Liệu

#### 8.3.1. Dữ Liệu Khảo Sát
```json
{
  "thong_tin_ca_nhan": {
    "ma_so_sinh_vien": "string",
    "gioi_tinh": "string",
    "khoa": "string",
    "nam_hoc": "string",
    "ho_ten": "string"
  },
  "thoi_gian_nop": "datetime",
  "Thai_do_hoc_tap": {
    "tong_so_cau_hoi": "number",
    "phan_tram_diem": "number"
  },
  // ... các kỹ năng khác
}
```

#### 8.3.2. Dữ Liệu Điểm
```json
{
  "data": {
    "total_items": "number",
    "total_pages": "number",
    "is_kkbd": "boolean",
    "ds_diem_hocky": [
      {
        "hoc_ky": "string",
        "ten_hoc_ky": "string",
        "dtb_hk_he10": "number",
        "dtb_hk_he4": "number",
        "ds_diem_mon_hoc": [
          {
            "ma_mon": "string",
            "ten_mon": "string",
            "so_tin_chi": "number",
            "diem_thi": "number",
            "diem_tk": "number"
          }
        ]
      }
    ]
  }
}
```

### 8.4. API Endpoints

#### 8.4.1. Khảo Sát
- `POST /api/submit-survey`: Gửi form khảo sát
- `GET /api/get-survey`: Lấy dữ liệu khảo sát

#### 8.4.2. Bảng Điểm
- `POST /api/upload-file`: Upload file Excel
- `GET /api/get-data`: Lấy dữ liệu điểm

#### 8.4.3. Phân Tích AI
- `POST /api/start-llm-analysis`: Bắt đầu phân tích
- `POST /api/llm-chat`: Tương tác với AI

### 8.5. Xử Lý Lỗi

#### 8.5.1. Backend
- Kiểm tra tính hợp lệ của input
- Xử lý lỗi file không tồn tại
- Xử lý lỗi định dạng dữ liệu
- Xử lý lỗi kết nối API

#### 8.5.2. Frontend
- Hiển thị thông báo lỗi
- Xử lý lỗi mạng
- Xử lý lỗi validation
<<<<<<< HEAD
- Xử lý lỗi upload file 
=======
- Xử lý lỗi upload file 
>>>>>>> db2c2a402a6831b2b517d3c08da67f0cf418754d
