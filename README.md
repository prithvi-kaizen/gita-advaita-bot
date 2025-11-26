A domain-specific LLM fine-tuned on the Bhagavad Gita and Advaita Vedanta philosophy.

## Project Overview
- **Model:** Llama 3.2 3B (Fine-tuned)
- **Technique:** QLoRA (Quantized Low-Rank Adaptation)
- **Framework:** Apple MLX
- **Hardware:** MacBook Pro (M3 Pro)

## How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run app.py`

## Dataset
Trained on 18,000+ Q&A pairs grounded in Vedic scriptures.

hugging face deploy : https://huggingface.co/spaces/Prithviraj6544/gita-chatbot-live

(for mac only) https://huggingface.co/Prithviraj6544/gita-advaita-v1/tree/main

RAG based implementation : https://github.com/Sujato-Dutta/Vedic-Spiritual-Master-Chatbot

RAG model deployment : https://k8xjj6hegddbhysmilqnfz.streamlit.app/
