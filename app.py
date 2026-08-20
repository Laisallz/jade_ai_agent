import base64
import os
import sys

# Força o Python a enviar logs em tempo real para o Render
sys.stdout.reconfigure(line_buffering=True)

print("=== [JADE AI AGENT] INICIANDO SERVIÇO ===", flush=True)

import gradio as gr
from langchain_groq import ChatGroq

def carregar_logo_base64():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_novo = os.path.join(base_dir, "jade", "logo1.png.jpeg")
    
    candidatos = [
        caminho_novo,
        os.path.join(base_dir, "jade", "jade.logo.png"),
    ]
    
    for caminho in candidatos:
        if os.path.exists(caminho):
            print(f"✅ Logo encontrada com sucesso em: {caminho}", flush=True)
            extensao = "jpeg" if caminho.lower().endswith((".jpg", ".jpeg")) else "png"
            with open(caminho, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f'<img src="data:image/{extensao};base64,{encoded}" style="height: 1em; vertical-align: -0.15em; display: inline-block; margin-right: 6px;">'
    
    print(f"⚠️ Imagem não encontrada em {caminho_novo}. Exibindo emoji fallback.", flush=True)
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
    # Cabeçalho com a logo
    gr.Markdown(
        f"""
        # {logo_html}JADE AI Agent
        ### Assistente Virtual Inteligente
        """
    )
    
    # Interface do Chat
    gr.ChatInterface(fn=responder_jade)

    # Seção de FAQ (Accordion Principal)
    with gr.Accordion("❓ Perguntas Frequentes (FAQ)", open=False):
        
        with gr.Accordion("O que é o JADE AI Agent?", open=False):
            gr.Markdown("O JADE é um assistente virtual inteligente projetado para responder dúvidas e auxiliar no processamento de informações.")

        with gr.Accordion("Como o assistente gera as respostas?", open=False):
            gr.Markdown("Ele utiliza modelos de linguagem avançados (LLMs) processados através da infraestrutura de alta velocidade da Groq.")

        with gr.Accordion("O serviço fica disponível continuamente?", open=False):
            gr.Markdown("Sim, a aplicação fica hospedada online e pronta para responder a qualquer momento.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Servidor rodando na porta {port}...", flush=True)
    demo.launch(server_name="0.0.0.0", server_port=port)
