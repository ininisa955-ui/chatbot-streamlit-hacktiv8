import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# --- 1. Page Configuration and Title ---

# Set the title and a caption for the web page
st.title("🏋🏻Chatbot Gym & Fitness")
st.caption("Bingung soal berat badan? Pengen makan enak tapi takut gendut? Santai aja! Aplikasi ini punya solusinya. Cek BMI-mu biar nggak penasaran, dapat ide makanan yang bikin happy dan tetap sehat, plus rekomendasi olahraga yang nggak bikin stres. Yuk, mulai hidup sehat sekarang!")

# --- 2. Sidebar for Settings ---

# Create a sidebar section for app settings using 'with st.sidebar:'
with st.sidebar:
    # Add a subheader to organize the settings
    st.subheader("Settings")
    
    # Create a text input field for the Google AI API Key.
    # 'type="password"' hides the key as the user types it.
    google_api_key = st.text_input("Google AI API Key", type="password")
    
    # Create a button to reset the conversation.
    # 'help' provides a tooltip that appears when hovering over the button.
    reset_button = st.button("Reset Conversation", help="Clear all messages and start fresh")

# --- 3. API Key and Agent Initialization ---

# Check if the user has provided an API key.
# If not, display an informational message and stop the app from running further.
if not google_api_key:
    st.info("Please add your Google AI API key in the sidebar to start chatting.", icon="🗝️")
    st.stop()

# This block of code handles the creation of the LangGraph agent.
# It's designed to be efficient: it only creates a new agent if one doesn't exist
# or if the user has changed the API key in the sidebar.

# We use `st.session_state` which is Streamlit's way of "remembering" variables
# between user interactions (like sending a message or clicking a button).
if ("agent" not in st.session_state) or (getattr(st.session_state, "_last_key", None) != google_api_key):
    try:
        # Initialize the LLM with the API key
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=google_api_key,
            temperature=0.7
        )
        
        # Create a simple ReAct agent with the LLM
        st.session_state.agent = create_react_agent(
            model=llm,
            tools=[],  # No tools for this simple example
            prompt="You are a helpful, friendly assistant. Respond concisely and clearly."
        )
        
        # Store the new key in session state to compare against later.
        st.session_state._last_key = google_api_key
        # Since the key changed, we must clear the old message history.
        st.session_state.pop("messages", None)
    except Exception as e:
        # If the key is invalid, show an error and stop.
        st.error(f"Invalid API Key or configuration error: {e}")
        st.stop()


def hitung_bmi(berat, tinggi):
    tinggi_m = tinggi / 100
    return berat / (tinggi_m ** 2)

def rekomendasi_makanan(bmi):
    if bmi < 18.5:
        return "Tingkatkan asupan kalori. Rekomendasi: nasi merah, alpukat, ayam panggang, kacang-kacangan."
    elif 18.5 <= bmi <= 24.9:
        return "Pertahankan pola makan seimbang. Rekomendasi: sayuran, ikan, oatmeal, buah segar."
    elif 25 <= bmi <= 29.9:
        return "Kurangi makanan tinggi kalori. Rekomendasi: sayuran hijau, dada ayam, telur, salad rendah kalori."
    else:
        return "Fokus pada diet defisit kalori. Rekomendasi: brokoli, ikan kukus, putih telur, buah rendah gula."

def rekomendasi_olahraga(bmi):
    if bmi < 18.5:
        return "Latihan: strength training ringan untuk meningkatkan massa otot."
    elif 18.5 <= bmi <= 24.9:
        return "Latihan: kombinasi cardio dan strength training."
    elif 25 <= bmi <= 29.9:
        return "Latihan: cardio intensitas sedang seperti jogging atau bersepeda."
    else:
        return "Latihan: low-impact cardio seperti jalan cepat, renang, dan latihan kekuatan bertahap."


menu = st.selectbox("Pilih fitur:", ["Hitung BMI", "Rekomendasi Makanan", "Rekomendasi Olahraga"])

berat = st.number_input("Masukkan berat badan (kg):", min_value=1.0)
tinggi = st.number_input("Masukkan tinggi badan (cm):", min_value=1.0)

if st.button("Proses"):
    bmi = hitung_bmi(berat, tinggi)
    st.write(f"BMI Anda: {bmi:.2f}")

    if menu == "Hitung BMI":
        pass
    elif menu == "Rekomendasi Makanan":
        st.write(rekomendasi_makanan(bmi))
    elif menu == "Rekomendasi Olahraga":
        st.write(rekomendasi_olahraga(bmi))
