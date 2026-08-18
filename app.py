import os
import sys

# Força o Python a enviar logs em tempo real para o Render
sys.stdout.reconfigure(line_buffering=True)

print("=== [JADE AI AGENT] INICIANDO SERVIÇO ===", flush=True)

import gradio as gr
from langchain_groq import ChatGroq

def responder_jade(mensagem, historico):
    if not mensagem or not mensagem.strip():
        return ""

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return "❌ Erro: GROQ_API_KEY não configurada nas variáveis do Render."

    # 1ª Tentativa: Modelo Llama 3.3 70B Versatile
    try:
        llm = ChatGroq(
            groq_api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )
        resposta = llm.invoke(mensagem)
        return resposta.content
    except Exception as erro_70b:
        print(f"⚠️ Modelo 70B indisponível ({erro_70b}). Redirecionando para o modelo 8B...", flush=True)
        
        # 2ª Tentativa (Fallback automático): Modelo Llama 3 8B
        try:
            llm = ChatGroq(
                groq_api_key=api_key,
                model="llama3-8b-8192",
                temperature=0.2
            )
            resposta = llm.invoke(mensagem)
            return resposta.content
        except Exception as erro_8b:
            return f"❌ Erro ao consultar a API da Groq: {str(erro_8b)}"

# Interface Visual do Gradio
theme = gr.themes.Soft(
    primary_hue="emerald",
    secondary_hue="teal",
    neutral_hue="slate"
)

with gr.Blocks(theme=theme, title="JADE AI Agent") as demo:
    gr.Markdown("# 💎 JADE AI Agent\n### Assistente Virtual Inteligente")
    gr.ChatInterface(fn=responder_jade)

# Execução na porta do Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Servidor pronto na porta {port}...", flush=True)
    demo.launch(server_name="0.0.0.0", server_port=port)
