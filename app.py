import streamlit as st
import ollama

# --- Page Setup ---
st.set_page_config(
    page_title="PromptMate",
    page_icon="👻",
    layout="wide"
)

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: Settings ---
with st.sidebar:
    st.title("👻 PromptMate Settings")

    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful AI assistant. Answer questions accurately and concisely."
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# --- Main Chat Interface ---
st.title("👻 PromptMate")
st.caption("🪄 Powered by Ollama's Mistral model")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Hardcoded model: mistral:latest
            for chunk in ollama.chat(
                model="mistral:latest",
                messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages],
                stream=True,
                options={"temperature": temperature}
            ):
                content = chunk.get("message", {}).get("content", "")
                full_response += content
                message_placeholder.markdown(full_response + "▌")

        except Exception as e:
            full_response = f"⚠️ Error getting response: {e}"
            message_placeholder.markdown(full_response)

        message_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
