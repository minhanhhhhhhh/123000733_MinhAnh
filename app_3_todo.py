"""
BÀI TẬP: Morphology & Sentiment tiếng Việt với underthesea
===========================================================
"""

import re
from collections import Counter

import streamlit as st

# TODO 1: Import word_tokenize và sentiment từ thư viện underthesea
from underthesea import word_tokenize, sentiment


# ========= CẤU HÌNH TỪ VỰNG MẪU =========

PREFIX_MEANINGS = {
    "bất": "phủ định / không",
    "phi": "trái với / không theo",
    "tái": "lặp lại / làm lại",
    "siêu": "rất / vượt trội",
    "phụ": "thêm / phụ trợ",
}

POSITIVE_PHRASES = [
    "chạy nhanh", "chạy_nhanh", "chơi game mượt", "chơi_game_mượt",
    "màn hình đẹp", "màn_hình_đẹp", "đẹp quá", "rất đẹp",
    "đẹp_lung_linh", "siêu đẹp", "hài lòng", "rất hài lòng",
]

NEGATIVE_PHRASES = [
    "chạy chậm", "chạy_chậm", "lag", "giật lag", "giật_lag",
    "lâu kinh", "pin yếu", "pin_yếu", "tụt pin", "tụt_pin",
    "hao pin", "hao_pin", "tụt kinh khủng", "tụt_kinh_khủng",
    "máy nóng", "máy_hơi_nóng", "camera chụp xấu", "camera_chụp_xấu",
    "xấu quá",
]

EXAMPLE_TEXT = (
    "Máy chạy nhanh, chơi game mượt, màn hình đẹp nhưng pin tụt kinh khủng, "
    "sạc hoài luôn. Thỉnh thoảng hơi lag nữa. Mình khá hài lòng nhưng pin yếu quá."
)


# ========= HÀM TIỆN ÍCH =========

def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def simple_tokenize(text: str):
    """Tokenize đơn giản bằng split() — dùng làm baseline so sánh."""
    return text.split()


def underthesea_tokenize(text: str):
    """
    TODO 2: Dùng word_tokenize từ underthesea để tách từ tiếng Việt.
    """
    # ---- VIẾT CODE TẠI ĐÂY ----
    tokens_list = word_tokenize(text)
    tokens_text = word_tokenize(text, format="text")
    # ----------------------------
    return tokens_list, tokens_text


def safe_sentiment(text: str) -> str:
    """
    TODO 3: Gọi underthesea.sentiment(text) để lấy nhãn cảm xúc.
    """
    # ---- VIẾT CODE TẠI ĐÂY ----
    try:
        result = sentiment(text)
        if isinstance(result, (list, tuple)):
            return str(result[0]).lower()
        return str(result).lower()
    except Exception:
        return "neutral"
    # ----------------------------


def detect_prefixes(tokens, prefixes: dict) -> Counter:
    counts = Counter()
    for tok in tokens:
        t = re.sub(
            r"[^\w_áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệ"
            r"íìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữự"
            r"ýỳỷỹỵđ]",
            "",
            tok.lower(),
        )
        for pref in prefixes:
            if t.startswith(pref):
                counts[pref] += 1
    return counts


def detect_phrases(text: str, phrases: list) -> Counter:
    counts = Counter()
    for p in phrases:
        if not p:
            continue
        matches = re.findall(re.escape(p), text)
        if matches:
            counts[p] = len(matches)
    return counts


def overall_sentiment(pos_count: int, neg_count: int) -> str:
    if pos_count == 0 and neg_count == 0:
        return "KHÔNG RÕ / TRUNG TÍNH"
    if pos_count > neg_count:
        return "TÍCH CỰC"
    elif neg_count > pos_count:
        return "TIÊU CỰC"
    return "TRUNG TÍNH / LẪN LỘN"


# ========= GIAO DIỆN STREAMLIT =========

st.set_page_config(
    page_title="Morphology & Sentiment tiếng Việt (BÀI TẬP)",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 BÀI TẬP — Morphology & Sentiment tiếng Việt")

st.markdown(
    """
**Sinh viên cần hoàn thành 4 TODO trong file này:**

| TODO | Nội dung |
|------|----------|
| TODO 1 | Import `word_tokenize`, `sentiment` từ `underthesea` |
| TODO 2 | Viết hàm `underthesea_tokenize()` dùng `word_tokenize` |
| TODO 3 | Viết hàm `safe_sentiment()` dùng `sentiment` |
| TODO 4 | Hiển thị kết quả underthesea tokenize & sentiment trên giao diện |
"""
)

col_left, col_right = st.columns([1.1, 1.6])

with col_left:
    st.subheader("Nhập review / comment tiếng Việt")

    def _paste_example():
        st.session_state["input_text"] = EXAMPLE_TEXT

    st.button("Dán ví dụ gợi ý", on_click=_paste_example)

    text = st.text_area(
        "Văn bản",
        key="input_text",
        height=200,
        placeholder="Ví dụ: Máy chạy nhanh, chơi game mượt, màn hình đẹp nhưng pin tụt kinh khủng...",
    )

    analyze_btn = st.button("Phân tích Morphology & Sentiment")

with col_right:
    st.subheader("Kết quả phân tích")

    if not text.strip():
        st.info("Hãy nhập một đoạn văn rồi bấm **Phân tích**.")
    elif analyze_btn:
        norm_text = normalize_text(text)

        # ============================================================
        # PHẦN A — Tokenization: so sánh split() vs underthesea
        # ============================================================
        st.markdown("### 1️⃣ Tokenization — So sánh 2 cách")

        # --- Cách 1: split đơn giản ---
        tokens_simple = simple_tokenize(norm_text)
        st.markdown("**Cách 1 — split() đơn giản:**")
        st.code(" | ".join(tokens_simple))

        # --- Cách 2: underthesea ---
        st.markdown("**Cách 2 — underthesea `word_tokenize`:**")
        tokens_list, tokens_text = underthesea_tokenize(text)
        st.code(" | ".join(tokens_list))
        st.caption(f"Dạng text: `{tokens_text}`")

        # ============================================================
        # PHẦN B — Tiền tố
        # ============================================================
        st.markdown("### 2️⃣ Yếu tố Hán‑Việt dạng 'tiền tố nghĩa'")
        prefix_counts = detect_prefixes(tokens_list, PREFIX_MEANINGS)
        if prefix_counts:
            for pref, c in prefix_counts.items():
                meaning = PREFIX_MEANINGS.get(pref, "")
                st.write(f"- `{pref}`: **{c}** lần – nghĩa: *{meaning}*")
        else:
            st.write("_Chưa thấy tiền tố mẫu._")

        # ============================================================
        # PHẦN C — Sentiment: So sánh 2 phương pháp (theo kiểu ảnh)
        # ============================================================
        st.markdown("### 3️⃣ Sentiment — So sánh 2 phương pháp")

        # ====================== PHƯƠNG PHÁP 1: RULE-BASED ======================
        st.markdown("#### 🔸 **Phương pháp 1: Rule-based (Tự xây dựng)**")

        # Giữ nguyên toàn bộ 5 bước chi tiết của Rule-based như code gốc
        pos_counts = detect_phrases(norm_text, POSITIVE_PHRASES)
        neg_counts = detect_phrases(norm_text, NEGATIVE_PHRASES)
        pos_total = sum(pos_counts.values())
        neg_total = sum(neg_counts.values())
        total_phrases = pos_total + neg_total

        # Bước 1
        st.markdown("##### Bước 1 — Phát hiện cụm cảm xúc")
        col_pos, col_neg = st.columns(2)
        with col_pos:
            st.markdown("🟢 **Cụm tích cực**")
            if pos_counts:
                for p, c in pos_counts.items():
                    st.write(f"- `{p}` × {c}")
            else:
                st.write("_Không tìm thấy_")
        with col_neg:
            st.markdown("🔴 **Cụm tiêu cực**")
            if neg_counts:
                for p, c in neg_counts.items():
                    st.write(f"- `{p}` × {c}")
            else:
                st.write("_Không tìm thấy_")

        # Bước 2, 3, 4, 5 giữ nguyên
        st.markdown("##### Bước 2 — Thống kê số lượng")
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        stat_col1.metric("Σ Tích cực (P)", pos_total)
        stat_col2.metric("Σ Tiêu cực (N)", neg_total)
        stat_col3.metric("Tổng cụm", total_phrases)

        st.markdown("##### Bước 3 — Tính Sentiment Score")
        if total_phrases > 0:
            score = (pos_total - neg_total) / total_phrases
            st.latex(
                r"\text{Score} = \frac{P - N}{P + N} = "
                rf"\frac{{{pos_total} - {neg_total}}}{{{pos_total} + {neg_total}}} = "
                rf"{score:+.2f}"
            )
        else:
            score = 0.0
            st.latex(r"\text{Score} = 0")

        st.markdown("##### Bước 4 — Quy tắc phân loại")
        st.markdown(r"""
| Điều kiện | Nhãn |
|---|---|
| $P = 0$ và $N = 0$ | KHÔNG RÕ / TRUNG TÍNH |
| $P > N$ | TÍCH CỰC |
| $N > P$ | TIÊU CỰC |
| $P = N$ | TRUNG TÍNH / LẪN LỘN |
""")

        label = overall_sentiment(pos_total, neg_total)
        st.markdown("##### Bước 5 — Kết luận Rule-based")
        if "TÍCH CỰC" in label:
            st.success(f"**{label}** (P: {pos_total} - N: {neg_total})")
        elif "TIÊU CỰC" in label:
            st.error(f"**{label}** (P: {pos_total} - N: {neg_total})")
        else:
            st.warning(f"**{label}** (P: {pos_total} - N: {neg_total})")

        # ====================== PHƯƠNG PHÁP 2: UNDERTHESEA ======================
        st.markdown("---")
        st.markdown("#### 🔹 **Phương pháp 2: Underthesea (Thư viện chuyên dụng)**")

        # Tokenization của underthesea (đã hiển thị ở trên, nhưng có thể nhắc lại nếu cần)
        st.markdown("**Tokenization (underthesea word_tokenize):**")
        st.code(" | ".join(tokens_list))

        # Sentiment của underthesea
        senti_label = safe_sentiment(text)
        st.markdown("**Kết quả Sentiment từ underthesea**")
        st.metric("Nhãn cảm xúc", senti_label.upper())

        # ====================== SO SÁNH ======================
        st.markdown("---")
        st.markdown("#### 📊 So sánh hai phương pháp")
        st.info(f"**Rule-based**: {label}  |  **Underthesea**: **{senti_label.upper()}**")

    else:
        st.info("Nhập văn bản và bấm **Phân tích** để xem kết quả.")