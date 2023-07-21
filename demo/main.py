from dotenv import load_dotenv
import os
import requests
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
huggingface_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

with st.sidebar:
    api_key = st.text_input(
        "API Key", key="chatbot_api_key", type="password"
    )
    model_name = st.selectbox(
        "Chat API Endpoint",
        options=["gpt-4", "hf-gpt2"],
        index=0,
    )

genoss_endpoint = "http://localhost:4321"

st.title("🐂🌈 Genoss")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = ""

    print(api_key)
    # Use the user-provided API key if available, otherwise use the API key from the .env file
    if api_key == "" or api_key is None:
        api_key = api_key if api_key else (huggingface_api_key if model_name.startswith("hf") else openai_api_key)
        if api_key == "" or api_key is None:
            st.error("Please provide an API key")
            st.stop()

    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.post(
            url=f"{genoss_endpoint}/chat/completions",
            headers=headers,
            json={
                "model": model_name,
                "messages": st.session_state.messages,
            },
        )
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        msg = response.json()['choices'][0]['message']
    except Exception as e:
        msg = f"Error: {e}"

    st.empty()

    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg["content"])
