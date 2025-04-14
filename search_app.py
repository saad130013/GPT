
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="🔍 Smart Asset Lookup", layout="centered", page_icon="🔍")
st.title("🔍 Smart Asset Description Autocomplete")

# تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_excel("assetv4.xlsx", header=1)
    df = df[df.columns.dropna()]
    df = df.dropna(subset=["Asset Description"])
    return df

df = load_data()
descriptions = df["Asset Description"].astype(str).tolist()

# إنشاء TF-IDF للنصوص
@st.cache_resource
def create_vectorizer():
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(descriptions)
    return vectorizer, vectors

vectorizer, description_vectors = create_vectorizer()

# إدخال المستخدم مع اقتراحات
user_input = st.text_input("✍️ Start typing asset description:")

if user_input:
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, description_vectors).flatten()
    top_indices = similarities.argsort()[-5:][::-1]

    suggestions = [descriptions[i] for i in top_indices]
    selected_suggestion = st.selectbox("💡 Suggestions:", suggestions)

    if selected_suggestion:
        st.markdown("### 🧾 Selected Description:")
        st.markdown(f"**{selected_suggestion}**")

        selected_row = df[df["Asset Description"] == selected_suggestion].iloc[0]

        with st.expander("📊 Classification Details"):
            fields = [
                "Level 1 FA Module Code", "Level 1 FA Module - English Description",
                "Level 2 FA Module Code", "Level 2 FA Module - English Description",
                "Level 3 FA Module Code", "Level 3 FA Module - English Description",
                "accounting group Code", "accounting group English Description",
                "Asset Code For Accounting Purpose"
            ]
            
for field in fields:
    st.write(f"**{field}**:", selected_row.get(field, ""))

# زر تصدير PDF
import io
from fpdf import FPDF

if st.button("📥 Export to PDF"):
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

    export_data = {field: selected_row.get(field, "") for field in fields}
    export_data["Asset Description"] = selected_suggestion

    pdf = PDF()
    pdf.add_page()
    pdf.add_data(export_data)

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)

    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_buffer.getvalue(),
        file_name="asset_classification.pdf",
        mime="application/pdf"
    )

                st.write(f"**{field}**:", selected_row.get(field, ""))
