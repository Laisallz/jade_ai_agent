# 🤖 JADE AI Agent — Assistente Corporativo RAG
[https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
O **JADE AI Agent** é um assistente corporativo baseado em **Retrieval-Augmented Generation (RAG)** de alta precisão, desenvolvido para responder a dúvidas de colaboradores com base na base de conhecimento interna da empresa, reduzindo alucinações e citando as fontes exatas das informações.

---

## 🌐 Teste a Interface Ao Vivo

Você pode testar a interface do assistente rodando 24/7 através do link:  
👉 **[Acessar JADE AI Agent no Hugging Face Spaces](https://huggingface.co/spaces/laisalisanezanatta/jade-ai-agent)**

---

## 🚀 Funcionalidades Principais

- 📚 **Processamento Multi-documento:** Suporte para múltiplos arquivos de texto e documentações corporativas.
- ⚡ **Busca Semântica & Re-ranking:** Combinação de embeddings vetoriais com **Cross-Encoder** (`mmarco-mMiniLMv2`) para garantir máxima relevância dos documentos recuperados.
- 🧠 **Memória e Contextualização:** Capacidade de manter o histórico do diálogo e reformular perguntas mantendo o contexto da conversa.
- 📊 **Suíte de Avaliação RAG (LLM-as-a-Judge):** Testes automatizados para mensurar *Fidelidade* (ausência de alucinações) e *Relevância das Respostas*.
- 🌐 **Interface Gráfica Interativa:** Interface web desenvolvida com Gradio.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **LLM Engine:** Groq API (`llama-3.1-8b-instant`)
- **Orquestração:** LangChain
- **Banco Vetorial:** ChromaDB
- **Embeddings & Re-ranking:** Hugging Face (`sentence-transformers/all-MiniLM-L6-v2` e `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`)
- **Interface:** Gradio

---

## 📊 Métricas de Avaliação RAG

| Métrica | Descrição | Meta do Sistema |
| :--- | :--- | :---: |
| **Fidelidade (Faithfulness)** | Avalia se a resposta contém apenas fatos presentes no contexto fornecido. | > 90% |
| **Relevância (Answer Relevance)** | Mede o quão diretamente a resposta atende à dúvida do usuário. | > 90% |

---

## ✒️ Autora

Desenvolvido por **Laisa**.
