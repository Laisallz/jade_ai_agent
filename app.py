import os
import sys

# Forçar o Python a enviar logs imediatamente para o Render
sys.stdout.reconfigure(line_buffering=True)

print("=== [JADE] INICIANDO APLICAÇÃO ===", flush=True)

# 1. Leitura segura das Variáveis de Ambiente
groq_api_key = os.environ.get("GROQ_API_KEY", "").strip()

if not groq_api_key:
    print("⚠️ AVISO CRÍTICO: GROQ_API_KEY não foi encontrada!", flush=True)
else:
    print("✅ GROQ_API_KEY encontrada com sucesso.", flush=True)

# 2. Imports Protegidos
try:
    import gradio as gr
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser
    print("✅ Todas as bibliotecas foram importadas com sucesso.", flush=True)
except Exception as e:
    print(f"❌ ERRO GRAVE NA IMPORTAÇÃO: {e}", flush=True)
    sys.exit(1)

# 3. Inicialização do LLM
llm = None
if groq_api_key:
    try:
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.2
        )
        print("✅ Modelo Llama-3.3-70b conectado com sucesso.", flush=True)
    except Exception as e:
        print(f"❌ ERRO ao conectar com a Groq: {e}", flush=True)

# 4. Função de Resposta
def responder_jade(mensagem, historico):
    if not mensagem or not mensagem.strip():
        return ""
    
    try:
        resposta = llm.invoke(mensagem)
        return resposta.content
    except Exception as e:
        return f"Ops! Ocorreu um erro ao consultar o modelo: {str(e)}"

# 5. Interface Gráfica Gradio
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

# 6. Boot do Servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Subindo servidor web na porta {port}...", flush=True)
    demo.launch(server_name="0.0.0.0", server_port=port)
