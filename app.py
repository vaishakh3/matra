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

# Minimal dark CSS
custom_css = """
.gradio-container {
    background: #000 !important;
    color: white;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    min-height: 100vh;
}

.main-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 120px 20px 20px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}

.logo {
    text-align: center;
    margin-bottom: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
}

.logo-symbol {
    width: 32px;
    height: 32px;
    border: 2px solid white;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.logo-line {
    width: 20px;
    height: 20px;
    border: 2px solid white;
    border-top: none;
    border-right: none;
    transform: rotate(-45deg);
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -10px;
    margin-left: -10px;
}

.logo-text {
    font-size: 24px;
    font-weight: 600;
    color: white;
    letter-spacing: 0.5px;
}

.input-container {
    margin-bottom: 30px;
    width: 100%;
    max-width: 600px;
}

.input-box {
    width: 100%;
    background: #111;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 16px;
    color: white;
    font-size: 16px;
    outline: none;
}

.input-box:focus {
    border-color: #00C8C8;
}

.generate-btn {
    background: #00C8C8;
    color: #000;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 16px;
}

.output-container {
    margin-top: 30px;
    width: 100%;
    max-width: 600px;
}

.video-container {
    background: #000;
    border-radius: 8px;
    overflow: hidden;
}

.code-container {
    background: #111;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 16px;
    margin-top: 16px;
}

.status {
    text-align: center;
    margin: 10px 0;
    padding: 16px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    width: 100%;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.status-info {
    background: rgba(0, 200, 200, 0.1);
    color: #00C8C8;
    border: 1px solid rgba(0, 200, 200, 0.2);
}

.status-success {
    background: rgba(0, 200, 200, 0.15);
    color: #00C8C8;
    border: 1px solid rgba(0, 200, 200, 0.3);
    font-weight: 600;
}

.status-error {
    background: rgba(255, 100, 100, 0.1);
    color: #FF6464;
    border: 1px solid rgba(255, 100, 100, 0.2);
}
"""

# Create minimal UI
with gr.Blocks(title="Matra", css=custom_css) as demo:

    with gr.Column(elem_classes=["main-container"]):
        
        # Logo
        gr.HTML("""<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <img src="https://i.ibb.co/VW0H6nM5/Matra.png" alt="Matra Logo" style="height: 40px;">
        <h1 style="margin: 0; font-size: 1.5em;">Matra</h1></div>""")
        
        # Input
        with gr.Column(elem_classes=["input-container"]):
            prompt_input = gr.Textbox(
                label="",
                placeholder="Describe what you want to animate...",
                lines=3,
                elem_classes=["input-box"]
            )
            submit_btn = gr.Button("Generate", elem_classes=["generate-btn"])
        
        # Status
        status_box = gr.HTML("", elem_classes=["status"])
        
        # Output
        with gr.Column(elem_classes=["output-container"], visible=False) as output_container:
            output_video = gr.Video(label="", show_label=False)
            with gr.Accordion("Code", open=False):
                output_code = gr.Code(language="python", elem_classes=["code-container"])

    # Event handler
    def on_submit(prompt):
        if not prompt.strip():
            return "", None, gr.update(visible=False), gr.update(value="<div class='status-error'>Enter a prompt</div>")
        
        status_html = '<div class="status-info">Generating animation...</div>'
        
        try:
            code, video = run_manim(prompt)
            if video:
                status_html = '<div class="status-success">Animation ready!</div>'
                return code, video, gr.update(visible=True), gr.update(value=status_html)
            else:
                status_html = '<div class="status-error">Rendering failed</div>'
                return code, None, gr.update(visible=True), gr.update(value=status_html)
        except Exception as e:
            status_html = f'<div class="status-error">Error: {str(e)}</div>'
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
