import base64
import os
import sys

# Força o Python a enviar logs em tempo real para o Render
sys.stdout.reconfigure(line_buffering=True)

print("=== [JADE AI AGENT] INICIANDO SERVIÇO ===", flush=True)

import gradio as gr
from langchain_groq import ChatGroq

# Função para converter a imagem local em formato que o navegador lê em qualquer lugar
def carregar_logo_base64():
    caminhos = ["jade/jade.logo.png", "jade.logo.png"]
    for caminho in caminhos:
        if os.path.exists(caminho):
            with open(caminho, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f'<img src="data:image/png;base64,{encoded}" style="height: 1em; vertical-align: -0.15em; display: inline-block; margin-right: 6px;">'
    return "💎 "

logo_html = carregar_logo_base64()

def responder_jade(mensagem, historico):
    try:
        if isinstance(mensagem, dict):
            texto = mensagem.get("text", "")
        else:
            texto = str(mensagem) if mensagem else ""

        texto = texto.strip()
        if not texto:
            return ""

        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if not api_key:
            return "❌ Erro: A variável GROQ_API_KEY não está configurada no Render."

        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="openai/gpt-oss-120b",
            temperature=0.2
        )

        resposta = llm.invoke(texto)

        if hasattr(resposta, "content"):
            return resposta.content
        return str(resposta)

    except Exception as e:
        return f"❌ Erro na API Groq ({type(e).__name__}): {str(e)}"

# Interface Visual
theme = gr.themes.Soft(
    primary_hue="emerald",
    secondary_hue="teal",
    neutral_hue="slate"
)

with gr.Blocks(theme=theme, title="JADE AI Agent") as demo:
    gr.Markdown(
        f"""
        # {logo_html}JADE AI Agent
        ### Assistente Virtual Inteligente
        """
    )
    gr.ChatInterface(fn=responder_jade)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Servidor rodando na porta {port}...", flush=True)
    demo.launch(server_name="0.0.0.0", server_port=port)
