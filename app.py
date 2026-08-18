import os
import sys

# Força o Python a exibir os logs imediatamente no console do Render
sys.stdout.reconfigure(line_buffering=True)

print("=== [JADE AI AGENT] INICIANDO APLICAÇÃO ===", flush=True)

import gradio as gr
from langchain_groq import ChatGroq

def obter_llm(nome_modelo, api_key):
    """Cria a instância do LLM com o modelo solicitado."""
    return ChatGroq(
        groq_api_key=api_key,
        model=nome_modelo,
        temperature=0.2
    )

def responder_jade(mensagem, historico):
    if not mensagem or not mensagem.strip():
        return ""

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    
    if not api_key:
        return "❌ Erro: A variável GROQ_API_KEY não foi encontrada no ambiente do Render."

    # 1ª Tentativa: Usar o modelo Llama 3.3 70B
    try:
        llm = obter_llm("llama-3.3-70b-versatile", api_key)
        resposta = llm.invoke(mensagem)
        return resposta.content
    except Exception as erro_70b:
        print(f"⚠️ Modelo 70B indisponível ou inacessível ({erro_70b}). Ativando fallback 8B...", flush=True)

        # 2ª Tentativa (Fallback): Usar o modelo Llama 3 8B
        try:
            llm = obter_llm("llama3-8b-8192", api_key)
            resposta = llm.invoke(mensagem)
            return resposta.content
        except Exception as erro_8b:
            return f"❌ Erro de conexão com a API Groq: {str(erro_8b)}"

# Configuração Visual da Interface
theme = gr.themes.Soft(
    primary_hue="emerald",
    secondary_hue="teal",
    neutral_hue="slate"
)

with gr.Blocks(theme=theme, title="JADE AI Agent") as demo:
    gr.Markdown(
        """
        # 💎 JADE AI Agent
        ### Assistente Virtual Inteligente
        """
    )
    gr.ChatInterface(fn=responder_jade)

# Execução do Servidor
if __name__ == "__main__":
    # O Render define a porta pela variável PORT automaticamente
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Subindo servidor web na porta {port}...", flush=True)
    
    demo.launch(server_name="0.0.0.0", server_port=port)
