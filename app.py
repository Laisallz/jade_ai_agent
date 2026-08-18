import os
import gradio as gr
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Configurar LLM da Groq (Sem consumo pesado de RAM no startup)
groq_api_key = os.environ.get("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.2
)

# Variáveis para Lazy Loading do Banco Vetorial
retriever_instance = None
retriever_checked = False

def get_retriever():
    """Carrega o banco de dados somente quando o usuário fizer a 1ª pergunta"""
    global retriever_instance, retriever_checked
    if retriever_checked:
        return retriever_instance

    retriever_checked = True
    chroma_path = None
    if os.path.exists("./jade_chroma"):
        chroma_path = "./jade_chroma"
    elif os.path.exists("./chroma_db"):
        chroma_path = "./chroma_db"

    if chroma_path:
        try:
            from langchain_community.vectorstores import Chroma
            from langchain_community.embeddings import FastEmbedEmbeddings
            
            embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
            vectorstore = Chroma(
                persist_directory=chroma_path,
                embedding_function=embeddings
            )
            retriever_instance = vectorstore.as_retriever(search_kwargs={"k": 3})
            print("--- Banco Vetorial carregado sob demanda com sucesso! ---")
        except Exception as e:
            print(f"Erro ao carregar banco vetorial: {e}")
            retriever_instance = None
    return retriever_instance

# 2. Prompt Template da JADE
prompt_template = ChatPromptTemplate.from_template(
    "Você é a JADE, uma assistente virtual inteligente, prestativa e amigável. "
    "Responda à dúvida do usuário de forma clara, bem formatada e direta. "
    "Se houver contexto fornecido abaixo, use-o para fundamentar sua resposta.\n\n"
    "Contexto:\n{context}\n\n"
    "Pergunta: {question}"
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def responder_jade(mensagem, historico):
    if not mensagem or not mensagem.strip():
        return ""
    
    try:
        retriever = get_retriever()
        if retriever:
            rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt_template
                | llm
                | StrOutputParser()
            )
            return rag_chain.invoke(mensagem)
        else:
            resposta = llm.invoke(mensagem)
            return resposta.content
    except Exception as e:
        return f"Ops! Tive um problema ao processar sua pergunta: {str(e)}"

# 3. Design da Interface Web (Gradio)
theme = gr.themes.Soft(
    primary_hue="emerald",
    secondary_hue="teal",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui"]
)

custom_css = """
footer {visibility: hidden}
.gradio-container {max-width: 850px !important; margin: 0 auto !important;}
"""

with gr.Blocks(theme=theme, css=custom_css, title="JADE AI Agent") as demo:
    gr.Markdown(
        """
        # 💎 JADE AI Agent
        ### Bem-vinda ao seu assistente de inteligência artificial!
        *Faça perguntas sobre o seu projeto e documentos para obter respostas em tempo real.*
        """
    )

    gr.ChatInterface(
        fn=responder_jade,
        textbox=gr.Textbox(
            placeholder="Digite sua pergunta para a JADE...",
            container=False,
            scale=7
        ),
        examples=[
            "Qual é o objetivo principal do projeto?",
            "Me faça um resumo dos pontos mais importantes.",
            "Quais são as principais etapas de execução?"
        ],
        cache_examples=False,
        retry_btn="🔄 Tentar novamente",
        undo_btn="↩️ Desfazer",
        clear_btn="🗑️ Limpar conversa"
    )

# 4. Inicializar Servidor Instantaneamente
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)
