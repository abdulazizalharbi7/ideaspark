import streamlit as st
from supabase import create_client
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatGroq(
    api_key=st.secrets["GROQ_API_KEY"],
    model_name="llama-3.3-70b-versatile"
)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def smart_generate(interest, major, level, goal, time_available, team_size, project_type, tech_str, difficulty):
    messages = [
        SystemMessage(content="أنت مساعد متخصص في اقتراح أفكار مشاريع برمجية مخصصة. حلل معلومات الطالب وقدم 3 أفكار مناسبة مع سبب مناسبة كل فكرة."),
        HumanMessage(content=f"""
        التخصص: {major} | المستوى: {level} | الاهتمام: {interest}
        الوقت: {time_available} | الهدف: {goal} | العمل: {team_size}
        النوع: {project_type} | التقنيات: {tech_str} | الصعوبة: {difficulty}
        اقترح 3 أفكار مشاريع بالعربي مع: الاسم، الوصف، التقنيات، خطوات البدء، سبب المناسبة.
        """)
    ]
    return llm.invoke(messages).content

st.set_page_config(page_title="IdeaSpark AI", page_icon="💡", layout="centered")

st.markdown("""
<style>
    .main { background-color: #0a0a0a; }
    .block-container { padding: 40px 20px; max-width: 600px; }
    label { color: #8B6914 !important; font-size: 13px !important; }
    div[data-baseweb="select"] {
        background-color: #111 !important;
        border: 0.5px solid #2a2a2a !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * { color: #D4A853 !important; }
    .stTextInput input {
        background-color: #111 !important;
        border: 0.5px solid #2a2a2a !important;
        color: #D4A853 !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        background: #D4A853;
        color: #0a0a0a;
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='color:#D4A853; margin-bottom:4px;'>💡 IdeaSpark</h3>", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None

if st.session_state.user is None:
    st.markdown("<p style='color:#8B6914; font-size:13px;'>سجّل دخول للبدء</p>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["دخول", "حساب جديد"])
    with tab1:
        email = st.text_input("الإيميل", key="login_email")
        password = st.text_input("كلمة السر", type="password", key="login_pass")
        if st.button("دخول"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except:
                st.error("إيميل أو كلمة سر غلط")
    with tab2:
        email = st.text_input("الإيميل", key="reg_email")
        password = st.text_input("كلمة السر", type="password", key="reg_pass")
        if st.button("إنشاء حساب"):
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.success("تم إنشاء الحساب! سجّل دخول الحين")
            except:
                st.error("مشكلة في إنشاء الحساب")
else:
    st.markdown(f"<p style='color:#3a3020; font-size:12px;'>مرحباً {st.session_state.user.email}</p>", unsafe_allow_html=True)
    if st.button("خروج", key="logout"):
        st.session_state.user = None
        st.rerun()

    major = st.selectbox("التخصص", ["هندسة برمجيات", "علوم حاسب", "نظم معلومات", "ذكاء اصطناعي", "شبكات", "أخرى"])
    level = st.selectbox("المستوى", ["مبتدئ", "متوسط", "متقدم"])
    interest = st.text_input("اهتمامك", placeholder="ألعاب، صحة، تعليم...")

    col1, col2 = st.columns(2)
    with col1:
        time_available = st.selectbox("الوقت المتاح", ["أسبوع", "شهر", "3 أشهر", "6 أشهر"])
        goal = st.selectbox("الهدف", ["سي في", "تعلم", "مشروع تخرج", "مشروع تجاري", "مسابقة"])
    with col2:
        team_size = st.selectbox("فريق أو فردي؟", ["فردي", "فريق صغير 2-3", "فريق كبير 4+"])
        project_type = st.selectbox("نوع المشروع", ["ويب", "موبايل", "ذكاء اصطناعي", "داتا", "أي نوع"])

    tech_pref = st.multiselect("تقنيات تفضلها", ["Python", "Java", "JavaScript", "React", "Flutter", "SQL", "Machine Learning", "API"], default=["Python"])
    difficulty = st.select_slider("مستوى الصعوبة", options=["سهل جداً", "سهل", "متوسط", "صعب", "تحدي كبير"], value="متوسط")

    if st.button("ولّد أفكاري"):
        if not interest:
            st.warning("اكتب اهتمامك أولاً")
        else:
            with st.spinner("يفكر..."):
                tech_str = "، ".join(tech_pref) if tech_pref else "أي تقنية"
                result = smart_generate(interest, major, level, goal, time_available, team_size, project_type, tech_str, difficulty)
                st.session_state.last_result = result

                try:
                    supabase.table("ideas").insert({
                        "major": major,
                        "level": level,
                        "interest": interest,
                        "goal": goal,
                        "result": result,
                        "user_email": st.session_state.user.email
                    }).execute()
                except:
                    pass

                st.markdown(f"""
                <div style='margin-top:24px; padding:20px; background:#111;
                border-radius:10px; border:0.5px solid #2a2a2a;
                color:#D4A853; line-height:1.9; font-size:14px;'>
                {result}
                </div>
                """, unsafe_allow_html=True)

    if st.session_state.get("last_result"):
        st.download_button(
            label="📄 حمّل الأفكار",
            data=st.session_state.last_result.encode('utf-8'),
            file_name="ideaspark_ideas.txt",
            mime="text/plain"
        )

    if st.button("📂 أفكاري السابقة"):
        try:
            data = supabase.table("ideas").select("*").eq("user_email", st.session_state.user.email).order("created_at", desc=True).limit(5).execute()
            if data.data:
                for idea in data.data:
                    st.markdown(f"""
                    <div style='padding:14px; background:#111; border-radius:8px;
                    border:0.5px solid #2a2a2a; color:#8B6914; margin-bottom:8px; font-size:13px;'>
                    <b style='color:#D4A853;'>{idea['interest']}</b> — {idea['major']} — {idea['goal']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ما فيه أفكار محفوظة بعد")
        except:
            st.error("مشكلة في الاتصال")

st.markdown("<p style='color:#2a2a2a; font-size:11px; text-align:center; margin-top:32px;'>IdeaSpark AI</p>", unsafe_allow_html=True)