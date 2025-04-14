
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_excel("assetv4.xlsx", header=1)
    df = df[df.columns.dropna()]
    df = df.dropna(subset=["Asset Description"])
    return df

df = load_data()
descriptions = df["Asset Description"].astype(str).tolist()

# إنشاء تمثيل رقمي باستخدام TF-IDF
vectorizer = TfidfVectorizer().fit(descriptions)
description_vectors = vectorizer.transform(descriptions)

# واجهة المستخدم
st.set_page_config(page_title="تصنيف الأصول - ذكاء صناعي محلي", layout="centered", page_icon="🧠")
st.title("🧠 نموذج ذكاء محلي لتصنيف الأصول")

user_input = st.text_input("📝 أدخل اسم الأصل (مثال: طابعة، حاسب، مكيف):")

if user_input:
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, description_vectors).flatten()
    top_indices = similarities.argsort()[-3:][::-1]

    st.markdown("### 🔍 أعلى 3 تطابقات:")
    for i, idx in enumerate(top_indices):
        score = round(similarities[idx]*100, 2)
        match_desc = df.iloc[idx]["Asset Description"]
        st.markdown(f"**{i+1}.** `{match_desc}` — تطابق بنسبة: **{score}%**")

        # عرض التصنيف المحاسبي
        with st.expander("📊 التصنيف المحاسبي"):
            fields = [
                "Level 1 FA Module Code", "Level 1 FA Module - Arabic Description", "Level 1 FA Module - English Description",
                "Level 2 FA Module Code", "Level 2 FA Module - Arabic Description", "Level 2 FA Module - English Description",
                "Level 3 FA Module Code", "Level 3 FA Module - Arabic Description", "Level 3 FA Module - English Description",
                "accounting group Code", "accounting group Arabic Description", "accounting group English Description",
                "Asset Code For Accounting Purpose"
            ]
            for field in fields:
                st.write(f"**{field}**:", df.iloc[idx].get(field, ""))
