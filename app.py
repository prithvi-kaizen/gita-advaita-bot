import streamlit as st
from mlx_lm import load, generate

# PAGE CONFIG
st.set_page_config(page_title="Gita AI", page_icon="🕉️", layout="centered")

# HEADER
st.title("🕉️ Gita & Advaita AI")
st.caption("A spiritual companion fine-tuned on the Bhagavad Gita and Advaita Vedanta.")

# LOAD MODEL (Cached so it doesn't reload every time you type)
@st.cache_resource
def load_model():
    # We load the base model from your local folder
    # AND the new "adapters" (the brains you are training right now)
    model, tokenizer = load(
        "./llama-3b",
        adapter_path="adapters"  # This points to the folder created by your training
    )
    return model, tokenizer

# STATUS INDICATOR
with st.spinner("Meditating on the scriptures (Loading Model)..."):
    model, tokenizer = load_model()

# CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Namaste. I am here to guide you through the wisdom of the Gita. What troubles your mind?"}
    ]

# DISPLAY CHAT
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# USER INPUT
if prompt := st.chat_input("Ask a question about life, karma, or dharma..."):
    # 1. Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Format the prompt for Llama 3
    # We apply the chat template to the last few messages to keep context
    chat_history = st.session_state.messages[-3:] 
    full_prompt = tokenizer.apply_chat_template(chat_history, tokenize=False, add_generation_prompt=True)

    # 3. Generate Answer
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response_text = generate(
            model, 
            tokenizer, 
            prompt=full_prompt, 
            max_tokens=256,   # Limit length for faster replies
            verbose=True
        )
        message_placeholder.write(response_text)
    
    # 4. Save assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})