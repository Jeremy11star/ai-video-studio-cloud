import streamlit as st
import requests
import time
import uuid

# Inside your System 1 tab:
if st.button("🚀 Generate Long-Form Video"):
    if not script_input.strip():
        st.warning("Please paste a script first.")
    else:
        kaggle_url = st.secrets["KAGGLE_API_URL"].rstrip("/")
        job_id = f"vid_{uuid.uuid4().hex[:8]}"
        payload = {
            "job_id": job_id,
            "channel": target_channel,
            "script": script_input,
            "voice_style": voice_delivery,
            "music_mode": bg_music
        }
        
        with st.spinner("Sending job to Kaggle GPU server..."):
            res = requests.post(f"{kaggle_url}/generate", json=payload, timeout=15)
        
        if res.status_code == 200:
            status_box = st.empty()
            while True:
                status_res = requests.get(f"{kaggle_url}/status/{job_id}", timeout=10).json()
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
