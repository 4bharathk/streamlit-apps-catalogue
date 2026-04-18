import streamlit.components.v1 as components

def render_tts_reader(text):
    html_code = f"""
    <style>
        .word {{ padding: 2px; border-radius: 3px; font-family: sans-serif; font-size: 1.2rem; }}
        .active {{ background: #ffeb3b; font-weight: bold; }}
    </style>
    <div id="container" style="border:1px solid #ddd; padding:20px; border-radius:10px; background:#fafafa; line-height:1.8;">
        <div id="text-box"></div>
    </div>
    <button id="play" style="margin-top:15px; padding:10px 20px; background:#FF4B4B; color:white; border:none; border-radius:5px; cursor:pointer;">Play / Stop</button>
    
    <script>
        const text = `{text}`;
        const words = text.split(/\s+/);
        const box = document.getElementById('text-box');
        box.innerHTML = words.map((w, i) => `<span id="w-${{i}}" class="word">${{w}}</span>`).join(' ');

        let synth = window.speechSynthesis;
        let playing = false;

        document.getElementById('play').onclick = () => {{
            if (playing) {{ synth.cancel(); playing = false; return; }}
            let utt = new SpeechSynthesisUtterance(text);
            utt.onboundary = (e) => {{
                if (e.name === 'word') {{
                    document.querySelectorAll('.word').forEach(s => s.classList.remove('active'));
                    let charPos = 0;
                    for (let i = 0; i < words.length; i++) {{
                        if (e.charIndex >= charPos && e.charIndex < charPos + words[i].length + 1) {{
                            const el = document.getElementById('w-'+i);
                            el.classList.add('active');
                            el.scrollIntoView({{block:'center'}});
                            break;
                        }}
                        charPos += words[i].length + 1;
                    }}
                }}
            }};
            utt.onend = () => {{ playing = false; }};
            playing = true;
            synth.speak(utt);
        }};
    </script>
    """
    return components.html(html_code, height=400)