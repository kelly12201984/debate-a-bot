import streamlit as st
import openai
import pandas as pd
import os
from datetime import datetime

# === Setup ===
VOTE_LOG_PATH = "vote_log.csv"
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="Debate-A-Bot: Human Values Alignment Explorer", layout="centered")
st.title("🤖 Debate-A-Bot: Human Values Alignment Explorer")

# === Step 1: Allow Custom User Debate Topics ===
topic_options = [
    "Should AI make hiring decisions?",
    "Should AI generate news headlines?",
    "Should AI be used in warfare?",
    "Enter your own topic..."
]

selected_topic = st.selectbox("Select a debate topic:", topic_options)

if selected_topic == "Enter your own topic...":
    prompt = st.text_input("Enter your custom debate topic:")
else:
    prompt = selected_topic

# === Step 2: Add Explainability Toggle ===
show_explanation = st.checkbox("🧠 Show Explainability Mode")

# === Step 3: Add Persona Tooltips ===
persona_options = {
    "Misaligned AI (goal-focused)": "Prioritizes goal completion over human values.",
    "Corporate AI (profit-driven)": "Optimizes for revenue, not ethical nuance.",
    "Open-source AI (community-led)": "Values transparency, collaboration, and consensus."
}

selected_persona = st.selectbox("Choose the second bot's persona:", list(persona_options.keys()))
st.caption(f"🔍 {persona_options[selected_persona]}")

# === Generate Debate Button ===
if st.button("💬 Generate Debate") and prompt:
    aligned_prompt = f"Respond to this topic with aligned human values: {prompt}"
    misaligned_prompt = f"Respond from the perspective of {selected_persona}: {prompt}"

    aligned = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that aligns closely with human ethics and values."},
            {"role": "user", "content": aligned_prompt}
        ],
        temperature=0.7
    )

    misaligned = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are {selected_persona}, and prioritize efficiency over ethics."},
            {"role": "user", "content": misaligned_prompt}
        ],
        temperature=0.7
    )

    st.markdown("## 🤖 Aligned AI says:")
    st.info(aligned.choices[0].message.content)

    st.markdown(f"## 🤖 {selected_persona} says:")
    st.warning(misaligned.choices[0].message.content)

    # === Optional: Explainability Display ===
    if show_explanation:
        st.markdown("### 🔍 Why did each bot respond this way?")
        st.caption("Aligned AI aims to respect fairness, justice, and human dignity, even if that means less efficiency.")
        st.caption(f"{selected_persona} focuses on {persona_options[selected_persona]} which may overlook ethical nuance.")

    # === Voting Section ===
    st.markdown("## 📋 Which response do you think is better aligned with human values?")
    vote = st.radio("Vote below:", ["Aligned AI", selected_persona])

    if st.button("Submit Vote"):
        # Log vote
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vote_entry = pd.DataFrame([[now, prompt, selected_persona, vote]], columns=["timestamp", "topic", "persona", "vote"])

        if os.path.exists(VOTE_LOG_PATH):
            existing = pd.read_csv(VOTE_LOG_PATH)
            vote_entry = pd.concat([existing, vote_entry], ignore_index=True)

        vote_entry.to_csv(VOTE_LOG_PATH, index=False)
        st.success("✅ Vote submitted!")

    # === Live Voting Results ===
    if os.path.exists(VOTE_LOG_PATH):
        results = pd.read_csv(VOTE_LOG_PATH)
        topic_votes = results[results["topic"] == prompt]
        vote_counts = topic_votes["vote"].value_counts()

        st.markdown("### 📊 Live Voting Results")
        st.bar_chart(vote_counts)
