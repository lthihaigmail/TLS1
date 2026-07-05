# TSL — AI Business Diagnosis

**TSL Business Transformation Platform · From Evidence to Execution**

Bài chẩn đoán sức khỏe vận hành doanh nghiệp (10 phút) theo khung TSL — Team · System · Leadership. Khách nhận điểm trưởng thành (L1–L5), chỉ số tự do, 10 điểm nghẽn và lộ trình 90 ngày.

## Nội dung

| File | Vai trò |
|---|---|
| `index.html` | Landing page — bán hàng + thu lead |
| `diagnosis.html` | Bài chẩn đoán → báo cáo → PDF → xuất JSON |
| `proposal.html` | Sinh báo giá Mission 90 ngày (nội bộ) |

## Chạy

Trang tĩnh, không cần server. Mở `index.html` bằng trình duyệt, hoặc deploy lên GitHub Pages / Netlify.

- Đưa lên GitHub Pages: xem **GITHUB_SETUP.md**
- Deploy Netlify + thu lead tự động (Formspree): xem **README_DEPLOY.md**

## Cấu hình (trong `diagnosis.html`, đầu `<script>`)

```js
var CFG={ brand:"...", price:"499.000đ",
  payLink:"...",      // link thanh toán (Stripe/Momo/ZaloPay)
  calendly:"...",     // link đặt lịch
  formEndpoint:"",    // Formspree để thu lead tự động
  contact:"..." };
```

---

© TSL · Coach Emmy Lê Thị Hải — System Leadership Coach
