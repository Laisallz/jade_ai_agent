# 💎 JADE AI Agent

**Aplicação Online:** [Acessar a JADE no Render]https://jade-ai-agent-1-scuv.onrender.com

Assistente Virtual Inteligente baseada em Inteligência Artificial, construída com arquitetura RAG (Retrieval-Augmented Generation), LangChain Expression Language (LCEL) e implantada de forma leve no Render.com.

---

## 📝 1. Descrição Geral do Projeto

A **JADE AI Agent** é uma assistente virtual conversacional projetada para responder a dúvidas de usuários de forma clara, contextualizada e amigável. O projeto combina o poder do modelo **Llama 3.3 (70B)** via API da **Groq** com busca vetorial de documentos em tempo real.

O projeto foi totalmente otimizado para execução contínua em ambientes de recursos reduzidos (como a camada gratuita do Render.com com limite de **512 MB de RAM**), garantindo inicialização rápida, baixa pegada de memória e respostas em tempo real.

---

## 🏗️ 2. Arquitetura da Solução

A arquitetura da JADE utiliza uma abordagem moderna focada em eficiência e performance:

* **Interface Web (Gradio):** Recebe as perguntas do usuário e exibe as respostas do chat em tempo real.
* **LangChain LCEL (Pipeline):** Orquestra o fluxo entre o modelo de linguagem e o banco de dados de forma declarativa.
* **Groq API (Llama-3.3-70b):** Executa o processamento do LLM em nuvem com alta velocidade.
* **Chroma DB + FastEmbed (RAG):** Armazena os documentos vetoriais e realiza buscas de similaridade utilizando uma biblioteca de embeddings leve otimizada para C++.

### Principais Decisões Arquiteturais:
* **Pipeline RAG via LCEL (LangChain Expression Language):** Garante código limpo, declarativo e compatível com as versões mais recentes do LangChain.
* **Lazy Loading do Banco Vetorial:** O carregamento dos embeddings e da base vetorial ocorre apenas sob demanda na primeira pergunta do usuário, garantindo a abertura rápida da porta HTTP (`PORT 10000`).
* **Embeddings Ultraleves (FastEmbed):** Substituição de bibliotecas nativas em PyTorch por execução otimizada em ONNX C++, reduzindo o consumo de RAM de mais de 500MB para apenas ~80MB.

---

## 🛠️ 3. Tecnologias e Ferramentas Utilizadas

| Categoria | Tecnologia / Biblioteca | Descrição |
| :--- | :--- | :--- |
| **Linguagem** | Python 3.10+ | Linguagem base do projeto |
| **Interface Web** | Gradio | Interface de chat interativa e elegante |
| **Orquestração AI** | LangChain / LangChain Core | Framework para encadeamento do RAG e prompts |
| **LLM (Modelo)** | Groq API (`llama-3.3-70b-versatile`) | Processamento de linguagem natural de alta velocidade |
| **Embeddings** | FastEmbed (`BAAI/bge-small-en-v1.5`) | Gerador de vetores leve e de baixa memória |
| **Banco Vetorial** | ChromaDB | Armazenamento e busca por similaridade de documentos |
| **Hospedagem** | Render.com | Nuvem para deploy do serviço web 24/7 |

--
<img width="1024" height="432" alt="image" src="https://github.com/user-attachments/assets/8f0df7e0-da34-40c4-b6c9-a8f15026a369" />
-
<p align="center">
  <img src="jade/Captura de tela 2026-08-19 092713.png" width="31%" />
  <img src="jade/Captura de tela 2026-08-19 093225.png" width="31%" />
  <img src="jade/nome_da_terceira_foto.png" width="31%" />
</p>




## 🚀 4. Instruções para Executar o Projeto

### 💻 Execução Local

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone [https://github.com/Laisallz/jade_ai_agent.git](https://github.com/Laisallz/jade_ai_agent.git)
   cd jade_ai_agent
