import os
import gradio as gr
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Recuperar a chave de API das configurações de Secret do Hugging Face / Ambiente
groq_api_key = os.environ.get("GROQ_API_KEY")

# 2. Inicializar o LLM (Groq)
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant",
    temperature=0.2
)

# 3. Carregar modelo de Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Carregar o banco vetorial Chroma local (se existir a pasta jade_chroma)
if os.path.exists("./jade_chroma"):
    vectorstore = Chroma(
        persist_directory="./jade_chroma",
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
else:
    retriever = None

# 5. Definir o Prompt do RAG
system_prompt = (
    "Você é o JADE AI Agent, um assistente corporativo prestativo e preciso.\n"
    "Responda à pergunta do usuário utilizando APENAS o contexto fornecido abaixo.\n"
    "Se você não souber a resposta ou ela não estiver no contexto, diga claramente que não possui essa informação.\n\n"
    "Contexto:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 6. Função de resposta para o Gradio
def respond(message, history):
    if not groq_api_key:
        return "⚠️ Erro: A chave GROQ_API_KEY não foi configurada nos Secrets do Hugging Face."
    
    if retriever is None:
        return "⚠️ Base de conhecimento (ChromaDB) não foi encontrada na raiz do projeto."
    
    try:
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        response = rag_chain.invoke({"input": message})
        return response["answer"]
    except Exception as e:
        return f"Ocorreu um erro ao processar sua pergunta: {str(e)}"

# 7. Criar a interface do Gradio
demo = gr.ChatInterface(
    fn=respond,
    title="🤖 JADE AI Agent — Assistente Corporativo RAG",
    description="Faça perguntas sobre a base de conhecimento interna da empresa.",
    examples=["O que é o JADE AI Agent?", "Quais são as principais funcionalidades?"],
    theme="soft"
)

if __name__ == "__main__":
    demo.launch()
