import os
import sys

sys.stdout.reconfigure(line_buffering=True)

print("=== [JADE] INICIANDO APLICAÇÃO ===", flush=True)

# 1. Leitura das Variáveis
groq_api_key = os.environ.get("GROQ_API_KEY", "").strip()

# 2. Imports
try:
    import gradio as gr
    from langchain_groq import ChatGroq
    print("✅ Bibliotecas carregadas.", flush=True)
except Exception as e:
    print(f"❌ Erro de Importação: {e}", flush=True)
    sys.exit(1)

# 3. Inicialização do LLM (Usando o parâmetro 'model' atualizado)
llm = None
if groq_api_key:
    try:
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model="llama-3.3-70b-versatile",  # Usa 'model' em vez de 'model_name'
            temperature=0.2
        )
        print("✅ Modelo configurado.", flush=True)
    except Exception as e:
        print(f"❌ Erro na configuração do LLM: {e}", flush=True)

# 4. Função de Resposta com Fallback de Segurança
def responder_jade(mensagem, historico):
    if not mensagem or not mensagem.strip():
        return ""
    
    if not llm:
        return "Erro: GROQ_API_KEY não encontrada nas variáveis do Render."

    try:
        resposta = llm.invoke(mensagem)
        return resposta.content
    except Exception as e:
        # Exibe o erro legível
        return f"Ops! Erro de conexão com a API Groq: {str(e)}"

# 5. Interface
theme = gr.themes.Soft(primary_hue="emerald", secondary_hue="teal", neutral_hue="slate")

with gr.Blocks(theme=theme, title="JADE AI Agent") as demo:
    gr.Markdown("# 💎 JADE AI Agent\n### Assistente Virtual Inteligente")
    gr.ChatInterface(fn=responder_jade)

# 6. Servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)
