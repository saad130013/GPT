
import streamlit as st
import openai

# إعداد صفحة Streamlit
st.set_page_config(page_title="تصنيف الأصول باستخدام GPT", layout="centered", page_icon="🧠")
st.title("🤖 تصنيف ذكي للأصول حسب دليل التصنيف الحكومي")

# إدخال مفتاح API
api_key = st.text_input("🔐 أدخل مفتاح OpenAI API:", type="password", help="لن يتم حفظ المفتاح. يُستخدم فقط أثناء الجلسة.")

# إدخال وصف الأصل
asset_desc = st.text_input("📝 أدخل وصف الأصل (مثل: طابعة كانون، حاسب مكتبي، مكيف شباك):")

# دالة إرسال الطلب إلى GPT
def classify_asset_with_gpt(asset_name, key):
    prompt = f"""أنت مساعد ذكي لتصنيف الأصول حسب دليل الأصول الحكومي السعودي.

مهمتك:
عند إعطائك وصفًا مختصرًا لأصل (مثل: "طابعة كانون"، "جهاز بصمة"، "مكيف شباك")، قم بتحليل الوصف واقتراح التصنيف المحاسبي المناسب من حيث:
- رمز التصنيف المحاسبي (مستوى 1، 2، 3)
- اسم التصنيف المحاسبي بالعربي والإنجليزي لكل مستوى
- رمز المجموعة المحاسبية + وصفها
- رمز الأصل لغرض المحاسبة

📌 لا تخترع تصنيفات، اعتمد فقط على تصنيفات الأصول الحكومية المعروفة.

صنف الأصل التالي بدقة:
"{asset_name}"
"""
    openai.api_key = key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# تنفيذ العملية
if api_key and asset_desc:
    with st.spinner("🔍 جاري تصنيف الأصل باستخدام GPT..."):
        try:
            result = classify_asset_with_gpt(asset_desc, api_key)
            st.success("✅ تم التصنيف بنجاح:")
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ خطأ أثناء الاتصال بـ GPT:
{e}")
elif asset_desc and not api_key:
    st.warning("⚠️ الرجاء إدخال مفتاح OpenAI API أولاً.")
