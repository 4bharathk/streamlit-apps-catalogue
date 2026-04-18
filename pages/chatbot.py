import streamlit as st

from utils.shared import render_footer

from dotenv import load_dotenv
load_dotenv()

import os

from openai import OpenAI

from google import genai
from google.genai import types



def show():
    st.title("💬 ChatBot")

    # --- Sidebar Config ---
    with st.sidebar:

        API_KEY = st.text_input("API Key *",
                                       placeholder="your OpenAI API key (sk-...)",
                                       help="You can get your API key from https://platform.openai.com/account/api-keys.",
                                       type="password", key="sidebar_api_key_input")

        st.header("⚙️ LLM Model & Parameters")
        provider = st.selectbox("Provider", ["OpenAI", "Gemini"])
        llm_model = st.selectbox('LLM Model', ["openrouter/free", "openrouter/elephant-alpha","gemini-2.5-flash"], help="Select the language model you want to use for generating responses.")
        temp = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01,help="Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")
        #top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
        max_length = st.slider('Max_Tokens', min_value=64, max_value=200, value=128, step=8, help="The maximum number of tokens to generate in the response. Adjust based on your needs and model limits.")

    

    # Configure the Gemini API
    #API_KEY = os.getenv("GEMINI_API_KEY")
    #API_KEY = os.getenv("OPENROUTER_API_KEY")

    def display_messages():
        """Display all messages in the chat history"""
        for msg in st.session_state.messages:
            author = "user" if msg["role"] == "user" else "assistant"
            with st.chat_message(author):
                st.write(msg["content"])

    def friendly_wrap(raw_text):
        """Add a friendly tone to AI responses"""
        return (
            f"{raw_text.strip()}\n\n"
            "Would you like me to elaborate on any part of this, or do you have other questions?"
        )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Hi! I'm AI Smart Assitant ,  How can I help you today?"
            }
        ]
        st.session_state.openai_total_tokens = 0
        st.session_state.gemini_total_tokens = 0

    # Display existing messages
    display_messages()

    # Handle new user input
    prompt = st.chat_input("Ask anything ...")
    
    if prompt :
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Show user message
        with st.chat_message("user"):
            st.write(prompt)

        # Show thinking indicator while processing
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.write("🤔 Thinking...")

            try:
                full_response = ""

                if not API_KEY:
                    full_response = "❌ Error: Please enter an API key in the sidebar."
                    
                elif provider == "OpenAI":
                    client = OpenAI(
                        base_url="https://openrouter.ai/api/v1",
                        api_key = API_KEY)

                    response = client.chat.completions.create(model=llm_model, messages=st.session_state.messages)
                    
                     # Extract the assistant message with reasoning_details
                    full_response = response.choices[0].message.content
                    st.session_state.openai_total_tokens += response.usage.prompt_tokens 

                elif provider == "Gemini":
                    client = genai.Client(api_key=API_KEY)
                    system_instruction = "You are a Smart AI assistant."
                    response = client.models.generate_content(
                        model=llm_model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                                #   thinking_config=types.ThinkingConfig(
                                #         thinking_budget=0 #disable the thinking by setting 
                                #   ),
                            system_instruction=system_instruction,
                            temperature=temp,
                            max_output_tokens=max_length,
                        ))
                    full_response = response.text
                    st.session_state.gemini_total_tokens += response.usage_metadata.prompt_token_count

                # Extract response text   
                friendly_answer = friendly_wrap(full_response)
                
            except Exception as e:
                friendly_answer = f"I'm sorry, ⚠️ API Error: {e}. Please try asking your question again."

            # Replace thinking indicator with actual response
            placeholder.write(friendly_answer)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": friendly_answer})

            # Refresh the page to show updated chat

    #st.rerun()

    st.write(f"Tokens used in this session: OpenAI : :red[{st.session_state.openai_total_tokens}] , Gemini : :red[{st.session_state.gemini_total_tokens}] ")
  
    render_footer(True)

if __name__ == "__main__":
    show()