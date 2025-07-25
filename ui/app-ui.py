import streamlit as st
import requests

st.set_page_config(page_title="Chatbot RAG", layout="wide")

st.title("💬 Chat with your docs")

query = st.text_area("Make a question:", height=100)

if st.button("Submit"):
    if not query.strip():
        st.warning("❗ C'mon. Make a question before submit!")
    else:
        with st.spinner("🔎 looking for answers..."):
            try:
                response = requests.post(
                    "http://backend:8000/ask",
                    json={"query": query},
                    #timeout=10  # optional
                )
                response.raise_for_status()

                data = response.json()
                answer = data.get("answer")

                if answer:
                    st.markdown("### 🧠 Answer:")
                    st.success(answer)
                else:
                    st.warning("⚠️ Nothing received from Ollama.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed the request: {e}")
            except ValueError:
                st.error("⚠️ The backend return an invalid JSON.")
