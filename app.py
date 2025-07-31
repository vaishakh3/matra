import os
import gradio as gr
import subprocess
import re
from datetime import datetime
from groq import Groq
import shutil
import time
import dotenv
import json
import html

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

# Clean CSS with proper Gradio styling
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Montserrat:wght@300;400;500;600;700&display=swap');

/* Global Styles */
.gradio-container {
    background: #1a1a1a !important;
    color: white !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    min-height: 100vh !important;
}

body {
    background: #1a1a1a !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Main Container - Made bigger */
.main-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    padding: 60px 32px !important;
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

/* Logo Section - Made bigger */
.logo-section {
    text-align: center !important;
    margin-bottom: 60px !important;
}

.logo-container {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 16px !important;
    margin-bottom: 12px !important;
}

.logo-text {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 40px !important;
    font-weight: 500 !important;
    color: white !important;
    letter-spacing: 0.5px !important;
    margin: 0 !important;
}

.logo-subtitle {
    color: #9ca3af !important;
    font-size: 16px !important;
    margin: 0 !important;
}

/* Input Section Styling */
.input-section {
    width: 100% !important;
    margin-bottom: 40px !important;
}

/* Style the input row to look like one container */
.input-row {
    background: #2a2a2a !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 16px !important;
    padding: 20px 20px 20px 16px !important;
    display: flex !important;
    align-items: center !important;
    gap: 16px !important;
    transition: border-color 0.2s ease !important;
}

.input-row:focus-within {
    border-color: inherit !important;
}

/* Search icon */
.search-icon {
    color: #9ca3af !important;
    width: 20px !important;
    height: 20px !important;
    flex-shrink: 0 !important;
}

/* Hide default Gradio styling for textbox */
.input-row .gradio-textbox {
    background: transparent !important;
    border: none !important;
    flex: 1 !important;
}

.input-row .gradio-textbox .wrap {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

.input-row .gradio-textbox .scroll-hide {
    background: transparent !important;
    border: none !important;
}

.input-row .gradio-textbox textarea {
    background: #23272f !important;
    /* Autofill override for Chrome/Webkit */
    box-shadow: 0 0 0 1000px #23272f inset !important;
    -webkit-box-shadow: 0 0 0 1000px #23272f inset !important;
    -webkit-text-fill-color: #fff !important;
    transition: background-color 5000s ease-in-out 0s !important;
}

/* Autofill override for Chrome/Webkit */
.input-row .gradio-textbox textarea:-webkit-autofill,
.input-row .gradio-textbox textarea:-webkit-autofill:focus {
    box-shadow: 0 0 0 1000px #23272f inset !important;
    -webkit-box-shadow: 0 0 0 1000px #23272f inset !important;
    -webkit-text-fill-color: #fff !important;
    background: #23272f !important;
    transition: background-color 5000s ease-in-out 0s !important;
}
    border: none !important;
    color: white !important;
    font-size: 18px !important;
    resize: none !important;
    outline: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.input-row .gradio-textbox textarea::placeholder {
    color: #6b7280 !important;
    font-size: 18px !important;
}

/* Style the button to be small and inline */
.input-row .gradio-button {
    background: white !important;
    border: none !important;
    border-radius: 10px !important;
    min-width: 44px !important;
    height: 44px !important;
    padding: 0 !important;
    flex-shrink: 0 !important;
}

.input-row .gradio-button .wrap {
    background: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0 !important;
    min-width: 44px !important;
    height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.input-row .gradio-button button {
    background: white !important;
    color: black !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    cursor: pointer !important;
    transition: background-color 0.2s ease !important;
    width: 44px !important;
    height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
    margin: 0 !important;
}

.input-row .gradio-button button:hover {
    background: #e5e7eb !important;
}

/* Suggestions - Made bigger */
.suggestions {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 12px !important;
    justify-content: center !important;
    margin-top: 20px !important;
}

.suggestion-chip {
    background: #2a2a2a !important;
    border: 1px solid #3a3a3a !important;
    color: #9ca3af !important;
    padding: 8px 16px !important;
    border-radius: 24px !important;
    font-size: 14px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

.suggestion-chip:hover {
    color: white !important;
    background: #3a3a3a !important;
}

/* Status Messages - Made bigger */
.status-message {
    text-align: center !important;
    padding: 20px 32px !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    margin: 20px 0 !important;
    width: 100% !important;
}

.status-loading {
    background: rgba(59, 130, 246, 0.1) !important;
    color: #60a5fa !important;
    border: 1px solid rgba(59, 130, 246, 0.2) !important;
}

.status-success {
    background: rgba(34, 197, 94, 0.1) !important;
    color: #4ade80 !important;
    border: 1px solid rgba(34, 197, 94, 0.2) !important;
}

.status-error {
    background: rgba(239, 68, 68, 0.1) !important;
    color: #f87171 !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
}

/* Video Player - Made bigger */
.video-container {
    background: #2a2a2a !important;
    border-radius: 12px !important;
    padding: 20px !important;
    width: 100% !important;
    margin-bottom: 20px !important;
}

.video-header {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-bottom: 20px !important;
}

.video-title {
    color: white !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    margin: 0 !important;
}

.video-subtitle {
    color: #9ca3af !important;
    font-size: 14px !important;
    margin: 0 !important;
}

.video-player {
    width: 100% !important;
    border-radius: 8px !important;
    background: #0a0a0a !important;
    min-height: 400px !important;
}

/* Code Section - Made bigger */
.code-section {
    background: #2a2a2a !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    width: 100% !important;
}

.code-content {
    background: #1a1a1a !important;
    color: #e5e7eb !important;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 20px !important;
    overflow-x: auto !important;
    max-height: 500px !important;
}

/* Empty State - Made bigger */
.empty-state {
    text-align: center !important;
    padding: 60px 0 !important;
}

.empty-title {
    color: #9ca3af !important;
    font-size: 22px !important;
    margin-bottom: 12px !important;
}

.empty-subtitle {
    color: #6b7280 !important;
    font-size: 16px !important;
}

/* Hide Gradio elements */
footer {
    display: none !important;
}

/* Loading spinner */
.loading-spinner {
    display: inline-block !important;
    width: 18px !important;
    height: 18px !important;
    border: 2px solid #60a5fa !important;
    border-radius: 50% !important;
    border-top-color: transparent !important;
    animation: spin 1s ease-in-out infinite !important;
    margin-right: 8px !important;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
"""

# Suggestions for prompts
suggestions = [
    "Einstein's E=mc²",
    "Sine wave animation", 
    "Pythagorean theorem",
    "Electromagnetic wave",
    "Derivative visualization"
]

def create_suggestion_chips():
    """Create clickable suggestion chips HTML"""
    chips_html = []
    for suggestion in suggestions:
        escaped_text = suggestion.replace("'", "\\'")  # escape single quotes for JS
        visible_text = html.escape(suggestion)  # escape for HTML display
        onclick_code = (
            f"const textarea = document.querySelector('textarea');"
            f"textarea.value='{escaped_text}';"
            f"textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));"
        )
        chip_html = f'<span class="suggestion-chip" onclick="{onclick_code}">{visible_text}...</span>'
        chips_html.append(chip_html)
    
    return f'<div class="suggestions">{"".join(chips_html)}</div>'

# Create the Gradio interface
with gr.Blocks(title="Matra - Mathematical Animation Generator", css=custom_css, theme=gr.themes.Base()) as demo:
    
    # Main container
    with gr.Column(elem_classes=["main-container"]):
        
        # Logo section
        gr.HTML("""
        <div class="logo-section">
            <div class="logo-container">
                <img src="https://i.ibb.co/VW0H6nM5/Matra.png" alt="Matra" style="width: 40px; height: 40px; filter: invert(1);">
                <h1 class="logo-text">Matra</h1>
            </div>
            <p class="logo-subtitle">Mathematical animation generator</p>
        </div>
        """)
        
        # Input section with search icon, input, and button in one row
        with gr.Column(elem_classes=["input-section"]):
            with gr.Row(elem_classes=["input-row"]):
                
                
                # Text input
                prompt_input = gr.Textbox(
                    label="",
                    placeholder="Describe your mathematical animation...",
                    lines=1,
                    show_label=False,
                    container=False,
                    scale=4
                )
                
                # Generate button
                submit_btn = gr.Button(
                    "▶",
                    size="sm",
                    scale=0,
                    min_width=44
                )
            
            # Suggestions
            gr.HTML(create_suggestion_chips())
        
        # Status display
        status_display = gr.HTML("", elem_classes=["status-message"])
        
        # Output section
        with gr.Column(visible=False) as output_section:
            # Video player
            gr.HTML("""
            <div class="video-container">
                <div class="video-header">
                    <div>
                        <h3 class="video-title">Generated Animation</h3>
                        <p class="video-subtitle">Mathematical visualization</p>
                    </div>
                </div>
            </div>
            """)
            
            output_video = gr.Video(
                label="",
                show_label=False,
                elem_classes=["video-player"]
            )
            
            # Code section
            with gr.Accordion("Generated Code", open=False):
                output_code = gr.Code(
                    language="python",
                    show_label=False,
                    elem_classes=["code-content"]
                )
        
        # Empty state
        empty_state = gr.HTML("""
        <div class="empty-state">
            <div class="empty-title">Ready to create</div>
            <div class="empty-subtitle">Enter a mathematical concept above and click generate</div>
        </div>
        """)

    # Event handlers
    def generate_animation(prompt):
        if not prompt.strip():
            return (
                gr.update(value='<div class="status-message status-error">Please enter a prompt</div>'),
                gr.update(visible=False),
                gr.update(visible=True),
                "", 
                None
            )
        
        # Show loading state
        loading_html = '<div class="status-message status-loading"><span class="loading-spinner"></span>Generating animation...</div>'
        
        try:
            # Update status to loading
            yield (
                gr.update(value=loading_html),
                gr.update(visible=False),
                gr.update(visible=False),
                "",
                None
            )
            
            # Generate the animation
            code, video = run_manim(prompt)
            
            if video and os.path.exists(video):
                success_html = '<div class="status-message status-success">✅ Animation generated successfully!</div>'
                yield (
                    gr.update(value=success_html),
                    gr.update(visible=True),
                    gr.update(visible=False),
                    code,
                    video
                )
            else:
                error_html = '<div class="status-message status-error">❌ Failed to generate video. Check the code for errors.</div>'
                yield (
                    gr.update(value=error_html),
                    gr.update(visible=True),
                    gr.update(visible=False),
                    code,
                    None
                )
                
        except Exception as e:
            error_html = f'<div class="status-message status-error">❌ Error: {str(e)}</div>'
            yield (
                gr.update(value=error_html),
                gr.update(visible=False),
                gr.update(visible=True),
                "",
                None
            )

    # Connect the button click
    submit_btn.click(
        fn=generate_animation,
        inputs=[prompt_input],
        outputs=[status_display, output_section, empty_state, output_code, output_video]
    )
    
    # Also trigger on Enter key
    prompt_input.submit(
        fn=generate_animation,
        inputs=[prompt_input],
        outputs=[status_display, output_section, empty_state, output_code, output_video]
    )

# Launch the app

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    favicon_path="./Matra.png" if os.path.exists("./Matra.png") else None,
    show_error=True
)
