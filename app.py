import os
import gradio as gr
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Configurar Chave de API e Embeddings
groq_api_key = os.environ.get("GROQ_API_KEY")

# Modelo de embeddings para busca no banco vetorial
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Carregar o banco vetorial Chroma (se existir na pasta chroma_db)
if os.path.exists("./chroma_db"):
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
else:
    retriever = None

# Configurar o LLM da Groq
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.2
)

# Template de prompt com a personalidade da JADE
system_prompt = (
    "Você é a JADE, uma assistente virtual inteligente, prestativa e amigável. "
    "Responda à dúvida do usuário de forma clara, bem formatada e direta. "
    "Se houver contexto fornecido abaixo, use-o para fundamentar sua resposta.\n\n"
    "Contexto:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Criar a cadeia RAG
question_answer_chain = create_stuff_documents_chain(llm, prompt)

def responder_jade(mensagem, historico):
    if not mensagem.strip():
        return ""
    
    try:
        if retriever:
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            resposta = rag_chain.invoke({"input": mensagem})
            return resposta["answer"]
        else:
            # Resposta direta caso o banco vetorial não tenha sido carregado
            resposta = llm.invoke(mensagem)
            return resposta.content
    except Exception as e:
        return f"Ops! Tive um problema ao processar sua pergunta: {str(e)}"

# 2. Design da Interface Web (Gradio)
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

# 3. Execução configurada para a porta do Render.com
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    demo.launch(server_name="0.0.0.0", server_port=port)
  

    
