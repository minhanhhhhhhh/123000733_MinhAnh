"""
BÀI TẬP: Morphology & Sentiment tiếng Việt với underthesea
===========================================================
Sinh viên cần hoàn thành các phần đánh dấu TODO bên dưới.

Yêu cầu:
  1) Dùng underthesea.word_tokenize thay cho simple_tokenize (split đơn giản).
  2) Dùng underthesea.sentiment thay cho rule-based sentiment.
  3) So sánh kết quả giữa 2 cách (rule-based vs underthesea).

Cài đặt: pip install underthesea streamlit
Chạy:    streamlit run app_3_todo.py
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

    Gợi ý:
      - word_tokenize(text) trả về list các token, ví dụ: ['màn_hình', 'đẹp', 'quá']
      - word_tokenize(text, format="text") trả về chuỗi: 'màn_hình đẹp quá'

    Yêu cầu: Trả về tuple (tokens_list, tokens_text)
      - tokens_list: list token (dạng list)
      - tokens_text: chuỗi token (dạng format="text")
    """
    # ---- VIẾT CODE TẠI ĐÂY ----
    tokens_list = word_tokenize(text)
    tokens_text = word_tokenize(text, format="text")
    # ----------------------------
    return tokens_list, tokens_text


def safe_sentiment(text: str) -> str:
    """
    TODO 3: Gọi underthesea.sentiment(text) để lấy nhãn cảm xúc.

    Gợi ý:
      - sentiment(text) có thể trả về 'positive', 'negative', 'neutral'
        hoặc list/tuple tuỳ phiên bản.
      - Cần xử lý trường hợp trả về list/tuple: lấy phần tử đầu tiên.
      - Bọc trong try/except để tránh crash nếu chưa cài model.

    Yêu cầu: Trả về string nhãn sentiment, ví dụ: 'positive', 'negative'.
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
    st.subheader("Kết quả")

    if not text.strip():
        st.info("Hãy nhập một đoạn văn rồi bấm **Phân tích**.")
    elif analyze_btn:
        norm_text = normalize_text(text)

        # ============================================================
        # PHẦN A — Tokenization: so sánh split() vs underthesea
        # ============================================================
        st.markdown("### 1️⃣ Tokenization — So sánh 2 cách")

        # --- Cách 1: split đơn giản (đã có sẵn) ---
        tokens_simple = simple_tokenize(norm_text)
        st.markdown("**Cách 1 — split() đơn giản:**")
        st.code(" | ".join(tokens_simple))

        # --- Cách 2: underthesea word_tokenize ---
        st.markdown("**Cách 2 — underthesea `word_tokenize`:**")

        # TODO 4a: Gọi underthesea_tokenize(text) và hiển thị kết quả.
        tokens_list, tokens_text = underthesea_tokenize(text)
        st.code(" | ".join(tokens_list))
        st.caption(f"Dạng text: `{tokens_text}`")

        # ============================================================
        # PHẦN B — Sentiment Analysis
        # ============================================================
        st.markdown("### 2️⃣ Sentiment Analysis — So sánh 2 cách")

        # --- Cách 1: Rule-based (giữ nguyên) ---
        pos_count = sum(detect_phrases(norm_text, POSITIVE_PHRASES).values())
        neg_count = sum(detect_phrases(norm_text, NEGATIVE_PHRASES).values())
        rule_sentiment = overall_sentiment(pos_count, neg_count)

        st.markdown("**Cách 1 — Rule-based (từ vựng):**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Positive phrases", pos_count)
        col2.metric("Negative phrases", neg_count)
        col3.metric("Kết luận", rule_sentiment)

        # --- Cách 2: underthesea sentiment ---
        st.markdown("**Cách 2 — underthesea `sentiment`:**")
        underthesea_label = safe_sentiment(text)

        st.metric("Kết quả underthesea", underthesea_label.upper())

        # So sánh
        st.markdown("**So sánh hai phương pháp:**")
        st.info(f"Rule-based: **{rule_sentiment}**  •  underthesea: **{underthesea_label.upper()}**")

        # Bonus: Prefix detection
        st.markdown("### 3️⃣ Phát hiện tiền tố (Morphology)")
        prefixes = detect_prefixes(tokens_list, PREFIX_MEANINGS)
        if prefixes:
            for pref, cnt in prefixes.items():
                st.write(f"• **{pref}** ({PREFIX_MEANINGS[pref]}): xuất hiện **{cnt}** lần")
        else:
            st.write("Không phát hiện tiền tố đặc biệt.")