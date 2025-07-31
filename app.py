import os
import gradio as gr
import subprocess
import re
from datetime import datetime
from groq import Groq
import shutil
import time
import dotenv

dotenv.load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def strip_non_ascii(text):
    return ''.join(c for c in text if ord(c) < 128)

def get_manim_code(prompt: str, scene_name: str) -> str:
    messages = [
        {
            "role": "user",
            "content": f"Give python Manim code for: '{prompt}'. Only code, no explanation. No comments. Dont begin with triple quoted ```python. Name the scene class exactly `{scene_name}`. Use Text() instead of Tex() unless strictly necessary."
        }
    ]

    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=messages,
        temperature=0.8,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )

    raw_code = response.choices[0].message.content.strip()
    safe_code = strip_non_ascii(raw_code)
    return safe_code

def run_manim(prompt: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scene_name = f"Scene_{timestamp}"
    filename = f"generated/{scene_name}.py"
    os.makedirs("generated", exist_ok=True)

    code = get_manim_code(prompt, scene_name)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    # Clean old media
    shutil.rmtree("media/videos", ignore_errors=True)

    try:
        subprocess.run(f"manim -ql {filename} {scene_name}", shell=True, check=True)
    except subprocess.CalledProcessError:
        return code, None

    video_file = None
    for root, _, files in os.walk("media/videos"):
        for file in files:
            if file.endswith(".mp4") and scene_name in file:
                full_path = os.path.join(root, file)
                video_file = full_path.replace("\\", "/")
                break

    return code, video_file if video_file and os.path.exists(video_file) else None

# Modern UI CSS matching the reference design
custom_css = """
/* Import Montserrat font */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&display=swap');

/* Global styles */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background-color: #1a1a1a;
  color: white;
  min-height: 100vh;
}

/* Main container */
.gradio-container {
  background-color: #1a1a1a !important;
  color: white !important;
  min-height: 100vh;
}

/* Override Gradio's default styling */
.gradio-container .contain {
  max-width: 768px !important;
  margin: 0 auto !important;
  padding: 3rem 1.5rem !important;
}

/* Header/Logo section */
.matra-header {
  text-align: center;
  margin-bottom: 3rem;
}

.matra-logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.matra-logo {
  width: 32px;
  height: 32px;
  filter: invert(1);
}

.matra-title {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.875rem;
  font-weight: 500;
  letter-spacing: 0.025em;
  margin: 0;
  color: white;
}

.matra-subtitle {
  color: #9ca3af;
  font-size: 0.875rem;
  margin: 0;
}

/* Input section */
.input-container {
  margin-bottom: 2rem;
  width: 100%;
}

.search-container {
  display: flex;
  align-items: center;
  background-color: #2a2a2a;
  border: 1px solid #3a3a3a;
  border-radius: 0.75rem;
  padding: 1rem;
  transition: border-color 0.2s;
  width: 100%;
}

.search-container:focus-within {
  border-color: rgba(255, 255, 255, 0.2);
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: white;
  font-size: 1rem;
  padding: 0;
}

.search-input::placeholder {
  color: #6b7280;
}

.generate-button {
  background-color: white;
  color: black;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  margin-left: 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.generate-button:hover {
  background-color: #e5e7eb;
}

.generate-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Status display */
.status {
  text-align: center;
  margin: 1rem 0;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  width: 100%;
}

.status-info {
  background-color: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.status-success {
  background-color: rgba(34, 197, 94, 0.1);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-error {
  background-color: rgba(239, 68, 68, 0.1);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

/* Output container */
.output-container {
  margin-top: 2rem;
  width: 100%;
}

/* Animation player */
.animation-player {
  background-color: #2a2a2a;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.player-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.player-title {
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  margin: 0;
}

/* Code display */
.code-container {
  background-color: #2a2a2a;
  border-radius: 0.5rem;
  padding: 1rem;
}

.code-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.code-title {
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  margin: 0;
}

/* Override Gradio specific styles */
.gradio-container .wrap {
  background-color: #1a1a1a !important;
}

.gradio-container .panel {
  background-color: #2a2a2a !important;
  border: 1px solid #3a3a3a !important;
}

.gradio-container .form {
  background-color: transparent !important;
}

.gradio-container input[type="text"], .gradio-container textarea {
  background-color: #2a2a2a !important;
  border: 1px solid #3a3a3a !important;
  color: white !important;
  border-radius: 0.75rem !important;
  padding: 1rem !important;
  font-size: 1rem !important;
}

.gradio-container input[type="text"]:focus, .gradio-container textarea:focus {
  border-color: rgba(255, 255, 255, 0.2) !important;
  box-shadow: none !important;
}

.gradio-container input[type="text"]::placeholder, .gradio-container textarea::placeholder {
  color: #6b7280 !important;
}

.gradio-container button {
  background-color: white !important;
  color: black !important;
  border: none !important;
  border-radius: 0.5rem !important;
  padding: 0.5rem 1rem !important;
  transition: background-color 0.2s !important;
  font-weight: 500 !important;
}

.gradio-container button:hover {
  background-color: #e5e7eb !important;
}

.gradio-container .accordion {
  background-color: #2a2a2a !important;
  border: 1px solid #3a3a3a !important;
  border-radius: 0.5rem !important;
}

.gradio-container .accordion summary {
  background-color: transparent !important;
  color: white !important;
  padding: 0.75rem !important;
}

.gradio-container pre {
  background-color: rgba(0, 0, 0, 0.3) !important;
  border-radius: 0.25rem !important;
  padding: 0.75rem !important;
  color: #d1d5db !important;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
  font-size: 0.75rem !important;
}

/* Responsive design */
@media (max-width: 768px) {
  .gradio-container .contain {
    padding: 2rem 1rem !important;
  }
  
  .matra-title {
    font-size: 1.5rem;
  }
  
  .search-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .generate-button {
    margin-left: 0;
    align-self: stretch;
    justify-content: center;
  }
}
"""

# Create modern UI matching the reference design
with gr.Blocks(title="Matra", css=custom_css) as demo:

    # Header/Logo section
    with gr.Column(elem_classes=["matra-header"]):
        gr.HTML("""
        <div class="matra-logo-container">
            <img src="https://i.ibb.co/VW0H6nM5/Matra.png" alt="Matra Logo" class="matra-logo">
            <h1 class="matra-title">Matra</h1>
        </div>
        <p class="matra-subtitle">AI-powered animation generation</p>
        """)
    
    # Input section
    with gr.Column(elem_classes=["input-container"]):
        with gr.Row():
            prompt_input = gr.Textbox(
                label="",
                placeholder="Describe what you want to animate...",
                lines=1,
                elem_classes=["search-input"],
                container=False,
                scale=4
            )
            submit_btn = gr.Button(
                "Generate", 
                elem_classes=["generate-button"],
                scale=1
            )
    
    # Status
    status_box = gr.HTML("", elem_classes=["status"])
    
    # Output
    with gr.Column(elem_classes=["output-container"], visible=False) as output_container:
        with gr.Column(elem_classes=["animation-player"]):
            gr.HTML('<h3 class="player-title">Generated Animation</h3>')
            output_video = gr.Video(label="", show_label=False)
        
        with gr.Accordion("Generated Code", open=False, elem_classes=["code-container"]):
            output_code = gr.Code(language="python", show_label=False)

    # Event handler
    def on_submit(prompt):
        if not prompt.strip():
            return "", None, gr.update(visible=False), gr.update(value='<div class="status status-error">Please enter a prompt</div>')
        
        status_html = '<div class="status status-info">Generating animation...</div>'
        
        try:
            code, video = run_manim(prompt)
            if video:
                status_html = '<div class="status status-success">Animation ready!</div>'
                return code, video, gr.update(visible=True), gr.update(value=status_html)
            else:
                status_html = '<div class="status status-error">Rendering failed</div>'
                return code, None, gr.update(visible=True), gr.update(value=status_html)
        except Exception as e:
            status_html = f'<div class="status status-error">Error: {str(e)}</div>'
            return "", None, gr.update(visible=False), gr.update(value=status_html)

    submit_btn.click(
        fn=on_submit,
        inputs=prompt_input,
        outputs=[output_code, output_video, output_container, status_box]
    )

demo.launch(server_name="0.0.0.0",
            server_port=int(os.environ.get("PORT", 7860)),
            favicon_path="Matra.png",
            pwa=True)
