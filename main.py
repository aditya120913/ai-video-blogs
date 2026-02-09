import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

# 1. Page Configuration
st.set_page_config(page_title="AI Video-to-Blog", page_icon="📝", layout="centered")

st.title("🎥 YouTube to SEO Blog Post Generator")
st.markdown("Turn any YouTube video into a high-quality blog post in seconds.")

# 2. Sidebar for API Key (Keep it secure)
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get your key at [Google AI Studio](https://aistudio.google.com/)")

# 3. Main Input Area
video_url = st.text_input("Paste YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Generate Blog Post"):
    if not api_key:
        st.error("Please provide an API Key in the sidebar!")
    elif not video_url:
        st.warning("Please paste a YouTube URL first.")
    else:
        try:
            with st.spinner("Step 1: Extracting Transcript..."):
                # Extract Video ID from URL
                if "v=" in video_url:
                    video_id = video_url.split("v=")[1].split("&")[0]
                else:
                    video_id = video_url.split("/")[-1]
                
                # Fetch Transcript
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([item['text'] for item in transcript_list])

            with st.spinner("Step 2: AI is writing your blog..."):
                # Initialize Gemini Client
                client = genai.Client(api_key=api_key)
                
                # Professional Prompt
                prompt = f"""
                You are a professional SEO copywriter. Transform the following YouTube transcript 
                into a viral, engaging, and SEO-optimized blog post. 
                Include:
                - A catchy H1 Title
                - An introduction
                - Subheadings (H2, H3)
                - Bullet points for key takeaways
                - A conclusion
                
                Transcript: {transcript_text}
                """
                
                # Generate Content
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=prompt
                )

            # 4. Display Results
            st.success("✨ Your Blog Post is Ready!")
            st.divider()
            st.markdown(response.text)
            
            # Add a copy button for the user
            st.button("Re-generate", type="secondary")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Tip: Make sure the video has 'Captions/Subtitles' enabled.")
