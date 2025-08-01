# Matra ✨

<p align="center">
  <img src="https://i.ibb.co/VW0H6nM5/Matra.png" alt="Matra Banner" width="400" height="800"/>
</p>

**Mathematical Animation Generator**

Matra is an AI-powered tool that generates animated math visualizations from natural language prompts using the Manim engine. It's like having your own personal animation studio for math content creators, educators, and learners.

---

## 🔧 Features

* ✨ **Natural Language to Manim Code**: Just describe a concept like "Pythagorean theorem" or "visualize sine wave" and Matra generates the Manim code and animation.
* ▶️ **In-browser Playback**: Watch the animation immediately after generation.
* 🔐 **Clean, Minimal UI**: Built with Gradio and custom CSS for a delightful experience.
* 🕹️ **Predefined Suggestions**: Clickable chips like:

  * Einstein's E=mc²
  * Sine wave animation
  * Derivative visualization
  * Electromagnetic wave

---

## 🚀 Live Demo

Try it now: [https://matra.dev](https://matra.dev)

---

## 💡 How It Works

1. **You Describe** a concept in simple English
2. **Matra Prompts an LLM** (LLaMA 4 Maverick) to generate Manim code
3. **Manim CLI Renders** the animation on the backend
4. **Gradio Interface** shows the code and plays the video

---

## 🚧 Installation

### Requirements

* Python 3.10+
* Manim CE
* FFmpeg

### Backend Setup

```bash
git clone https://github.com/vaishakh3/matra.git
cd matra
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file with:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Run the App

```bash
python matra.py
```

---

## 🛋️ Tech Stack

| Layer      | Stack                                        |
| ---------- | -------------------------------------------- |
| UI         | Gradio + TailwindCSS-style CSS               |
| AI         | Groq + LLaMA 4 (via `groq` Python SDK)       |
| Rendering  | [Manim](https://www.manim.community/)        |
| Deployment | Render 

---

## 🚫 Limitations

* Generated Manim code is not always perfect (LLM hallucination)
* No editing interface for tweaking animations yet
* GPU required for faster rendering

---

## 🤝 Contributing

Pull requests welcome ❤️

1. Fork the repo
2. Create a branch
3. Make your changes
4. Submit a PR

Or file an issue for bugs/feature requests!

---

## 🌐 Links

* [Matra.dev](https://matra.dev)
* [Manim Documentation](https://docs.manim.community/)
* [Groq LLM](https://groq.com)

---

## 👤 Author

Built by [Vaishakh Suresh](https://linkedin.com/in/vaishakhsuresh)

---

## ✉️ License

This project is licensed under the MIT License.
