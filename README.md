# Booming Ninemila · Kế hoạch truyền thông tích hợp (IMC)

Web một trang: `index.html` + nội dung `noidung.json` (trang chủ, Fanpage & Instagram và 8 kế hoạch kênh, chuyển trang bằng `#ten-trang`).
Mục Fanpage & Instagram nhúng trang lịch & brief: https://kigogroupvn-dot.github.io/lich-content-ninemila/

## Sửa nội dung
Sửa trên bản Claude (nút "Sửa nội dung"), sau đó nhờ Claude đưa bản mới lên đây:
lấy `noidung.json` mới, tải ảnh đã chèn về `assets/anh/` và đổi đường dẫn ảnh.

## Các file
- `index.html` — khung trang (sinh từ `build/spa.py`, nút sửa tự ẩn ngoài Claude)
- `noidung.json` — toàn bộ nội dung
- `assets/` — logo, ảnh bìa, ảnh nền; `assets/anh/` — ảnh demo đã chèn
- `site.css`, `build/` — mã nguồn giao diện
- `robots.txt` + thẻ noindex — chặn Google
