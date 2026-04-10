import streamlit as st
import requests

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
        background-color: #ffffff;
    }
    
  h1 {
    font-family: 'Fredoka One', cursive !important;
    color: #ff6b9d !important;
    font-size: 2rem !important;
}

div[data-testid="stCaptionContainer"] p {
    color: #000000 !important;
}
    
    .stChatMessage {
        font-family: 'Nunito', sans-serif !important;
        font-size: 1.1rem !important;
    }
    
    .stChatInputContainer textarea {
        font-family: 'Nunito', sans-serif !important;
        border-radius: 20px !important;
        background-color: #f0f0f0 !important;
    }

    section[data-testid="stChatMessageContainer"] {
        background-color: #ffffff;
    }

    [data-testid="stChatMessageContent"] {
        background-color: #f9f0ff !important;
        border-radius: 18px !important;
        padding: 10px 15px !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    [data-testid="stChatMessageContent"] p {
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        min-height: 40px !important;
        color: #000000 !important;
    }

    .stApp {
        background-image: 
            linear-gradient(rgba(255,192,203,0.15) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,192,203,0.15) 1px, transparent 1px);
        background-size: 30px 30px;
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

def get_bot_response(conversation_history):
    system_prompt = """You are a fun, witty chatbot inspired by the viral "you the birthday" trend from Twitter and TikTok. 

Your personality is like a best friend — real, warm, a little sassy, but genuinely caring.

Here is how you respond every single time:
1. First, respond to what the person said with genuine emotion. If it's sad news, say something empathetic like "Oh no, I'm so sorry to hear that" or "That's really tough, I hear you." If it's good news, match their energy like "Okay that's amazing!" or "Yesss we are celebrating!"
2. Then at the end of your response, ALWAYS finish with a "you the birthday" style joke that matches their situation. The joke should be clever and relate to what they actually said.

Examples of the birthday joke format:
- Someone sad about a breakup: "you the canceled birthday party"
- Someone who got promoted: "it's giving you the birthday upgrade"  
- Someone in a car crash: "you the birthday that got crashed"
- Someone fired: "you the birthday bill nobody wanted to pay"
- Someone excited about getting engaged: "you the birthday wish that came true"
- Someone lonely: "you the birthday nobody showed up to"
- Someone doing too much: "you the whole birthday parade"
- Someone left out: "you the birthday card that got lost in the mail"
- Someone explaining too much: "you the birthday planner"
- Someone late: "you the belated birthday"

The joke always connects to their actual situation. Be creative. Keep the whole response short — 2 to 3 sentences max. Always end with the birthday joke on the same line as your empathy or excitement, connected naturally."""

    api_key = st.secrets["GROQ_API_KEY"]

    messages = [{"role": "system", "content": system_prompt}]
    for msg in conversation_history:
        if msg["role"] in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "max_tokens": 200
        }
    )

    data = response.json()

    if "choices" not in data:
        st.error(f"API Error: {data}")
        return "Something went wrong, try again."

    return data["choices"][0]["message"]["content"]

st.title("You the Birthday Bot 🎂")
st.caption("Girl you know it's me Osob, what's the problem?")

if "messages" not in st.session_state:
    st.session_state.messages = []
    opening = "Girl, what's the problem? Tell me everything. 👀"
    st.session_state.messages.append({"role": "assistant", "content": opening})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Spill it...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    api_history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if m["role"] in ["user", "assistant"]
    ]

    with st.spinner("..."):
        reply = get_bot_response(api_history)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
