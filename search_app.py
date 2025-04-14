
import streamlit as st
from openai import OpenAI
from openai import OpenAIError

# إعداد واجهة Streamlit
st.set_page_config(page_title="تصنيف الأصول باستخدام GPT", layout="centered", page_icon="🤖")
st.title("🤖 نموذج ذكاء اصطناعي لتصنيف الأصول حسب الدليل الحكومي")

# إدخال مفتاح API من المستخدم
api_key = st.text_input("🔑 أدخل مفتاح OpenAI API الخاص بك:", type="password")

# اختيار النموذج
model = st.selectbox("🧠 اختر نموذج الذكاء الاصطناعي:", ["gpt-3.5-turbo", "gpt-4"])

# إدخال وصف الأصل
asset_name = st.text_input("📥 أدخل اسم الأصل (مثال: طابعة كانون، جهاز بصمة، مكيف شباك):")

def classify_asset_with_gpt(asset_name, key, model_name):
    client = OpenAI(api_key=key)

    prompt = f"""أنت مساعد ذكي لتصنيف الأصول حسب دليل الأصول الحكومي السعودي.

مهمتك:
عند إعطائك وصفًا مختصرًا لأصل (مثل: "طابعة كانون"، "جهاز بصمة"، "مكيف شباك")، قم بتحليل الوصف واقتراح التصنيف المحاسبي المناسب من حيث:
- رمز التصنيف المحاسبي (مستوى 1، 2، 3)
- اسم التصنيف المحاسبي بالعربي والإنجليزي لكل مستوى
- رمز المجموعة المحاسبية + وصفها بالعربي والإنجليزي
- رمز الأصل لغرض المحاسبة

📌 لا تخترع تصنيفات، اعتمد فقط على تصنيفات الأصول الحكومية المعروفة.

صنف الأصل التالي بدقة:
"{asset_name}"
"""

    chat = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return chat.choices[0].message.content

if api_key and asset_name:
    with st.spinner("🔍 جاري تصنيف الأصل باستخدام GPT..."):
        try:
            result = classify_asset_with_gpt(asset_name, api_key, model)
            st.success("✅ تم التصنيف بنجاح:")
            st.markdown(result)
        except OpenAIError as e:
            st.error("❌ حدث خطأ أثناء الاتصال بـ GPT:\n" + str(e))
elif asset_name and not api_key:
    st.warning("⚠️ الرجاء إدخال مفتاح OpenAI API أولاً.")
