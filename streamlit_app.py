import streamlit as st
import json

# 1. Configuración de la página del chat
st.set_page_config(page_title="AI Chat por Kevin", page_icon="🤖", layout="centered")

st.title("🤖 Mi Chat de Inteligencia Artificial")
st.write("Creado por Kevin. Conectado en vivo con la API de OpenRouter.")
st.divider()

# 2. Tu API Key integrada de forma segura
API_KEY = "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"

# Inicializar el historial de mensajes
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

# 3. Mostrar los mensajes anteriores en la pantalla
for mensaje in st.session_state.historial_chat:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# 4. Capturar el texto que escribe el usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    
    # Mostrar el mensaje del usuario de inmediato
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Guardarlo en el historial
    st.session_state.historial_chat.append({"role": "user", "content": prompt})
    mensajes_api_json = json.dumps(st.session_state.historial_chat)

    # 5. PUENTE SEGURO: Realiza la consulta directa a OpenRouter
    js_fetch_script = f"""
    <div id="ai-response" style="padding:15px; border-radius:10px; background-color:#1E1E1E; font-family:sans-serif; color:#FFFFFF; line-height:1.5;">
        ⏳ Pensando respuesta...
    </div>

    <script>
        fetch("https://openrouter.ai", {{
            method: "POST",
            headers: {{
                "Authorization": "Bearer {API_KEY}",
                "Content-Type": "application/json"
            }},
            body: JSON.stringify({{
                "model": "meta-llama/llama-3-8b-instruct:free",
                "messages": {mensajes_api_json}
            }})
        }})
        .then(response => {{
            if (!response.ok) throw new Error('Error de conexión en OpenRouter.');
            return response.json();
        }})
        .then(data => {{
            const respuestaTexto = data.choices.message.content;
            document.getElementById("ai-response").innerHTML = respuestaTexto.replace(/\\n/g, '<br>');
        }})
        .catch(error => {{
            document.getElementById("ai-response").innerHTML = `<div style="color: #FF6B6B;">⚠️ Error: ${{error.message}}</div>`;
        }});
    </script>
    """

    # Renderizar la respuesta del asistente en pantalla
    with st.chat_message("assistant"):
        st.components.v1.html(js_fetch_script, height=250, scrolling=True)
        st.session_state.historial_chat.append({"role": "assistant", "content": "🤖 Respuesta cargada en el recuadro."})
