# chatbot_app.py
import streamlit as st
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖")

st.title("🤖 CodeAlpha FAQ Assistant")
st.markdown("---")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# FAQ Database
faqs = [
    {'question': 'What is CodeAlpha internship?',
     'answer': 'CodeAlpha internship is a program where students work on real-world AI and software development projects.'},
    {'question': 'How long is the internship?',
     'answer': 'The internship duration is typically 4 weeks, requiring 2-3 projects.'},
    {'question': 'Do I get a certificate?',
     'answer': 'Yes, you receive a certificate upon completing minimum 2 tasks.'},
]

# Preprocess FAQs
vectorizer = TfidfVectorizer()
faq_questions = [f['question'] for f in faqs]
faq_vectors = vectorizer.fit_transform(faq_questions)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about CodeAlpha internship..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Find best match
            question_vec = vectorizer.transform([prompt])
            similarities = cosine_similarity(question_vec, faq_vectors).flatten()
            best_match = np.argmax(similarities)

            if similarities[best_match] > 0.2:
                response = faqs[best_match]['answer']
            else:
                response = "I don't have an answer. Please contact CodeAlpha support."

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})