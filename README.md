# Booming Ninemila · Kế hoạch truyền thông tích hợp (IMC)

Trang chủ `index.html` + 8 trang kế hoạch con. Mục **Fanpage & Instagram** dẫn sang trang lịch & brief riêng:
https://kigogroupvn-dot.github.io/lich-content-ninemila/

## Sửa nội dung
Toàn bộ chữ và số liệu nằm trong `build/build.py`. Sửa ở đó rồi chạy:

    python3 build/build.py

để sinh lại `index.html` và các trang con. (Sửa thẳng file HTML cũng được, nhưng lần dựng sau sẽ ghi đè.)

## Đổi ảnh
- `assets/anh-bia.jpg`: ảnh sản phẩm ở bìa trang chủ (dọc, ~4:5).
- `assets/nen-bia.jpg`: ảnh nền bìa (ngang), phủ màu chocolate.

## Giao diện
`site.css` (chung mọi trang) theo guideline Ninemila: chocolate #380E00, cam #F16100, hổ phách #F0C79C;
font Philosopher · Be Vietnam Pro · Josefin Sans. `site.js`: menu, lọc ma trận, mục lục.

Có `robots.txt` + thẻ noindex để chặn Google.

## Ảnh demo (khung ảnh)
Mỗi khung ảnh có một **mã khung** (hiện trên khung). Ảnh lấy từ tab **"Ảnh IMC"** trong Google Sheet ghi ở `config.js`:
cột *Mã khung* + cột *Link ảnh (Google Drive)*. Dán link vào Sheet, tải lại web là thấy ảnh. Mã `nen-bia` đổi ảnh nền bìa.

## Bản xem nhanh trên Claude
`preview/` do `build/build.py` sinh ra (CSS/JS nhúng thẳng vào trang). Bản này không đọc được Google Sheet nên chỉ hiện khung mẫu.
