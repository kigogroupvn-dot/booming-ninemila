# -*- coding: utf-8 -*-
"""Dựng website Booming Ninemila.
Chạy:  python3 build/build.py   (từ thư mục gốc repo)
Toàn bộ nội dung nằm trong file này; sửa chữ ở đây rồi chạy lại để sinh các trang HTML."""
import html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FANPAGE_URL = "https://kigogroupvn-dot.github.io/lich-content-ninemila/"
PERIOD = "15/11/2026 – 28/02/2027"
E = html.escape

# ───────────────────────── Danh mục kế hoạch ─────────────────────────
PLANS = [
  dict(slug="fanpage", name="Fanpage & Instagram", short="Lịch đăng, brief nội dung và tiến độ triển khai.", kpi="5 bài/tuần", kpi_sub="Fanpage branding · 22 brief", url=FANPAGE_URL, ext=True),
  dict(slug="threads", name="Threads", short="Kênh brand 21 bài/tuần và tuyến bài seeding riêng.", kpi="500.000", kpi_sub="Tiếp cận kỳ vọng / tháng"),
  dict(slug="kol-koc", name="KOL / KOC", short="65 KOC TikTok; booking Hoàng Kim Ngọc và Linh Remy.", kpi="65 KOC · 2 KOL", kpi_sub="20/11/2026 – 02/2027"),
  dict(slug="megalive", name="Megalive Võ Hà Linh", short="Cao điểm chủ lực của chiến dịch, tháng 01/2027.", kpi="≈ 150.000.000 ₫", kpi_sub="Ngân sách dự kiến"),
  dict(slug="tiktok", name="TikTok", short="Hai kênh công ty: video, quảng cáo và livestream hằng ngày.", kpi="60.000.000 ₫", kpi_sub="Quảng cáo / tháng"),
  dict(slug="shopee", name="Shopee", short="Hai gian hàng: SIS, quảng cáo nội sàn và livestream.", kpi="10.000.000 ₫", kpi_sub="Ads / tháng cho hai shop"),
  dict(slug="dai-ly", name="Đại lý", short="50 đại lý đăng bài trong tháng 12/2026.", kpi="1.500 bài", kpi_sub="50 đại lý × 30 bài"),
  dict(slug="hasaki", name="HASAKI", short="Livestream độc quyền, activation và PG tháng 01–02.", kpi="≥ 50.000.000 ₫", kpi_sub="Activation & PG"),
  dict(slug="website", name="Website", short="Cập nhật nội dung trên kigora.vn và kigora.com.", kpi="2 website", kpi_sub="kigora.vn · kigora.com"),
]
for i, p in enumerate(PLANS, 1): p["no"] = f"{i:02d}"; p.setdefault("url", p["slug"] + ".html"); p.setdefault("ext", False)
INTERNAL = [p for p in PLANS if not p["ext"]]

# ───────────────────────── Khung trang ─────────────────────────
def head(title, desc):
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="light only">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Josefin+Sans:wght@400;600&family=Philosopher:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css">
</head>
<body>
"""

def menu(current):
    items = "".join(
        f'<a href="{E(p["url"])}"{" target=\"_blank\" rel=\"noopener\"" if p["ext"] else ""}{" class=\"on\"" if p["slug"] == current else ""}>'
        f'<span>{E(p["name"])}</span><small>{"↗" if p["ext"] else p["no"]}</small></a>' for p in PLANS)
    home = f'<a href="index.html"{" class=\"on\"" if current == "index" else ""}><span>Tổng quan IMC</span><small>⌂</small></a><hr>'
    return f'<div class="menu"><button class="btn" type="button" aria-expanded="false">Các kế hoạch ▾</button><div class="menu-list">{home}{items}</div></div>'

def topbar(current):
    back = '' if current == "index" else '<a class="btn hide-m" href="index.html">← Tổng quan IMC</a>'
    return f'<div class="top"><a class="logo" href="index.html"><img src="assets/logo-white.png" alt="Ninemila"></a><nav>{back}{menu(current)}</nav></div>'

def stats(items, note=""):
    cells = "".join(f'<div class="stat"><b>{E(a)}</b><span>{E(b)}</span>{f"<small>{E(c)}</small>" if c else ""}</div>' for a, b, c in items)
    return f'<div class="stats-band"><div class="wrap"><div class="stats">{cells}</div>{f"<div class=\"band-note\">{E(note)}</div>" if note else ""}</div></div>'

FOOT = """<footer class="footer"><div class="wrap"><img src="assets/logo-white.png" alt="Ninemila"><span>Booming Ninemila · Kế hoạch truyền thông tích hợp 2026–2027 · Khối Marketing, Kigo Group</span></div></footer>
<script src="site.js"></script>
</body>
</html>
"""

def ul(items): return '<ul class="dash">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
def boxes(cols, three=False):
    return f'<div class="split{" three" if three else ""}">' + "".join(
        f'<div class="box"><h3>{f"<small>{E(k)}</small>" if k else ""}{E(t)}</h3>{ul(items)}</div>' for k, t, items in cols) + "</div>"
def table(headers, rows, num=(), total=None):
    th = "".join(f'<th{" class=\"num\"" if i in num else ""}>{E(h)}</th>' for i, h in enumerate(headers))
    def tr(r, cls=""):
        return f'<tr{f" class=\"{cls}\"" if cls else ""}>' + "".join(f'<td{" class=\"num\"" if i in num else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>"
    body = "".join(tr(r) for r in rows) + (tr(total, "total") if total else "")
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def callout(t): return f'<div class="callout">{t}</div>'
def prose(*ps): return '<div class="prose">' + "".join(f"<p>{p}</p>" for p in ps) + "</div>"
def sm(t): return f"<small>{t}</small>"

# ───────────────────────── Trang con ─────────────────────────
PAGES = {}

PAGES["threads"] = dict(
  title="Kế hoạch Threads",
  lead="Kết hợp nội dung kênh brand với tuyến bài seeding để tạo thảo luận về tóc rụng, tóc thiếu độ phồng và trải nghiệm Ninemila. Hai tuyến bài được lập lịch và đo lường riêng.",
  stats=[("21 bài/tuần","Kênh brand","Tương đương 3 bài/ngày"),("318 bài","Sản lượng brand dự kiến","3 bài/ngày × 106 ngày"),("500.000","Tiếp cận kỳ vọng / tháng",""),("2 tuyến","Brand & seeding","Lập lịch, đo lường riêng")],
  sections=[
    ("Hai tuyến triển khai", boxes([("Kênh brand","21 bài/tuần",["Tình huống tóc rụng, tóc xẹp, tóc khô xơ.","Chia sẻ kiến thức, cách dùng, routine và giải đáp.","Nội dung KOC/KOL và các hoạt động thương hiệu."]),
                                    ("Seeding","Lịch bài riêng",["Chủ đề hỏi đáp, trao đổi trải nghiệm và tìm hiểu sản phẩm.","Ưu tiên câu chuyện, hình ảnh và trải nghiệm có thật.","Khối lượng phân bổ theo chủ đề và từng cao điểm."])])
                                 + callout("Bài seeding thể hiện giọng văn và cách đặt vấn đề; <b>không trình bày hội thoại dàn dựng như phản hồi khách hàng đã có.</b>")),
    ("Chủ đề theo giai đoạn", table(["Giai đoạn","Kênh brand","Seeding"],[
        ["15/11 – 31/12","Giảm rụng, phồng mềm tóc, men bia, cách dùng và nội dung 65 KOC.","Tóc xẹp/bết, rụng khi gội, tìm hiểu dầu gội và tẩy da đầu."],
        ["Tháng 01","Megalive Võ Hà Linh, KOL, HASAKI và chăm tóc đón Tết.","Câu hỏi sản phẩm và hội thoại quanh các hoạt động thực tế."],
        ["Tháng 02","Trải nghiệm theo thời gian, routine và chăm tóc sau Tết.","Quá trình sử dụng, giải đáp và chia sẻ có thật."]])),
    ("Nguồn lực và nhịp triển khai", prose("Duy trì <b>21 bài/tuần</b> trên kênh brand, tương đương 3 bài/ngày. Trong 106 ngày kế hoạch, sản lượng quy đổi là <b>318 bài brand</b>.",
        "Seeding có lịch và ngân sách theo thực tế triển khai, không tính vào 318 bài này.")),
    ("Mục tiêu và cách đánh giá", table(["Chỉ tiêu","Cơ sở tính","Báo cáo"],[
        ["500.000 lượt tiếp cận/tháng","Mục tiêu tổng hợp của hoạt động Threads; tháng 11 theo phạm vi chạy thực tế.","Tách kênh brand và tuyến seeding, ghi rõ nguồn dữ liệu."],
        ["21 bài brand/tuần","3 bài/ngày × 106 ngày = 318 bài dự kiến.","Số bài theo lịch và kết quả từng bài."],
        ["Chất lượng thảo luận","Đánh giá bình luận liên quan nhu cầu tóc/sản phẩm, tương tác và click nếu có.","Tách dữ liệu quan sát công khai và dữ liệu chủ tài khoản cung cấp."]])
        + callout("Không quy lượt xem công khai thành số người tiếp cận duy nhất. Reach tổng hợp giữa các bài hoặc tài khoản có thể trùng người.")),
  ])

PAGES["kol-koc"] = dict(
  title="Kế hoạch KOL / KOC",
  lead="Triển khai 65 KOC TikTok từ 20/11 đến 12/12/2026; booking Hoàng Kim Ngọc và Linh Remy trong tháng 01–02/2027. Chỉ tiêu trình bày ở cấp chương trình, độc lập với danh sách creator chi tiết.",
  stats=[("65 KOC","Quy mô triển khai","Lên sóng 20/11 – 12/12"),("130 sản phẩm","Gửi trải nghiệm","65 × (dầu gội + tẩy tế bào chết)"),("2 KOL lớn","Hoàng Kim Ngọc · Linh Remy","Tháng 01–02/2027"),("≈ 200.000.000 ₫","Dự kiến booking hai KOL","")],
  sections=[
    ("Phạm vi triển khai", table(["Hạng mục","Thời gian","Quy mô và nội dung"],[
        ["65 KOC TikTok","20/11 – 12/12/2026","Mỗi người nhận 1 dầu gội Men bia + 1 tẩy tế bào chết; tổng 130 sản phẩm. Sản xuất video trải nghiệm, lên sóng theo đợt."],
        ["Hoàng Kim Ngọc & Linh Remy","Tháng 01 – 02/2027","Booking hai KOL, lịch phân bổ trong tháng 01–02. Nội dung thuộc chiến dịch toàn thương hiệu Ninemila."]])
        + callout("Danh sách creator và lịch từng video được quản lý trong hồ sơ triển khai; bản kế hoạch này trình bày quy mô, vai trò và nguồn lực của chương trình.")),
    ("Nội dung video", boxes([("Sản phẩm 1","Dầu gội Men bia",["Tình trạng tóc, lý do lựa chọn và trải nghiệm gội.","Giảm rụng – kích mọc theo thông tin sản phẩm được duyệt.","Mốc giảm rụng 4 tuần gắn đúng nghiên cứu và thời gian sử dụng thực tế."]),
                               ("Sản phẩm 2","Tẩy tế bào chết da đầu",["Thao tác sử dụng, cảm giác sạch thoáng, chân tóc tơi phồng.","Hình ảnh tóc sau sử dụng và cảm nhận thực tế.","Vai trò bổ trợ với dầu gội trong routine."])])),
    ("Lịch triển khai", table(["Thời gian","Công việc chính","Phối hợp"],[
        ["15 – 19/11","Gửi sản phẩm, cung cấp brief và lập lịch.","Đồng bộ thông tin sản phẩm và tư liệu cho các kênh."],
        ["20/11 – 12/12","65 KOC lên sóng theo đợt.","Khuếch đại video tốt; fanpage, TikTok, Threads và gian hàng tiếp sức."],
        ["13/12 – 28/02","Khai thác nội dung được cấp quyền.","Tư vấn sản phẩm, quảng cáo và hỗ trợ cao điểm tháng 01."],
        ["Tháng 01 – 02","Booking Hoàng Kim Ngọc và Linh Remy.","Phân bổ lịch theo booking; truyền thông trên hệ thống kênh thương hiệu."]])),
    ("Ngân sách và sản phẩm", table(["Khoản đầu tư","Cách tính","Giá trị"],[
        ["Hai KOL lớn","Một lần cho cả chiến dịch","Khoảng 200.000.000 ₫"],
        ["Booking 65 KOC","Theo thực tế thương lượng","Theo booking"],
        ["Sản phẩm trải nghiệm","65 × (1 dầu gội + 1 tẩy tế bào chết)","130 sản phẩm"],
        ["Quảng cáo video KOC","Đã nằm trong TikTok Ads; không cộng lại","5.000.000 ₫/tháng"]], num=(2,))),
    ("Mục tiêu và phương pháp đánh giá", table(["Chỉ tiêu kế hoạch","Cơ sở / phương pháp","Đánh giá sau triển khai"],[
        ["65 KOC tham gia","Quy mô đã đặt cho chương trình; danh sách từng người thuộc kế hoạch thực thi.","Số creator thực tế và video hợp lệ đã lên sóng."],
        ["2 KOL lớn trong tháng 01–02","Hoàng Kim Ngọc và Linh Remy; lịch phân bổ theo booking.","Nội dung lên sóng và quyền khai thác được bàn giao."],
        ["Công ty + KOC: hơn 3.000.000 lượt tiếp cận","Mục tiêu chung TikTok; gồm nội dung công ty, creator và quảng cáo.","Báo cáo theo nguồn: kênh công ty, KOC và quảng cáo."],
        ["Cộng KOL: kỳ vọng 5.000.000 – 6.000.000 lượt tiếp cận","Mục tiêu chung chiến dịch; không coi là KPI riêng của từng creator.","Báo cáo theo từng nhóm nguồn, giữ riêng reach và views."]])
        + callout("Các con số là mục tiêu dự kiến, không phải kết quả đã đạt. Khi cộng giữa tài khoản hoặc tháng có thể trùng người xem; chỉ gọi là người tiếp cận duy nhất nếu có dữ liệu khử trùng.")),
  ])

PAGES["megalive"] = dict(
  title="Kế hoạch Megalive Võ Hà Linh",
  lead="Megalive Võ Hà Linh chào 2027 trong tháng 01 là cao điểm chủ lực. Hệ thống kênh Ninemila phối hợp giới thiệu sản phẩm, thông báo phiên live và tư vấn khách trước, trong và sau sự kiện.",
  stats=[("Tháng 01/2027","Thời gian dự kiến","Megalive chào 2027"),("Võ Hà Linh","Đối tác megalive",""),("≈ 150.000.000 ₫","Ngân sách dự kiến","Một khoản cho chiến dịch"),("3 giai đoạn","Trước · Trong · Sau live","")],
  sections=[
    ("Phạm vi hoạt động", boxes([("Mục đích","Vai trò trong chiến dịch",["Tạo cao điểm truyền thông và bán hàng tháng 01.","Tận dụng độ phủ đã tích lũy từ 65 KOC và hệ thống kênh công ty.","Nội dung phối hợp toàn thương hiệu Ninemila."]),
                                 ("Công việc","Các hạng mục triển khai",["Thông báo lịch và đường dẫn theo thông tin booking.","Chuẩn bị ảnh/video giới thiệu sản phẩm, nội dung tư vấn.","Phối hợp các kênh và tổng hợp kết quả sau phiên."])])),
    ("Kế hoạch trước – trong – sau live", table(["Giai đoạn","Công việc","Đầu ra"],[
        ["Trước live","Xác nhận thông tin phiên; chuẩn bị tư liệu, nội dung giới thiệu và giải đáp; công bố, nhắc lịch.","Bộ nội dung sản phẩm, banner phiên live và lịch đăng trên các kênh."],
        ["Trong live","Cập nhật đường dẫn; dẫn khách theo dõi; tư vấn, giải đáp.","Thông tin thống nhất trên các kênh và nội dung hỗ trợ khách."],
        ["Sau live","Hướng dẫn sử dụng, chia sẻ tư liệu được cấp quyền, tổng hợp hiệu quả.","Nội dung sau live và báo cáo từ nguồn dữ liệu thực tế."]])),
    ("Bộ tư liệu truyền thông", prose("Gồm ảnh/video giới thiệu trước live (teaser hoặc video dọc) và hình ảnh trong hoặc sau phiên.",
        "Bộ tư liệu được dùng cho fanpage, Instagram, TikTok, Threads, website và đại lý theo phạm vi booking.")),
    ("Phối hợp các kênh", table(["Nhóm kênh","Trước và trong phiên","Sau phiên"],[
        ["Fanpage & Instagram","Sản phẩm, thông báo lịch, nhắc lịch và đường dẫn.","Hướng dẫn dùng và tư liệu được cấp quyền."],
        ["TikTok & Threads","Video, chủ đề thảo luận, giới thiệu sản phẩm và dẫn người xem.","Giải đáp và nội dung tiếp nối."],
        ["Gian hàng, website & đại lý","Thông tin sản phẩm, nơi mua và tư vấn.","Tiếp tục tư vấn, cập nhật nội dung sản phẩm."]])),
    ("Ngân sách", table(["Hạng mục","Cách tính","Ngân sách"],[
        ["Megalive Võ Hà Linh","Khoản dự kiến cho chiến dịch; không nhân số tháng. Phạm vi chi phí theo booking.","Khoảng 150.000.000 ₫"],
        ["Quảng cáo công ty hỗ trợ live","Phân bổ trong ngân sách quảng cáo tháng 01 đã có.","Không cộng lần hai"]], num=(2,))),
    ("Mục tiêu và phương pháp đánh giá", table(["Mục tiêu kế hoạch","Cách đánh giá","Nguồn dữ liệu"],[
        ["Tổ chức cao điểm megalive tháng 01","Phiên diễn ra theo booking; sản phẩm và nội dung triển khai đúng phạm vi.","Hồ sơ booking và báo cáo phiên."],
        ["Phối hợp truyền thông đủ ba giai đoạn","Số nội dung đã thực hiện so với lịch triển khai được phê duyệt.","Các kênh công ty."],
        ["Đánh giá hiệu quả tiếp cận và tương tác","Báo cáo riêng lượt xem, tiếp cận, tương tác, click; không tự quy đổi sang người duy nhất.","Nền tảng và dữ liệu bên tổ chức cung cấp."]])
        + callout("Mục tiêu doanh số và chỉ tiêu người xem riêng cho phiên chưa được đưa vào dự toán. Ngày giờ, SKU và lịch nội dung cụ thể thuộc hồ sơ triển khai.")),
  ])

PAGES["tiktok"] = dict(
  title="Kế hoạch TikTok",
  lead="Triển khai trên hai kênh Kigo Group Vietnam và Ninemilavn, kết hợp video thương hiệu, nội dung creator, quảng cáo và livestream hằng ngày từ 15/12/2026.",
  stats=[("2 kênh","Kigo Group Vietnam · Ninemilavn",""),("60.000.000 ₫","Quảng cáo / tháng","Chạy lẻ · tiếp cận · video KOC"),("4 giờ/ngày","Livestream TikTok & Shopee","Chung hai nền tảng"),("15/12 – 28/02","Thời gian livestream","76 ngày · 304 giờ")],
  sections=[
    ("Các nhóm video", boxes([("Nhóm 1","Trải nghiệm sản phẩm",["Dầu gội, tẩy tế bào chết và các sản phẩm phù hợp nhu cầu.","Thao tác, kết cấu và hình ảnh tóc.","Nội dung model và trả lời câu hỏi."]),
                              ("Nhóm 2","Creator & chiến dịch",["Khai thác KOC/KOL theo quyền sử dụng.","Megalive Võ Hà Linh và HASAKI.","Video dẫn về gian hàng và livestream."])])),
    ("Kế hoạch theo giai đoạn", table(["Giai đoạn","Nội dung","Quảng cáo / livestream"],[
        ["15/11 – 31/12","Model, sản phẩm và 65 KOC; bám nhu cầu tìm mua dịp 12.12.","Chạy quảng cáo; bắt đầu livestream hằng ngày từ 15/12."],
        ["Tháng 01","Megalive Võ Hà Linh, KOL và hoạt động bán lẻ.","Duy trì ads; live hằng ngày, nội dung bám cao điểm."],
        ["Tháng 02","KOL theo lịch, routine, trải nghiệm và HASAKI.","Duy trì ads và live đến hết 28/02."]])),
    ("Livestream công ty", prose("<b>4 giờ/ngày</b> trên hai nền tảng TikTok và Shopee, từ 15/12/2026 đến 28/02/2027: 76 ngày, tương đương <b>304 giờ</b> kế hoạch chung (chưa nhân đôi thành 608 giờ cho hai nền tảng).",
        "Nội dung gồm giới thiệu hệ sản phẩm, hướng dẫn lựa chọn, cách sử dụng và giải đáp trực tiếp. Phân bổ giờ giữa hai nền tảng theo lịch vận hành.")),
    ("Ngân sách", table(["Hạng mục","Định mức","Cơ sở tính"],[
        ["Chạy lẻ TikTok","50.000.000 ₫/tháng","Nằm trong tổng TikTok Ads"],
        ["Chạy tiếp cận","5.000.000 ₫/tháng","Nằm trong tổng TikTok Ads"],
        ["Quảng cáo video KOC","5.000.000 ₫/tháng","Nằm trong tổng TikTok Ads"],
        ["Vận hành livestream chung","15.000.000 ₫ × (17/31 + 2)","38.225.806 ₫ · dùng chung với Shopee, ghi một lần"]],
        total=["Tổng TikTok Ads","60.000.000 ₫ × (16/30 + 3)","212.000.000 ₫"])),
    ("Mục tiêu và cách đánh giá", table(["Mục tiêu","Phạm vi","Cách đánh giá"],[
        ["Công ty + KOC: hơn 3.000.000 lượt tiếp cận","Mục tiêu TikTok chung, không gán riêng cho kênh công ty.","Tách organic công ty, creator và ads trong báo cáo."],
        ["Cộng KOL: kỳ vọng 5.000.000 – 6.000.000","Mục tiêu tổng hợp toàn chiến dịch.","Ghi rõ reach / views theo nguồn, tránh cộng trùng trong cùng báo cáo."],
        ["Livestream liên tục","76 ngày / 304 giờ chung hai nền tảng.","Lịch live, thời lượng và báo cáo phiên thực tế."]])),
  ])

PAGES["shopee"] = dict(
  title="Kế hoạch Shopee",
  lead="Triển khai trên hai gian hàng Sắc đẹp & Sức khỏe và Ninemilavn, cập nhật bộ banner SIS Ninemila, quảng cáo nội sàn và livestream hằng ngày từ 15/12/2026.",
  stats=[("2 gian hàng","Phạm vi triển khai","Sắc đẹp & Sức khỏe · Ninemilavn"),("10.000.000 ₫","Ads / tháng cho cả hai",""),("SIS Ninemila","Bộ nhận diện gian hàng",""),("15/12 – 28/02","Livestream hằng ngày","Dùng chung lịch với TikTok")],
  sections=[
    ("Chuẩn bị gian hàng", boxes([("Gian hàng","Hình ảnh & thông tin",["Đồng bộ banner SIS và nhận diện Ninemila.","Cập nhật thông tin sản phẩm, hướng dẫn dùng và ảnh chi tiết.","Bổ sung video creator theo quyền sử dụng."]),
                                  ("Bán hàng","Quảng cáo & tư vấn",["Phân bổ 10.000.000 ₫/tháng cho cả hai shop.","Theo dõi sản phẩm và nội dung thu hút nhu cầu tìm mua.","Kết nối tư vấn và livestream."])])),
    ("Kế hoạch theo giai đoạn", table(["Giai đoạn","Gian hàng","Ads và livestream"],[
        ["15/11 – 31/12","Cập nhật SIS, sản phẩm và nội dung creator; chuẩn bị siêu sale 12.12.","Ads từ 15/11; livestream hằng ngày từ 15/12."],
        ["Tháng 01","Thông tin sản phẩm, video được cấp quyền; nội dung theo chiến dịch.","Duy trì ads, livestream và tư vấn."],
        ["Tháng 02","Cập nhật nội dung hệ sản phẩm và trải nghiệm.","Duy trì ads và livestream đến 28/02."]])),
    ("Ngân sách", table(["Hạng mục","Cách tính","Tổng"],[
        ["Shopee Ads","10.000.000 ₫ × (16/30 + 3)","35.333.333 ₫"],
        ["Livestream công ty","Dùng chung 4 giờ/ngày và chi phí vận hành với TikTok.","Không cộng lần hai"]], num=(2,))),
    ("Đánh giá triển khai", table(["Nhóm đánh giá","Chỉ tiêu / phạm vi kế hoạch","Nguồn dữ liệu"],[
        ["Hoàn thiện gian hàng","Hai shop có SIS và nội dung sản phẩm Ninemila.","Ảnh gian hàng và nội dung sản phẩm."],
        ["Quảng cáo","Chi phí, lượt hiển thị, click và hiệu quả theo báo cáo nội sàn.","Báo cáo Shopee Ads; không đặt doanh số khi chưa có chỉ tiêu."],
        ["Livestream","Đánh giá theo lịch và thời lượng phân bổ từ kế hoạch chung.","Báo cáo phiên Shopee Live."]])),
  ])

PAGES["dai-ly"] = dict(
  title="Kế hoạch truyền thông đại lý",
  lead="Huy động hệ thống 50 đại lý đăng bài Ninemila trong tháng 12/2026, sử dụng tư liệu công ty kết hợp nội dung tự sản xuất phù hợp với khách hàng của từng đại lý.",
  stats=[("50 đại lý","Quy mô mục tiêu",""),("30 bài/đại lý","Trong tháng 12",""),("1.500 bài","Tổng sản lượng kế hoạch","50 × 30 bài"),("30 bộ quà","Mỗi bộ 5 sản phẩm","Cho 30 đại lý tốt nhất")],
  sections=[
    ("Quy mô và cơ chế", boxes([("Tháng 12","Đăng bài",["50 đại lý × 30 bài = 1.500 bài truyền thông.","Nội dung từ bộ tư liệu và câu chuyện thực tế của đại lý.","Link bài được lưu để tổng hợp kết quả."]),
                                ("Ghi nhận","Quà cho 30 đại lý tốt nhất",["30 bộ, mỗi bộ gồm 5 sản phẩm Ninemila.","Đề xuất xét mức hoàn thành, chất lượng nội dung và kết quả tương tác.","Cơ chế chấm chi tiết công bố trong hướng dẫn triển khai."])])),
    ("Bộ tư liệu cung cấp", prose("Gồm bài mẫu (ảnh sản phẩm, nội dung đăng) và gợi ý để đại lý tự sản xuất review/video.",
        "Bộ nội dung bao gồm sản phẩm, trải nghiệm KOC được cấp quyền, cách dùng, giải đáp và các hoạt động thương hiệu.")),
    ("Lịch chương trình", table(["Thời gian","Hoạt động","Đầu ra"],[
        ["Cuối tháng 11","Chuẩn bị tư liệu và hướng dẫn.","Bộ nội dung, cách lưu link và hướng dẫn chương trình."],
        ["Tháng 12","50 đại lý thực hiện lịch đăng.","Mục tiêu 30 bài/đại lý, tổng 1.500 bài."],
        ["Sau tháng 12","Tổng hợp kết quả và chọn 30 đại lý tốt nhất.","Báo cáo nội dung và phân bổ 30 bộ quà."],
        ["Tháng 01 – 02","Duy trì thông tin sản phẩm và hỗ trợ cao điểm.","Nội dung tư vấn và truyền thông theo hoạt động thực tế."]])),
    ("Nguồn lực", prose("<b>30 bộ quà × 5 sản phẩm = 150 sản phẩm.</b> Giá trị sản phẩm theo dõi riêng với ngân sách tiền mặt; chưa cộng vào tổng 862.225.806 ₫ đã có định mức.")),
    ("Đánh giá kết quả", table(["Chỉ tiêu","Công thức","Cách kiểm tra"],[
        ["50 đại lý tham gia","Số đại lý có hoạt động đăng bài trong chương trình.","Danh sách và link bài thực tế."],
        ["1.500 bài","50 × 30 bài. Tỷ lệ hoàn thành = bài hợp lệ / 1.500.","Kiểm tra link, thời gian và nội dung."],
        ["30 đại lý nhận quà","Lựa chọn theo kết quả chương trình.","Tổng hợp số bài, chất lượng và dữ liệu tương tác có thể kiểm chứng."]])),
  ])

PAGES["hasaki"] = dict(
  title="Kế hoạch HASAKI",
  lead="Triển khai Ninemila tại HASAKI từ tháng 01/2027, kết hợp livestream độc quyền, activation tại chi nhánh và PG tư vấn bán hàng trong giai đoạn tháng 01–02.",
  stats=[("Từ tháng 01","Triển khai dự kiến",""),("Tháng 01 – 02","Livestream độc quyền",""),("Activation & PG","Hoạt động tại chi nhánh",""),("≥ 50.000.000 ₫","Ngân sách activation & PG","Tạm tính mức tối thiểu")],
  sections=[
    ("Ba nhóm hoạt động", boxes([("Online","Livestream độc quyền",["Dự kiến trong tháng 01 và tháng 02.","Giới thiệu sản phẩm, cách dùng và tương tác trực tiếp.","Phối hợp truyền thông với kênh công ty."]),
                                 ("Tại điểm bán","Activation tại chi nhánh",["Giới thiệu và tạo cơ hội trải nghiệm sản phẩm.","Chuẩn bị tư liệu và nội dung tư vấn.","Khai thác hình ảnh hoạt động thực tế."]),
                                 ("Nhân sự","PG tư vấn bán hàng",["Giới thiệu hệ sản phẩm theo nhu cầu tóc.","Hướng dẫn lựa chọn và sử dụng.","Tổng hợp câu hỏi thực tế để bổ sung nội dung."])], three=True)),
    ("Phương án hình ảnh", prose("Chuẩn bị thiết kế khu vực activation (bố trí sản phẩm, POSM) và hình ảnh PG (đồng phục, vị trí đứng, tư liệu tư vấn).")),
    ("Kế hoạch theo giai đoạn", table(["Giai đoạn","Công việc","Truyền thông phối hợp"],[
        ["Tháng 12","Chuẩn bị tư liệu, hình ảnh và nội dung tư vấn.","Chuẩn bị thông tin giới thiệu hoạt động bán lẻ."],
        ["Tháng 01","Triển khai hiện diện, livestream độc quyền, activation và PG.","Cập nhật điểm bán, hình ảnh hoạt động và nội dung sản phẩm."],
        ["Tháng 02","Tiếp tục livestream độc quyền và hoạt động tại chi nhánh theo thực tế.","Khai thác tư liệu, giải đáp và nội dung chăm tóc."]])),
    ("Ngân sách", table(["Phạm vi","Cách tính","Dự kiến"],[
        ["Activation & PG","Tạm tính một khoản cho toàn chiến dịch; theo thực tế triển khai.","Tối thiểu 50.000.000 ₫"],
        ["Livestream độc quyền và khoản khác","Theo phạm vi phối hợp thực tế.","Theo triển khai"]], num=(2,))
        + callout("Không mặc định triển khai tại toàn bộ hệ thống. Phạm vi chi nhánh, ngày hoạt động và nhân sự phân bổ theo kế hoạch thực thi.")),
    ("Mục tiêu và đánh giá", table(["Mục tiêu kế hoạch","Cách đánh giá","Cơ sở báo cáo"],[
        ["Hiện diện tại HASAKI từ tháng 01","Phạm vi điểm bán và sản phẩm thực tế.","Danh sách điểm triển khai và hình ảnh."],
        ["Livestream độc quyền tháng 01–02","Số phiên, nội dung và kết quả theo thỏa thuận.","Báo cáo phiên được cung cấp."],
        ["Activation và PG","Số ngày hoạt động, điểm triển khai, tư vấn và câu hỏi khách.","Báo cáo nhân sự, ảnh và dữ liệu được ghi nhận."]])),
  ])

PAGES["website"] = dict(
  title="Kế hoạch website",
  lead="Cập nhật song song thông tin Ninemila trên kigora.vn và kigora.com, kết nối nội dung thương hiệu, sản phẩm và các hoạt động chiến dịch với thông tin nơi mua.",
  stats=[("2 website","kigora.vn · kigora.com",""),("Toàn chiến dịch","15/11 – 28/02",""),("Sản phẩm & hoạt động","Trục nội dung",""),("Theo cao điểm","Nhịp cập nhật","")],
  sections=[
    ("Các hạng mục cập nhật", boxes([("Thường trực","Thông tin sản phẩm",["Hệ sản phẩm, lợi ích, cách dùng và lựa chọn theo nhu cầu.","Ảnh/video phù hợp từ bộ tư liệu model và creator.","Thông tin nơi mua và kênh chính hãng."]),
                                     ("Theo chiến dịch","Tin hoạt động",["65 KOC và nội dung trải nghiệm.","Megalive Võ Hà Linh, KOL và HASAKI.","Hướng dẫn chăm tóc theo từng giai đoạn."])])),
    ("Nội dung theo giai đoạn", table(["Giai đoạn","Nội dung","Vai trò"],[
        ["15/11 – 31/12","Sản phẩm, KOC, trải nghiệm và nơi mua.","Cung cấp thông tin nhất quán khi khách tìm hiểu."],
        ["Tháng 01","Megalive Võ Hà Linh, KOL và HASAKI.","Cập nhật sự kiện, hoạt động và điểm bán."],
        ["Tháng 02","KOL, trải nghiệm dài ngày, chăm tóc và hoạt động bán lẻ.","Duy trì thông tin và hỗ trợ lựa chọn sản phẩm."]])),
    ("Tư liệu và vận hành", prose("Tận dụng bộ ảnh/video đã sản xuất và nội dung creator được cấp quyền; cập nhật theo từng sự kiện.",
        "Chưa đặt ngân sách website riêng khi chưa có định mức bổ sung.")),
    ("Đánh giá triển khai", table(["Nhóm đánh giá","Cách thực hiện","Nguồn dữ liệu"],[
        ["Độ đầy đủ thông tin","Kiểm tra sản phẩm, nội dung và nơi mua trên cả hai website.","Danh mục URL và nội dung công bố."],
        ["Traffic từ chiến dịch","Đề xuất gắn nguồn vào link công ty/creator để phân biệt nguồn truy cập.","Công cụ phân tích website nếu đã được thiết lập."],
        ["Mức quan tâm nội dung","Theo dõi lượt vào trang sản phẩm, bài viết và click sang nơi mua nếu đo được.","Báo cáo website; không tự tạo số liệu khi chưa có tracking."]])),
  ])

def build_sub(slug):
    p = next(x for x in PLANS if x["slug"] == slug); d = PAGES[slug]
    i = INTERNAL.index(p); prev = INTERNAL[i-1] if i > 0 else None; nxt = INTERNAL[i+1] if i < len(INTERNAL)-1 else None
    ids = [f"muc-{k}" for k in range(1, len(d["sections"]) + 1)]
    toc = "".join(f'<a href="#{ids[k]}">{k+1}. {E(t)}</a>' for k, (t, _) in enumerate(d["sections"]))
    secs = "".join(f'<section id="{ids[k]}"><h2><span>{k+1:02d}</span>{E(t)}</h2>{body}</section>' for k, (t, body) in enumerate(d["sections"]))
    pager = '<nav class="pager">' + (f'<a href="{prev["url"]}"><small>← Kế hoạch trước</small><b>{E(prev["name"])}</b></a>' if prev else '<a href="index.html"><small>← Trang chủ</small><b>Tổng quan IMC</b></a>') \
          + (f'<a class="next" href="{nxt["url"]}"><small>Kế hoạch tiếp →</small><b>{E(nxt["name"])}</b></a>' if nxt else '<a class="next" href="index.html"><small>Trang chủ →</small><b>Tổng quan IMC</b></a>') + '</nav>'
    out = head(f'{d["title"]} · Booming Ninemila', d["lead"]) + f"""<header class="cover sub">
  <div class="wrap">
    {topbar(slug)}
    <div class="hero"><div>
      <div class="crumb"><a href="index.html">Tổng quan IMC</a> / {E(p["name"])}</div>
      <div class="kicker">Kế hoạch {p["no"]} · Booming Ninemila</div>
      <h1>{E(d["title"])}</h1>
      <p class="lead">{E(d["lead"])}</p>
      <dl class="meta"><dt class="label">Thời gian</dt><dd>{PERIOD}</dd><dt class="label">Loại kế hoạch</dt><dd>Dự kiến triển khai</dd></dl>
    </div></div>
  </div>
</header>
{stats(d["stats"])}
<main class="wrap layout">
  <aside class="toc"><span class="label">Mục lục</span>{toc}</aside>
  <div class="content">{secs}{pager}</div>
</main>
""" + FOOT
    open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8").write(out)

# ───────────────────────── Trang chủ ─────────────────────────
MATRIX_COLS = [("20/11 – 31/12/2026","65 KOC · Siêu sale 12.12 · Đại lý"),("Tháng 01/2027","Megalive Võ Hà Linh · KOL · HASAKI"),("Tháng 02/2027","KOL · HASAKI · Duy trì livestream")]
# (nhóm, [(tên hàng, link slug, [(tiêu đề, nội dung, trọng tâm?) × 3])])
MATRIX = [
 ("creator","Creator & sự kiện",[
   ("65 KOC TikTok","kol-koc",[("Lên sóng 20/11 – 12/12","65 KOC, mỗi người nhận dầu gội + tẩy tế bào chết. Chọn video để chạy ads và khai thác lại.",1),("Khai thác nội dung KOC","Dùng video được cấp quyền để hỗ trợ megalive và tư vấn sản phẩm.",0),("Khai thác nội dung KOC","Tiếp tục sử dụng nội dung theo thời hạn và quyền đã thỏa thuận.",0)]),
   ("Megalive Võ Hà Linh","megalive",[("Chuẩn bị megalive","Tư liệu sản phẩm, nội dung giới thiệu; phối hợp lịch truyền thông trên các kênh.",0),("Megalive chào 2027","Cao điểm chủ lực toàn chiến dịch. Thông báo, dẫn người xem, phối hợp các kênh và tư vấn sau live.",1),("Nội dung sau megalive","Tiếp tục giải đáp và khai thác tư liệu được phép sử dụng.",0)]),
   ("Hoàng Kim Ngọc · Linh Remy","kol-koc",[("Chuẩn bị booking","Chốt lịch lên sóng và quyền sử dụng nội dung.",0),("Booking KOL theo lịch","Hai KOL được phân bổ lên sóng trong tháng 01–02.",1),("Booking KOL theo lịch","Tiếp nối lịch đã chốt; khuếch đại trên kênh thương hiệu.",1)]),
 ]),
 ("brand","Kênh truyền thông thương hiệu",[
   ("Fanpage branding & Instagram","fanpage",[("Nội dung sản phẩm & KOC","Fanpage khoảng 5 bài/tuần; Instagram điều chỉnh định dạng. Giảm rụng, phồng mềm tóc và hoạt động 12.12.",0),("Nội dung bám cao điểm","Megalive Võ Hà Linh, KOL, HASAKI và chăm tóc đón Tết.",0),("KOL & trải nghiệm sử dụng","Giới thiệu hệ sản phẩm, trải nghiệm thực tế và routine.",0)]),
   ("Threads · Brand & seeding","threads",[("Triển khai hai tuyến bài","Brand: 21 bài/tuần. Seeding: thảo luận tóc rụng, tóc xẹp và trải nghiệm có thật.",0),("Bám sự kiện tháng 01","Brand: megalive, KOL, HASAKI. Seeding: câu hỏi, thảo luận và trải nghiệm thực tế.",0),("Duy trì hội thoại","Brand: 21 bài/tuần. Seeding: quá trình sử dụng, routine và giải đáp.",0)]),
   ("kigora.vn · kigora.com","website",[("Cập nhật đồng thời hai web","Thông tin sản phẩm, KOC, chiến dịch và nơi mua.",0),("Cập nhật các hoạt động lớn","Megalive, KOL, HASAKI và thông tin điểm bán.",0),("Cập nhật nội dung Ninemila","Hệ sản phẩm, hoạt động và nội dung chăm sóc tóc.",0)]),
 ]),
 ("ads","Quảng cáo & livestream bán hàng",[
   ("3 fanpage bán lẻ","fanpage",[("Nội dung & quảng cáo","2 bài/page/ngày. Facebook Ads 50.000.000 ₫/tháng, tính từ 15/11.",0),("Quảng cáo bám cao điểm","50.000.000 ₫/tháng. Nội dung KOC/KOL và megalive theo quyền sử dụng.",0),("Duy trì quảng cáo","50.000.000 ₫/tháng; tiếp tục nội dung và tư vấn sản phẩm.",0)]),
   ("TikTok · 2 kênh công ty","tiktok",[("Video, ads & livestream","Ads 60.000.000 ₫/tháng (chạy lẻ, tiếp cận, video KOC). Livestream hằng ngày từ 15/12.",0),("Livestream & quảng cáo","Duy trì 60.000.000 ₫/tháng. Khai thác megalive và KOL; livestream hằng ngày.",0),("Livestream & quảng cáo","Duy trì ads và livestream đến hết 28/02.",0)]),
   ("Shopee · 2 gian hàng","shopee",[("SIS, ads & livestream","Thay bộ banner SIS Ninemila. Ads tổng 10.000.000 ₫/tháng; livestream từ 15/12.",0),("Livestream & quảng cáo","10.000.000 ₫/tháng cho hai gian hàng. Nội dung bám hoạt động chiến dịch.",0),("Livestream & quảng cáo","Duy trì gian hàng, ads và livestream đến hết 28/02.",0)]),
 ]),
 ("retail","Đại lý & bán lẻ",[
   ("Hệ thống đại lý","dai-ly",[("Chương trình tháng 12","50 đại lý × 30 bài = 1.500 bài. 30 đại lý tốt nhất nhận bộ quà 5 sản phẩm.",1),("Duy trì truyền thông","Tư liệu sản phẩm, nội dung cao điểm và tư vấn khách hàng.",0),("Duy trì truyền thông","Nội dung sản phẩm và tư vấn khách hàng.",0)]),
   ("HASAKI","hasaki",[("Chuẩn bị triển khai","Tư liệu sản phẩm và kế hoạch hoạt động điểm bán.",0),("Triển khai tại HASAKI","Livestream độc quyền. Activation tại chi nhánh và PG tư vấn, bán hàng.",1),("Tiếp tục hoạt động HASAKI","Livestream độc quyền tháng 02. Activation và PG theo thực tế triển khai.",1)]),
 ]),
]

def link_of(slug):
    p = next(x for x in PLANS if x["slug"] == slug)
    return p["url"], p["ext"]

def build_index():
    plans = "".join(
        f'<a class="plan" href="{E(p["url"])}"{" target=\"_blank\" rel=\"noopener\"" if p["ext"] else ""}>'
        f'<span class="no">{p["no"]}</span><h3>{E(p["name"])}{"<small>Trang lịch & brief riêng ↗</small>" if p["ext"] else ""}</h3>'
        f'<p>{E(p["short"])}</p><span class="kpi">{E(p["kpi"])}<small>{E(p["kpi_sub"])}</small></span><span class="go">{"↗" if p["ext"] else "→"}</span></a>' for p in PLANS)

    groups = [("all","Tất cả nhóm")] + [(g, n) for g, n, _ in MATRIX]
    chips = "".join(f'<button class="chip" type="button" data-g="{g}" aria-pressed="{str(g=="all").lower()}">{E(n)}</button>' for g, n in groups)
    rows = ""
    for g, gname, items in MATRIX:
        rows += f'<tr class="grp" data-g="{g}"><td colspan="4">{E(gname)}</td></tr>'
        for name, slug, cells in items:
            url, ext = link_of(slug)
            rows += f'<tr data-g="{g}"><td class="row"><a href="{E(url)}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}>{E(name)}&nbsp;{"↗" if ext else "→"}</a></td>' + "".join(
                f'<td class="{"hot" if hot else ""}"><b>{E(t)}</b>{E(c)}</td>' for t, c, hot in cells) + "</tr>"
    mhead = '<tr><th>Kênh / hoạt động</th>' + "".join(f'<th><b>{E(a)}</b><span>{E(b)}</span></th>' for a, b in MATRIX_COLS) + "</tr>"

    activities = table(["Hoạt động","Thời gian","Nội dung và quy mô","Ngân sách dự kiến"],[
        ["Booking 65 KOC TikTok","20/11 – 12/12/2026","<ul><li>65 KOC sản xuất video trải nghiệm Ninemila.</li><li>Mỗi người nhận 1 dầu gội Men bia và 1 tẩy tế bào chết da đầu: tổng 65 bộ, 130 sản phẩm.</li><li>Video lên sóng theo đợt; chọn nội dung phù hợp để chạy quảng cáo và đăng lại theo quyền sử dụng.</li></ul>","Theo thực tế thương lượng" + sm("Sản phẩm gửi KOC theo dõi riêng.")],
        ["Megalive Võ Hà Linh","Tháng 01/2027<br><span class=\"tag\">Cao điểm chủ lực</span>","<ul><li>Tháng 01 tập trung truyền thông cho megalive chào 2027.</li><li>Các kênh cùng thông báo, dẫn người xem đến phiên live và tiếp tục tư vấn sau live.</li></ul>","≈ 150.000.000 ₫" + sm("Phạm vi phiên theo booking.")],
        ["Hoàng Kim Ngọc và Linh Remy","Tháng 01 – 02/2027","<ul><li>Booking hai KOL lớn; phân bổ lịch lên sóng trong tháng 01–02.</li><li>Kênh thương hiệu và quảng cáo khai thác nội dung theo thỏa thuận sử dụng.</li></ul>","≈ 200.000.000 ₫" + sm("Ngân sách chung cho hai KOL.")],
        ["HASAKI","Từ tháng 01/2027","<ul><li>Triển khai hiện diện Ninemila tại hệ thống HASAKI.</li><li>Livestream độc quyền dự kiến trong tháng 01 và tháng 02.</li><li>Activation tại chi nhánh và bố trí PG tư vấn, bán sản phẩm.</li></ul>","≥ 50.000.000 ₫" + sm("Activation và PG; theo thực tế triển khai.")],
        ["Livestream hằng ngày","15/12/2026 – 28/02/2027","<ul><li>4 giờ/ngày trên hai nền tảng TikTok và Shopee.</li><li>Giới thiệu sản phẩm, hướng dẫn sử dụng, tư vấn và giải đáp trực tiếp.</li></ul>","≈ 15.000.000 ₫/tháng" + sm("Chi phí vận hành, tính từ 15/12.")],
        ["Truyền thông đại lý","Tháng 12/2026","<ul><li>50 đại lý, mỗi đại lý 30 bài: mục tiêu 1.500 bài truyền thông.</li><li>30 đại lý có kết quả tốt nhất nhận bộ quà gồm 5 sản phẩm Ninemila.</li></ul>","30 bộ quà" + sm("Tổng 150 sản phẩm; giá trị theo dõi riêng.")],
    ], num=(3,))

    budget_a = table(["Hạng mục","Đơn giá / tháng","15 – 30/11","Tháng 12","Tháng 01","Tháng 02","Tổng chiến dịch"],[
        ["Facebook Ads","50.000.000","26.666.667","50.000.000","50.000.000","50.000.000","176.666.667"],
        ["TikTok Ads" + sm("Chạy lẻ 50tr + tiếp cận 5tr + video KOC 5tr"),"60.000.000","32.000.000","60.000.000","60.000.000","60.000.000","212.000.000"],
        ["Shopee Ads" + sm("Tổng hai gian hàng"),"10.000.000","5.333.333","10.000.000","10.000.000","10.000.000","35.333.333"],
        ["Vận hành livestream" + sm("Bắt đầu từ 15/12/2026"),"15.000.000","—","8.225.806","15.000.000","15.000.000","38.225.806"],
    ], num=(1,2,3,4,5,6), total=["Tổng A","—","64.000.000","128.225.806","135.000.000","135.000.000","462.225.806"])
    budget_b = table(["Hạng mục","Cơ sở tính","Ngân sách dự kiến"],[
        ["Booking Hoàng Kim Ngọc và Linh Remy","Ngân sách chung cho hai KOL, lên sóng trong tháng 01–02.","200.000.000"],
        ["Megalive Võ Hà Linh","Một khoản cho chiến dịch; phạm vi phiên theo booking.","150.000.000"],
        ["HASAKI · Activation và PG","Tạm tính mức tối thiểu cho chiến dịch; cập nhật theo thực tế.","50.000.000"],
    ], num=(2,), total=["Tổng B","Ba hạng mục đã có mức dự kiến","400.000.000"])
    budget_c = ul(["<b>Booking 65 KOC:</b> theo thực tế thương lượng.","<b>Threads seeding:</b> theo thực tế triển khai.",
                   "<b>Sản phẩm gửi 65 KOC:</b> mỗi người 1 dầu gội và 1 tẩy tế bào chết; tổng 130 sản phẩm.","<b>Quà đại lý:</b> 30 bộ × 5 sản phẩm; tổng 150 sản phẩm.",
                   "<b>Các khoản khác chưa có đơn giá:</b> chi phí sản xuất tư liệu đã thực hiện, phát sinh và phần HASAKI vượt mức tạm tính (nếu có)."])

    out = head("Booming Ninemila · Kế hoạch truyền thông tích hợp", "Kế hoạch IMC Ninemila tại Việt Nam, 15/11/2026 – 28/02/2027") + f"""<header class="cover">
  <div class="wrap">
    {topbar("index")}
    <div class="hero">
      <div>
        <div class="kicker">Kigo Group · Thị trường Việt Nam</div>
        <h1>Booming Ninemila<em>Kế hoạch truyền thông tích hợp (IMC) 2026–2027</em></h1>
        <p class="slogan">“Giảm rụng từ 4 tuần, đón mái tóc bồng bềnh mềm mượt.”</p>
        <dl class="meta">
          <dt class="label">Thời gian</dt><dd>{PERIOD} · 106 ngày</dd>
          <dt class="label">Thương hiệu</dt><dd>Ninemila – thương hiệu chăm sóc tóc Hàn Quốc, Top 1 Hair Care tại Olive Young.</dd>
          <dt class="label">Trục thông điệp</dt><dd>Giảm rụng – kích mọc · Phồng, mềm, mượt tóc.</dd>
        </dl>
      </div>
      <div class="product"><img src="assets/anh-bia.jpg" alt="Dầu gội Men bia Ninemila Calming Beer"><span>Calming Beer</span></div>
    </div>
  </div>
</header>
{stats([("65 KOC","Tham gia chiến dịch","Lên sóng 20/11 – 12/12"),("4 fanpage","Đã xây dựng","1 branding · 3 bán lẻ vệ tinh"),("120.000.000 ₫","Quảng cáo / tháng","Facebook · TikTok · Shopee"),("5–6 triệu","Lượt tiếp cận kỳ vọng","TikTok công ty + KOC + KOL")], "Mục tiêu toàn chiến dịch. Lượt tiếp cận tổng hợp có thể trùng người xem.")}

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="label">01 · Danh mục</span><h2>Kế hoạch chi tiết <em>theo kênh</em></h2></div><p>9 kế hoạch, mỗi kế hoạch một trang riêng. Fanpage & Instagram mở trang lịch & brief đang vận hành.</p></div>
  <div class="plans">{plans}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="label">02 · Nền tảng</span><h2>Đã có trong tay <em>trước chiến dịch</em></h2></div><p>Các hạng mục đã đầu tư, sẵn sàng khai thác cho mọi kênh.</p></div>
  {boxes([("Đã thực hiện","Quay chụp tại Việt Nam",["Bộ ảnh & video với 2 model tại Việt Nam.","Bản địa hoá hình ảnh cho truyền thông, quảng cáo và gian hàng."]),
          ("Đã xây dựng","4 fanpage",["1 fanpage branding Ninemila.","3 fanpage bán lẻ vệ tinh.","Mỗi page đã có hàng chục bài đăng, kết nối hình ảnh thương hiệu với bán lẻ."]),
          ("Trục truyền thông","Thông điệp xuyên suốt",["Giảm rụng – kích mọc · Phồng, mềm, mượt tóc.","Truyền thông toàn thương hiệu và hệ sản phẩm.","Dầu gội Men bia và tẩy tế bào chết là trọng tâm đợt KOC mở màn."])], three=True)}
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="label">03 · Hoạt động chủ lực</span><h2>Sáu hoạt động <em>chính</em></h2></div><p>65 KOC mở màn tháng 11–12. Megalive Võ Hà Linh tháng 01 là cao điểm. KOL và HASAKI tiếp tục trong tháng 01–02.</p></div>
  {activities}
</div></section>

<section class="sec">
  <div class="wrap"><div class="sec-head"><div><span class="label">04 · Ma trận IMC</span><h2>Phối hợp các kênh <em>theo thời gian</em></h2></div><p>15–19/11: chuẩn bị tư liệu, gửi sản phẩm và đồng bộ các kênh. Bấm tên kênh để mở kế hoạch chi tiết.</p></div></div>
  <div class="band"><div class="wrap">
    <div class="chips" id="matrixChips"><span class="label" style="margin-right:6px">Lọc nhóm</span>{chips}</div>
    <div class="tbl-wrap"><table class="matrix" id="matrix"><thead>{mhead}</thead><tbody>{rows}</tbody></table></div>
    <div class="legend"><span><i class="hot"></i>Hoạt động trọng tâm của giai đoạn</span><span><i></i>Hoạt động duy trì</span></div>
    <p class="note-line">Livestream TikTok và Shopee 4 giờ/ngày từ 15/12/2026 đến 28/02/2027. Lịch lên sóng từng KOL phân bổ trong tháng 01–02 theo booking.</p>
  </div></div>
</section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="label">05 · Ngân sách</span><h2>Dự toán <em>15/11/2026 – 28/02/2027</em></h2></div><p>Chi phí duy trì nhân theo thời gian thực hiện. Booking KOL, megalive và HASAKI tính một lần cho cả chiến dịch. Đơn vị: đồng.</p></div>
  <div class="totals">
    <div class="main"><span class="label">Tổng tạm tính các hạng mục đã có định mức</span><b>862.225.806 ₫</b><p>Chưa gồm booking 65 KOC, seeding Threads, giá trị sản phẩm và các khoản chưa có đơn giá.</p></div>
    <div><span class="label">A · Theo tháng × thời gian</span><b>462.225.806 ₫</b><p>Quảng cáo và vận hành livestream.</p></div>
    <div><span class="label">B · Tính một lần</span><b>400.000.000 ₫</b><p>Hai KOL, megalive và HASAKI.</p></div>
  </div>
  <h3 class="sub-h">A. Ngân sách theo tháng</h3>
  <p>Quảng cáo: đơn giá × (16/30 + 3 tháng). Livestream: đơn giá × (17/31 + 2 tháng). Tháng lẻ tính theo số ngày lịch, gồm ngày bắt đầu và kết thúc; làm tròn đến đồng.</p>
  {budget_a}
  <h3 class="sub-h">B. Ngân sách tính một lần cho cả chiến dịch</h3>
  <p>Không nhân các khoản dưới đây với số tháng.</p>
  {budget_b}
  <h3 class="sub-h">C. Các khoản chưa cộng vào tổng</h3>
  <p>Chỉ cộng khi có đơn giá và phạm vi chi phí; giá trị sản phẩm theo dõi riêng với ngân sách tiền mặt.</p>
  {budget_c}
  {callout("Đây là dự toán theo định mức, không phải chi phí quyết toán. Tổng cuối cùng cập nhật khi đủ phạm vi và đơn giá thực tế.")}
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><div><span class="label">06 · Mục tiêu</span><h2>Mục tiêu truyền thông <em>và khối lượng</em></h2></div><p>Chỉ số tiếp cận là mục tiêu kỳ vọng; tổng hợp giữa các tài khoản có thể trùng người xem.</p></div>
  <div class="kpis">
    <div><b>5–6 triệu</b><span>Lượt tiếp cận toàn chiến dịch</span><p>TikTok công ty + KOC + KOL; riêng công ty và KOC kỳ vọng hơn 3 triệu.</p></div>
    <div><b>500.000</b><span>Tiếp cận Threads / tháng</span><p>Kết hợp kênh brand và tuyến seeding.</p></div>
    <div><b>1.500 bài</b><span>Truyền thông đại lý tháng 12</span><p>50 đại lý, mỗi đại lý 30 bài.</p></div>
    <div><b>4 giờ/ngày</b><span>Livestream TikTok & Shopee</span><p>Từ 15/12/2026 đến 28/02/2027.</p></div>
  </div>
</div></section>
""" + FOOT
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)

if __name__ == "__main__":
    build_index()
    for p in INTERNAL: build_sub(p["slug"])
    print("Đã dựng:", "index.html,", ", ".join(p["slug"] + ".html" for p in INTERNAL))
