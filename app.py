import streamlit as st
import requests
import time
import uuid

st.set_page_config(page_title="AI Video Studio Cloud", page_icon="🎬", layout="wide")

st.title("🎬 AI Video Production Studio")
st.markdown("Cloud-powered autonomous video generation studio running on Kaggle GPU & Gemini.")

# Navigation Tabs for Your 3 Systems
tab1, tab2, tab3 = st.tabs([
    "📺 System 1: Long-Form YouTube", 
    "📱 System 2: Shorts Repurposing", 
    "🏢 System 3: Brand Commercials"
])

with tab1:
    st.header("Long-Form YouTube Explainer Generator (Kurzgesagt Style)")
    target_channel = st.text_input("Target Channel Name", value="Remy Finance")
    script_input = st.text_area("Paste Your 15-20 Min Script Here", height=250, placeholder="Enter your full educational or financial script...")
    
    col1, col2 = st.columns(2)
    with col1:
        voice_delivery = st.selectbox("Voice Delivery Style", ["Alex Hormozi High-Energy (+18% Pacing)", "Standard Professional"])
    with col2:
        bg_music = st.selectbox("Background Music Mode", ["Cinematic & Curious", "Upbeat & Motivational", "Dark & Mysterious"])

    if st.button("🚀 Generate Long-Form Video"):
        if not script_input.strip():
            st.warning("Please paste a script first.")
        else:
            kaggle_url = st.secrets["KAGGLE_API_URL"].rstrip("/")
            job_id = f"vid_{uuid.uuid4().hex[:8]}"
            payload = {
                "job_id": job_id,
                "system_type": "system_1_longform",
                "channel": target_channel,
                "script": script_input,
                "voice_style": voice_delivery,
                "music_mode": bg_music
            }
            
            with st.spinner("Sending job to Kaggle GPU server..."):
                try:
                    res = requests.post(f"{kaggle_url}/generate", json=payload, timeout=15)
                except Exception as e:
                    st.error(f"Failed to connect to Kaggle server: {e}")
                    res = None
            
            if res and res.status_code == 200:
                status_box = st.empty()
                while True:
                    try:
                        status_res = requests.get(f"{kaggle_url}/status/{job_id}", timeout=10).json()
                    except:
                        status_res = {"status": "processing"}
                    state = status_res.get("status")
                    
                    if state == "completed":
                        status_box.success(f"✅ Video Ready! Detected Mood: {status_res.get('mood')} | Segments: {status_res.get('segments_count')}")
                        video_bytes = requests.get(f"{kaggle_url}/download/{job_id}").content
                        st.video(video_bytes)
                        st.download_button("⬇️ Download Master MP4", data=video_bytes, file_name=f"{job_id}.mp4", mime="video/mp4")
                        break
                    elif state == "failed":
                        status_box.error(f"❌ Render failed: {status_res.get('error')}")
                        break
                    else:
                        status_box.info(f"⏳ {status_res.get('progress', 'Processing...')}")
                        time.sleep(4)

with tab2:
    st.header("📱 System 2: Shorts Repurposing Engine")
    st.info("Supoclip-powered vertical short clips generator. Ready for connection!")

with tab3:
    st.header("🏢 System 3: Brand & Commercial AI Agent")
    st.info("Veo-standard character & image consistency commercial generator. Ready for connection!")
