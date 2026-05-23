import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="BrightHome Support Chat", page_icon="💡", layout="centered")

st.markdown("""
<style>
    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are Aria, a friendly customer service assistant 
for BrightHome — a smart home products company. You help customers with 
product information, orders, returns, and technical support. 
Always be warm, concise and helpful."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

st.markdown("## 💡 BrightHome Support Chat")
st.markdown("*AI-powered assistant · Available 24/7*")
st.divider()

with st.sidebar:
    st.markdown("### Settings")
    api_key = st.text_input("OpenAI API Key", type="password",
                            value=os.getenv("OPENAI_API_KEY", ""),
                            help="Get your key at platform.openai.com")
    st.divider()
    if st.button("Clear conversation"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.display_messages = []
        st.rerun()
    st.markdown("**Built with:** Python + OpenAI + Streamlit")

if not st.session_state.display_messages:
    with st.chat_message("assistant"):
        st.markdown("Hi! I'm **Aria**, your BrightHome assistant. How can I help you today?")

for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything about BrightHome..."):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
        st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.display_messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Aria is typing..."):
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=500,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.display_messages.append({"role": "assistant", "content": reply})
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
                