
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ الإعدادات
st.set_page_config(page_title="نموذج ذكي لتصنيف الأصول", layout="centered", page_icon="🧠")
st.title("🤖 نموذج ذكاء اصطناعي متقدم لتصنيف الأصول")

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_excel("assetv4.xlsx", header=1)
    df = df[df.columns.dropna()]
    df = df.dropna(subset=["Asset Description"])
    return df

df = load_data()
descriptions = df["Asset Description"].astype(str).tolist()

# تحميل نموذج الذكاء الاصطناعي
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-MiniLM-L6-v2')

model = load_model()
description_embeddings = model.encode(descriptions)

# إدخال المستخدم
user_input = st.text_input("📝 أدخل وصف الأصل (مثال: طابعة، مكيف، جهاز بصمة):")

if user_input:
    with st.spinner("🔍 جاري تحليل الوصف..."):
        user_embedding = model.encode([user_input])
        similarities = cosine_similarity(user_embedding, description_embeddings).flatten()
        top_indices = similarities.argsort()[-3:][::-1]

        st.markdown("### ✅ أفضل 3 تطابقات:")

        for i, idx in enumerate(top_indices):
            score = round(similarities[idx] * 100, 2)
            desc = df.iloc[idx]["Asset Description"]
            st.markdown(f"**{i+1}.** `{desc}` — تطابق: **{score}%**")

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
