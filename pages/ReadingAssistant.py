import streamlit as st
import streamlit.components.v1 as components
from deep_translator import GoogleTranslator

from utils.shared import render_footer      # pip install -U deep-translator

# Sidebar Instructions
st.sidebar.header("About")
st.sidebar.markdown("""
- **Reading Mode**: Clean layout for better focus.
- **Word Highlighting**: Tracks precisely which word is being spoken.
- **Controls**: Adjust playback speed and toggle Start , Stop.
- **Browser Powered**: Uses native Web Speech API for low latency.
""")

def show():
    st.title("📖 Reading Assistant")
    st.subheader("A Translation and Reading assistant that highlights words as they are read aloud. ")
    st.set_page_config(page_title="Reading Assistant", initial_sidebar_state="collapsed",layout="wide")

    ## Session States ##
    if 'translate' not in st.session_state:
        st.session_state.translate=[]  # For Translation

    if 'get_value' not in st.session_state:
        st.session_state.get_value=''  # For Uploaded File

    if 'widget' not in st.session_state:
        st.session_state.widget=''     # For clearing text area


    ### Functions ###
    def translator():  # Translate input text area
        try:
            translation=GoogleTranslator(source=st.session_state.input.lower(),
                                            target=st.session_state.output.lower()).translate(text_area)
            if not st.session_state.translate:   # Add translation if list st.session_state.translate is empty, else clear and add new one
                st.session_state.translate.append(translation)
            else:
                st.session_state.translate.clear()
                st.session_state.translate.append(translation)
        except:  # Handling LanguageNotSupportEdexception error
            st.toast(body=f'The text \"{text_area}\" is not in {st.session_state.input}!',icon='❌')

    def replace_file_text():  # Replace text area value with Uploaded File value
        st.session_state.get_value=text_area.replace(text_area,file_uploader.read().decode('utf-8'))
        st.toast(body='Press \"X\" to confirm!',icon='⚙️')

    def clear_text():
        st.session_state.pop('get_value')  # Clear content from uploaded file
        st.session_state.widget=''         # Clear content from keyboard

    def swap_textarea():
        st.session_state.input=keep_output  # Change Input language to Output language
        st.session_state.output=keep_input  # Change Output language to Input language


    ## Languages ##
    languages=[
        "English","Swedish"
    ]

    col1,col2,col3,col4,col5,col6,col7=st.columns([2,2,1,2,1,3,3]) # on same line
    with col1:   # Clear input text area Button
    # Select input language
        target_input=st.selectbox(label='**Input Language**',
                            options=languages,
                            index=languages.index('English'),
                            help='Select an input language',
                            key='input'
                            )
    with col2:   # Translate input text area Button
        # Select output language
        target_output=st.selectbox(label='**Output Language**',
                            options=languages,
                            index=languages.index('Swedish'),
                            help='Select an output language',
                            key='output')
    with col3:   # Clear input text area Button
        clear_button=st.button(label='Clear',type='secondary',on_click=clear_text)
    with col4:   # Translate input text area Button
        translate_button=st.button(label='Translate',type='secondary')
    with col5:   # Swap input & output Value
        swap_value=st.button(label='🔁',on_click=swap_textarea,type='secondary')
    with col6:   # File uploader Button
        file_uploader=st.file_uploader(label='**Upload a TXT File**',type=['txt'])
    with col7:    # Speak Button
        st.audio_input("🔊 Speak",disabled=True)


    # Input text area
    text_area=st.text_area(label='Input',value=st.session_state.get_value,
                            height=50,
                            placeholder='Enter text to translate or upload a TXT file! ',
                            help='Enter the text need to be translated!',key='widget',label_visibility='collapsed')


    if file_uploader is not None:
        replace_file_text()



    keep_input=st.session_state.input    # Keep st.session_state.input Value
    keep_output=st.session_state.output  # Keep st.session_state.output Value


    if translate_button:  # Translate Button system
        translator()  # Call function to translate input text area

    # Translation text area
    # st.html(f"""
    #         <textarea class='disable_textarea' name='Translation' placeholder='Translation'>{"".join(st.session_state.translate)}</textarea>""")

    user_text = "".join(st.session_state.translate)

    if user_text.strip() == "":
        st.warning("Please enter some text.")
        return

    # The CSS and JavaScript logic for TTS and Highlighting
    # We embed this in a single HTML component to keep word-tracking logic local to the DOM
    html_code = f"""
    <div id="reading-panel" style="
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        font-size: 1.25rem;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
        color: #333;
        margin-bottom: 20px;
    ">
        <div id="text-container"></div>
    </div>

    <div style="margin-bottom: 20px;">
        <button id="play-btn" style="
            padding: 10px 20px;
            font-size: 1rem;
            background-color: #60A7EF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        ">▶ Play / Stop</button>
        
        <label style="margin-left: 15px;">Speed: 
            <select id="rate" style="padding: 5px;">
                <option value="0.8">0.8x</option>
                <option value="1" selected>1x</option>
                <option value="1.2">1.2x</option>
                <option value="1.5">1.5x</option>
            </select>
        </label>
    </div>

    <style>
        .word {{
            display: inline-block;
            margin-right: 4px;
            padding: 2px 2px;
            border-radius: 3px;
            transition: background-color 0.1s;
        }}
        .highlight {{
            background-color: #ffeb3b;
            font-weight: bold;
            transform: scale(1.1);
        }}
    </style>

    <script>
        const text = `{user_text.replace('`', '\\`').replace('$', '\\$')}`;
        const container = document.getElementById('text-container');
        const playBtn = document.getElementById('play-btn');
        const rateSelect = document.getElementById('rate');
        
        // Split text into words and wrap in spans
        const words = text.split(/\s+/);
        container.innerHTML = words.map((word, index) => 
            `<span class="word" id="word-${{index}}">${{word}}</span>`
        ).join(' ');

        let synth = window.speechSynthesis;
        let utterance = null;
        let isPlaying = false;

        playBtn.onclick = () => {{
            if (isPlaying) {{
                synth.cancel();
                isPlaying = false;
                removeHighlights();
                return;
            }}

            utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = parseFloat(rateSelect.value);
            
            // This is the key event for word highlighting
            utterance.onboundary = (event) => {{
                if (event.name === 'word') {{
                    const charIndex = event.charIndex;
                    highlightWordByCharIndex(charIndex);
                }}
            }};

            utterance.onend = () => {{
                isPlaying = false;
                removeHighlights();
            }};

            isPlaying = true;
            synth.speak(utterance);
        }};

        function highlightWordByCharIndex(charIndex) {{
            removeHighlights();
            
            // Find which word corresponds to this character index
            let currentLength = 0;
            for (let i = 0; i < words.length; i++) {{
                // +1 to account for the space
                if (charIndex >= currentLength && charIndex < currentLength + words[i].length + 1) {{
                    const el = document.getElementById(`word-${{i}}`);
                    if (el) {{
                        el.classList.add('highlight');
                        el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    }}
                    break;
                }}
                currentLength += words[i].length + 1;
            }}
        }}

        function removeHighlights() {{
            document.querySelectorAll('.word').forEach(el => el.classList.remove('highlight'));
        }}
    </script>
    """

    # Display the reading panel
    components.html(html_code, height=500, scrolling=True)

render_footer(True)

if __name__ == "__main__":
    show()