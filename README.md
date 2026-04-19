# 💫 Streamlit Apps and Tools Catalogue

This is Apps and Tools building series using Streamlit and AI.  
We’ll build a very simple chatbot using **Streamlit** + **OpenRouter**  + **Gemini AI**.

## 🌟 Features

- **Basic Chat GPT** - Works using OpenRouter and Google Gemini
- **Text Translation to Swedish and Reading Assist** - Highlights the words when reading 


## 🚀 Live Demo

Visit : [Site](https://myapps-catalogue.streamlit.app/)

## 📁 Project Structure
```apps-catalogue/
├── app.py              # Main entry point & Navigation
├── config.py           # Centralized data/page configuration
├── styles.css          # Custom CSS for cards and UI
├── pages/              # Individual page modules
│   ├── home.py         # Dashboard with cards
│   ├── chatbot.py      # Chat GPT Bot logic
│   ├── ReadingAssistant.py      # Chat GPT Bot logic
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## To Customize 
### How to Run and Scale
1. To run: Put all files in a folder and run streamlit run app.py.
2. To add a new page:
3. Create a new file in pages/ (e.g., pages/summarizer.py).
   Define a show() function in it (or just write regular Streamlit code).
   Add the page details to config.py.
4. To change styles: Edit styles.css without touching the Python logic.

## Improvments
1. support other AI providers 
2. Need to improve swedish pronunciation for voice
3. Handle voice to text translation
