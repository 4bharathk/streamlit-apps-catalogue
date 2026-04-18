# config.py
# Define your pages here. To add a new page, just add an entry to this list and create the corresponding file in pages/.
PAGE_CONFIG = [
    {
        "id": "Home",
        "title": "Home",
        "icon": "🏠",
        "description": "Main menu",
        "script_path": "pages/home.py"
    },
    {
        "id": "chatbot",
        "title": "ChatBot",
        "icon": "💬",
        "description": "A demo of a chatbot application using LLMs.",
        "script_path": "pages/chatbot.py"
    },
    {
        "id": "reading",
        "title": "Reading Assistant",
        "icon": "📖",
        "description": "Translation and Reading assistant application demo",
        "script_path": "pages/ReadingAssistant.py"
    },

]