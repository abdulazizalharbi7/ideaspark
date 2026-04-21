from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatGroq(
    api_key="YOUR_KEY_HERE"
    model_name="llama-3.3-70b-versatile"
)

def smart_generate(interest: str, major: str, level: str, goal: str) -> str:
    messages = [
        SystemMessage(content="""أنت مساعد متخصص في اقتراح أفكار مشاريع برمجية.
        مهمتك: تحليل معلومات الطالب وتقديم 3 أفكار مشاريع مخصصة ومناسبة تماماً له.
        كل فكرة تحتوي: الاسم، الوصف، التقنيات، خطوات البدء، وسبب مناسبتها له."""),
        HumanMessage(content=f"""
        الطالب: {major}
        المستوى: {level}
        الاهتمام: {interest}
        الهدف: {goal}
        
        اقترح 3 أفكار مشاريع مخصصة له بالعربي.
        """)
    ]
    response = llm.invoke(messages)
    return response.content

# اختبار
result = smart_generate("ألعاب", "هندسة برمجيات", "مبتدئ", "سي في")
print(result)