import os
import sys

# Força o Python a enviar logs em tempo real para o Render
sys.stdout.reconfigure(line_buffering=True)

print("=== [JADE AI AGENT] INICIANDO SERVIÇO ===", flush=True)

import gradio as gr
from langchain_groq import ChatGroq

def responder_jade(mensagem, historico):
    try:
        # Tratamento de formato da mensagem do Gradio
        if isinstance(mensagem, dict):
            texto = mensagem.get("text", "")
        else:
            texto = str(mensagem) if mensagem else ""

        texto = texto.strip()
        if not texto:
            return ""

        # Verificação da Chave de API
        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if not api_key:
            return "❌ Erro: A variável GROQ_API_KEY não está configurada no Render."

        # Modelo oficial, ATIVO e GRATUITO na Groq
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
    gr.Markdown("# 💎 JADE AI Agent\n### Assistente Virtual Inteligente")
    gr.ChatInterface(fn=responder_jade)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Servidor rodando na porta {port}...", flush=True)
    demo.launch(server_name="0.0.0.0", server_port=port)
