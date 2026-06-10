import streamlit as st
import requests
import tempfile
import os
from audio_recorder_streamlit import audio_recorder

st.set_page_config(
    page_title="KTB Client Zero Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 KTB Client Zero Agent")
st.markdown("Ask me anything about the 5 KTB Client Zero teams.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

language = st.selectbox(
    "Select your language",
    options=["en", "th"],
    format_func=lambda x: "English" if x == "en" else "Thai"
)

st.markdown("### 🎤 Speak Your Question")

audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e74c3c",
    neutral_color="#2ecc71",
    icon_size="2x"
)

if audio_bytes is not None and len(audio_bytes) > 0 and audio_bytes != st.session_state.last_audio:
    st.session_state.last_audio = audio_bytes
    st.audio(audio_bytes, format="audio/wav")

    with st.spinner("Transcribing and thinking..."):
        try:
            tmp_path = os.path.join(tempfile.gettempdir(), "ktb_audio.wav")
            with open(tmp_path, "wb") as f:
                f.write(audio_bytes)

            with open(tmp_path, "rb") as f:
                response = requests.post(
                    "http://127.0.0.1:8000/agent/voice",
                    files={"file": ("audio.wav", f, "audio/wav")},
                    data={"language": language},
                    timeout=300
                )

            if response.status_code == 200:
                data     = response.json()
                answer   = data.get("response", "No response received.")
                tool     = data.get("selected_tool", "unknown")
                original = data.get("original_text", "")
                text     = data.get("english_query", "Voice input")
                display  = original if original else text

                st.session_state.messages.append({"role": "user", "content": "🎤 " + display})
                st.session_state.messages.append({"role": "assistant", "content": answer})

                with st.chat_message("user"):
                    st.markdown("🎤 " + display)
                    if original and original != text:
                        st.caption("Translated: " + text)
                with st.chat_message("assistant"):
                    st.markdown(answer)
                    st.caption("Topic: " + tool.replace("_", " ").title())
            else:
                st.error("Server error: " + response.text)

        except Exception as e:
            st.error("Error: " + str(e))

st.markdown("### ⌨️ Or Type Your Question")

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/agent/text",
                    data={"text": prompt, "language": language},
                    timeout=60
                )
                data   = response.json()
                answer = data.get("response", "No response received.")
                tool   = data.get("selected_tool", "unknown")

                st.markdown(answer)
                st.caption("Topic: " + tool.replace("_", " ").title())

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error("Error: " + str(e))

st.markdown("---")
if st.button("🔄 Reset Conversation"):
    requests.post("http://127.0.0.1:8000/agent/reset")
    st.session_state.messages = []
    st.session_state.last_audio = None
    st.rerun()