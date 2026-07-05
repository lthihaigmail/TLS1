# TSL AI Diagnosis — BỘ DEPLOY (host lên web miễn phí)
### 3 file HTML, không cần server, kéo-thả là có link gửi khách.

---

## Trong thư mục này

| File | Vai trò | Ai xem |
|---|---|---|
| **index.html** | Trang bán hàng (landing) + form thu lead | Khách hàng |
| **diagnosis.html** | Bài chẩn đoán → báo cáo → PDF → xuất JSON | Khách hàng |
| **proposal.html** | Sinh báo giá Mission từ JSON (công cụ nội bộ) | Emmy |

Luồng: **index → (đăng ký) → diagnosis → xuất JSON → proposal (báo giá) + nạp vào Mission Ledger.**

---

## CÁCH 1 · Netlify Drop (nhanh nhất, 2 phút, miễn phí)

1. Vào **https://app.netlify.com/drop**
2. **Kéo cả thư mục `TSL_AI_Diagnosis_Site`** (hoặc file `TSL_AI_Diagnosis_Site.zip`) thả vào trang.
3. Netlify tạo ngay link dạng `https://ten-ngau.netlify.app` → đây là link gửi khách.
4. Muốn tên đẹp: Site settings → Change site name (vd `chandoan-tsl`).
5. Muốn tên miền riêng (vd `chandoan.coachemmy.vn`): Domain settings → Add custom domain.

> Cập nhật sau này: chỉ cần kéo-thả lại thư mục mới đè lên.

## CÁCH 2 · GitHub Pages (miễn phí, ổn định lâu dài)

1. Tạo repo GitHub mới → upload 3 file (index/diagnosis/proposal).
2. Settings → Pages → Source: `main` branch, thư mục `/root` → Save.
3. Link: `https://<tài-khoản>.github.io/<repo>/`.

## CÁCH 3 · Gửi trực tiếp (không host)

Gửi thẳng file `diagnosis.html` qua email/Zalo — khách mở bằng trình duyệt là chạy. Không có form thu lead, nhưng chẩn đoán + PDF + xuất JSON vẫn hoạt động đầy đủ.

---

## TRƯỚC KHI DEPLOY — chỉnh 2 chỗ (5 phút)

**1. `diagnosis.html`** — mở bằng Notepad/editor, tìm dòng đầu `<script>`:
```js
var CFG={ brand:"TSL · Coach Emmy", price:"499.000đ", calendly:"#", contact:"lthihai@gmail.com" };
```
- `calendly`: dán link đặt lịch của bạn (Calendly / link Zalo / số điện thoại).
- `brand`, `price`, `contact`: chỉnh theo ý.

**2. `index.html`** — tìm `var CFG={ email:"lthihai@gmail.com" }` → đổi email nhận lead nếu cần.

---

## THU LEAD — mặc định mailto, bật TỰ ĐỘNG chỉ với 1 dòng

Mặc định: form thu lead bằng **mailto** (mở email điền sẵn) + lưu tạm ở trình duyệt. Đủ để bắt đầu ngay.

**Bật thu lead TỰ ĐỘNG (khuyến nghị, miễn phí, 5 phút) — Formspree:**
1. Vào **https://formspree.io** → đăng ký → tạo form mới → copy endpoint dạng `https://formspree.io/f/abcdwxyz`.
2. Mở `index.html`, tìm dòng:
   ```js
   var CFG={ email:"lthihai@gmail.com", formEndpoint:"" };
   ```
3. Dán endpoint vào: `formEndpoint:"https://formspree.io/f/abcdwxyz"`.
4. Xong. Từ giờ khách bấm "Gửi đăng ký" → lead **tự về email** bạn, không cần khách làm gì thêm. (Nếu endpoint lỗi, code tự quay về mailto.)

**Thay bằng Tally/Google Forms** (nếu thích form riêng): tạo form → lấy link → thay nút "Gửi đăng ký" bằng link đó. Đánh đổi: mất giao diện form đẹp hiện tại.

*(Không bắt buộc lúc đầu — bán trước, tự động sau. Nhưng Formspree chỉ mất 5 phút và đáng làm ngay.)*

---

## SAU KHI KHÁCH CHẨN ĐOÁN

1. Khách bấm **Xuất dữ liệu (JSON)** ở c