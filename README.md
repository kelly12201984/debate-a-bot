# 🤖 Debate-A-Bot: Human Values Alignment Explorer

**Debate-A-Bot** is an interactive Streamlit app designed to explore AI alignment and ethical decision-making. Users select (or write) a debate topic and compare responses from two AI bots: one aligned with human values, and another with a configurable misaligned persona (e.g., goal-focused, profit-driven, or open-source AI). Users can vote on which bot they believe better reflects human values and view live results.

## 🔍 Features

- 🎯 Select or write your own debate topic
- 🧠 Choose from various AI personas
- 🧵 Generate side-by-side debates
- 🗳 Vote on the response that better reflects human values
- 📊 Live voting results
- 🧠 Optional "Explainability Mode" to show reasoning behind each bot's perspective

## 🚀 Live Demo

👉 [Click here to launch the app](https://kellys-debate-a-bot.streamlit.app/)

## 🛠 Tech Stack

- Python 🐍
- Streamlit 📊
- OpenAI GPT-4 API 🤖

## 📁 Project Structure

```plaintext
debate_a_bot/
│
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
├── .streamlit/
│   └── secrets.toml     # API key (excluded from repo)
