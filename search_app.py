
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
import io

# إعداد الصفحة
st.set_page_config(page_title="Asset Classifier with PDF Export", layout="centered", page_icon="🧠")
st.title("🧠 Asset Classification with AI + PDF Export")

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
user_input = st.text_input("📝 Enter asset description (e.g. printer, AC, scanner):")

if user_input:
    user_embedding = model.encode([user_input])
    similarities = cosine_similarity(user_embedding, description_embeddings).flatten()
    top_indices = similarities.argsort()[-3:][::-1]

    st.markdown("### ✅ Top 3 matches:")

    for i, idx in enumerate(top_indices):
        score = round(similarities[idx] * 100, 2)
        desc = df.iloc[idx]["Asset Description"]
        st.markdown(f"**{i+1}.** `{desc}` — Match: **{score}%**")

        with st.expander("📊 Classification Details"):
            selected_data = df.iloc[idx]
            fields = {
                "Asset Description": desc,
                "Level 1 FA Module Code": selected_data.get("Level 1 FA Module Code", ""),
                "Level 1 FA Module - English Description": selected_data.get("Level 1 FA Module - English Description", ""),
                "Level 2 FA Module Code": selected_data.get("Level 2 FA Module Code", ""),
                "Level 2 FA Module - English Description": selected_data.get("Level 2 FA Module - English Description", ""),
                "Level 3 FA Module Code": selected_data.get("Level 3 FA Module Code", ""),
                "Level 3 FA Module - English Description": selected_data.get("Level 3 FA Module - English Description", ""),
                "Accounting Group Code": selected_data.get("accounting group Code", ""),
                "Accounting Group Description": selected_data.get("accounting group English Description", ""),
                "Asset Code For Accounting Purpose": selected_data.get("Asset Code For Accounting Purpose", "")
            }

            for k, v in fields.items():
                st.write(f"**{k}**: {v}")

            # زر تصدير PDF
            if st.button(f"📥 Export Match #{i+1} to PDF", key=f"pdf_button_{i}"):
                class PDF(FPDF):
                    def header(self):
                        self.set_font("Arial", "B", 14)
                        self.cell(0, 10, "Asset Classification Report", ln=True, align="C")

                    def footer(self):
                        self.set_y(-15)
                        self.set_font("Arial", "I", 8)
                        self.cell(0, 10, f"Page {self.page_no()}", align="C")

                    def add_data(self, data_dict):
                        self.set_font("Arial", "", 12)
                        for k, v in data_dict.items():
                            self.cell(60, 10, k + ":", border=0)
                            self.multi_cell(0, 10, str(v), border=0)

                pdf = PDF()
                pdf.add_page()
                pdf.add_data(fields)

                pdf_buffer = io.BytesIO()
                pdf.output(pdf_buffer)

                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_buffer.getvalue(),
                    file_name="asset_classification.pdf",
                    mime="application/pdf"
                )
