# 🎓 Hệ thống Phân tích và Đánh giá Kỹ năng Học tập Sinh viên

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Mô tả dự án

Hệ thống này được thiết kế để phân tích và đánh giá kết quả học tập của sinh viên thông qua việc kết hợp dữ liệu khảo sát và bảng điểm. Hệ thống sử dụng công nghệ **AI (LLM - Large Language Model)** để đưa ra các phân tích chi tiết và đề xuất cải thiện hiệu quả học tập.

### 🎯 Mục tiêu

- Đánh giá toàn diện kỹ năng học tập của sinh viên
- Phân tích kết quả học tập qua các học kỳ
- Đưa ra các đề xuất cải thiện dựa trên AI
- Cung cấp giao diện thân thiện cho việc theo dõi tiến độ học tập

## ✨ Tính năng chính

### 📊 Quản lý khảo sát
- Thu thập thông tin cá nhân sinh viên (MSSV, giới tính, khoa, năm học)
- Đánh giá 10 tiêu chí kỹ năng học tập cốt lõi
- Tính toán điểm phần trăm cho từng kỹ năng
- Lưu trữ dữ liệu khảo sát tự động

### 📈 Xử lý bảng điểm
- Hỗ trợ upload file Excel bảng điểm (.xlsx)
- Chuyển đổi dữ liệu sang định dạng JSON
- Phân tích điểm số theo từng học kỳ
- Tính toán điểm trung bình và thống kê

### 🤖 Phân tích AI thông minh
- **Giai đoạn 1**: Phân tích kỹ năng học tập chi tiết
- **Giai đoạn 2**: Đánh giá kết quả học tập
- **Giai đoạn 3**: Tổng hợp và đề xuất cải thiện
- Tương tác trò chuyện với AI để giải đáp thắc mắc

## 🏗️ Kiến trúc hệ thống

```
NCKH-2025/
├── Backend/                 # Máy chủ xử lý
│   ├── app/
│   │   ├── LLM/            # Mô-đun xử lý AI
│   │   ├── templates/      # Templates backend
│   │   ├── app.py          # Server chính Flask
│   │   ├── diem_converter.py  # Xử lý bảng điểm
│   │   └── process_excel.py   # Xử lý file Excel
│   └── requirements.txt    # Dependencies Python
├── Frontend/               # Giao diện người dùng
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Các trang chính
│   │   └── App.js         # Component gốc
│   └── package.json       # Dependencies Node.js
└── Database/              # Lưu trữ dữ liệu
    ├── khaosat.json       # Dữ liệu khảo sát
    └── diem.json          # Dữ liệu bảng điểm
```

## 🔧 Công nghệ sử dụng

### Backend
- **Python 3.8+** - Ngôn ngữ chính
- **Flask 2.3.3** - Web framework
- **Pandas 2.1.0** - Xử lý dữ liệu
- **Ollama API** - Tích hợp AI LLM (Gemma3:8B)

### Frontend
- **React 18+** - Thư viện UI
- **Node.js 14+** - Runtime JavaScript
- **Modern UI/UX libraries** - Giao diện hiện đại

### Công cụ phát triển
- **Git** - Quản lý phiên bản
- **VS Code** - IDE
- **WSL** - Windows Subsystem for Linux

## 📦 Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.8 trở lên
- Node.js 14 trở lên
- Ollama (cho AI LLM)

### 🚀 Cài đặt Backend

1. **Tạo môi trường ảo Python:**
```bash
cd Backend
python -m venv venv

# Kích hoạt môi trường ảo
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

2. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

3. **Chạy server:**
```bash
python app/app.py
```

### 🌐 Cài đặt Frontend

1. **Cài đặt dependencies:**
```bash
cd Frontend
npm install
```

2. **Chạy ứng dụng:**
```bash
npm start
```

### 🔗 Cấu hình API

- **Backend server**: `http://localhost:5000`
- **Frontend app**: `http://localhost:3000`
- **Ollama API**: `http://192.168.2.114:11434/api/chat`

## 🎯 Hướng dẫn sử dụng

### Bước 1: Khảo sát kỹ năng học tập
1. Truy cập giao diện web tại `http://localhost:3000`
2. Điền thông tin cá nhân (MSSV, giới tính, khoa, năm học, họ tên)
3. Đánh giá 10 tiêu chí kỹ năng học tập:
   - Thái độ học tập
   - Sử dụng mạng xã hội
   - Gia đình & Xã hội
   - Bạn bè
   - Môi trường học tập
   - Quản lý thời gian
   - Tự học
   - Hợp tác nhóm
   - Tư duy phản biện
   - Tiếp thu & xử lý kiến thức

### Bước 2: Upload bảng điểm
1. Chuẩn bị file Excel bảng điểm (.xlsx)
2. Kéo thả hoặc chọn file để upload
3. Hệ thống sẽ tự động xử lý và chuyển đổi dữ liệu

### Bước 3: Phân tích AI
1. Bắt đầu quá trình phân tích AI
2. Xem kết quả phân tích theo thời gian thực
3. Tương tác với AI để đặt câu hỏi và nhận tư vấn

## 📊 Cấu trúc dữ liệu

### Dữ liệu khảo sát (khaosat.json)
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
  }
  // ... các kỹ năng khác
}
```

### Dữ liệu bảng điểm (diem.json)
```json
{
  "data": {
    "total_items": "number",
    "total_pages": "number",
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

## 🛠️ API Endpoints

| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| `POST` | `/api/submit-survey` | Gửi form khảo sát |
| `GET` | `/api/get-survey` | Lấy dữ liệu khảo sát |
| `POST` | `/api/upload-file` | Upload file Excel |
| `GET` | `/api/get-data` | Lấy dữ liệu điểm |
| `POST` | `/api/start-llm-analysis` | Bắt đầu phân tích AI |
| `POST` | `/api/llm-chat` | Tương tác chat với AI |

## 🔒 Bảo mật và xử lý lỗi

### Bảo mật
- Xác thực người dùng
- Mã hóa dữ liệu nhạy cảm
- Kiểm tra tính hợp lệ của input
- Validation dữ liệu đầu vào

### Xử lý lỗi
- Kiểm tra tính hợp lệ của file upload
- Xử lý lỗi kết nối API
- Xử lý lỗi định dạng dữ liệu
- Hiển thị thông báo lỗi thân thiện

## 🚀 Kế hoạch phát triển

### Tính năng mới
- [ ] Thêm biểu đồ phân tích trực quan
- [ ] Tích hợp nhiều mô hình AI
- [ ] Hỗ trợ nhiều định dạng file (CSV, PDF)
- [ ] Xuất báo cáo PDF

### Cải thiện hiệu suất
- [ ] Caching dữ liệu
- [ ] Tối ưu hóa truy vấn
- [ ] Xử lý đồng thời
- [ ] Nâng cấp giao diện responsive

### Mở rộng tính năng
- [ ] Hệ thống thông báo
- [ ] Dashboard quản lý
- [ ] Tích hợp với LMS
- [ ] Mobile app companion

## Video Demo

[![🎬 Xem video demo trên YouTube](https://img.youtube.com/vi/vOCOzLpUNrc/0.jpg)](https://youtu.be/vOCOzLpUNrc)

*Click vào ảnh để xem video demo trên YouTube*

## 📞 Liên hệ và hỗ trợ

- **Tác giả**: dammanhdungvn
- **Email**: [Thêm email liên hệ]
- **Issues**: [GitHub Issues](https://github.com/dammanhdungvn/NCKH-2025/issues)

## 📄 Giấy phép

Dự án này được phát hành dưới giấy phép [MIT License](LICENSE).

## 📚 Tài liệu tham khảo

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Ollama API Documentation](https://ollama.ai/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

⭐ **Nếu dự án này hữu ích với bạn, hãy cho chúng tôi một star trên GitHub!**
