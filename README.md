💎 JADE AI Agent
Assistente Virtual Inteligente baseada em Inteligência Artificial, construída com arquitetura RAG (Retrieval-Augmented Generation), LangChain Expression Language (LCEL) e implantada de forma leve no Render.com.

📝 1. Descrição Geral do Projeto
A JADE AI Agent é uma assistente virtual conversacional projetada para responder a dúvidas de usuários de forma clara, contextualizada e amigável. O projeto combina o poder do modelo Llama 3.3 (70B) via API da Groq com busca vetorial de documentos em tempo real.

O projeto foi totalmente otimizado para execução contínua em ambientes de recursos reduzidos (como a camada gratuita do Render.com com limite de 512 MB de RAM), garantindo inicialização rápida, baixa pegada de memória e respostas em tempo real.

🏗️ 2. Arquitetura da Solução
A arquitetura da JADE utiliza uma abordagem moderna focada em eficiência e performance:

Interface Web (Gradio): Recebe as perguntas do usuário e exibe as respostas do chat em tempo real.

LangChain LCEL (Pipeline): Orquestra o fluxo entre o modelo de linguagem e o banco de dados de forma declarativa.

Groq API (Llama-3.3-70b): Executa o processamento do LLM em nuvem com alta velocidade.

Chroma DB + FastEmbed (RAG): Armazena os documentos vetoriais e realiza buscas de similaridade utilizando uma biblioteca de embeddings leve otimizada para C++.

Principais Decisões Arquiteturais:
Pipeline RAG via LCEL (LangChain Expression Language): Garante código limpo, declarativo e compatível com as versões mais recentes do LangChain.

Lazy Loading do Banco Vetorial: O carregamento dos embeddings e da base vetorial ocorre apenas sob demanda na primeira pergunta do usuário, garantindo a abertura rápida da porta HTTP (PORT 10000).

Embeddings Ultraleves (FastEmbed): Substituição de bibliotecas nativas em PyTorch por execução otimizada em ONNX C++, reduzindo o consumo de RAM de mais de 500MB para apenas ~80MB.

🛠️ 3. Tecnologias e Ferramentas Utilizadas
Categoria	Tecnologia / Biblioteca	Descrição
Linguagem	Python 3.10+	Linguagem base do projeto
Interface Web	Gradio	Interface de chat interativa e elegante
Orquestração AI	LangChain / LangChain Core	Framework para encadeamento do RAG e prompts
LLM (Modelo)	Groq API (llama-3.3-70b-versatile)	Processamento de linguagem natural de alta velocidade
Embeddings	FastEmbed (BAAI/bge-small-en-v1.5)	Gerador de vetores leve e de baixa memória
Banco Vetorial	ChromaDB	Armazenamento e busca por similaridade de documentos
Hospedagem	Render.com	Nuvem para deploy do serviço web 24/7
🚀 4. Instruções para Executar o Projeto
💻 Execução Local
Clone o repositório e acesse a pasta:

git clone https://github.com/Laisallz/jade_ai_agent.git

cd jade_ai_agent

Crie e ative um ambiente virtual (opcional):

python -m venv venv

source venv/bin/activate (Linux/Mac) ou venv\Scripts\activate (Windows)

Instale as dependências:

pip install -r requirements.txt

Configure sua chave da API Groq:

Linux/Mac: export GROQ_API_KEY="sua_chave_aqui"

Windows (CMD): set GROQ_API_KEY=sua_chave_aqui

Windows (PowerShell): $env:GROQ_API_KEY="sua_chave_aqui"

Inicie a aplicação:

python app.py

Acesse a interface no seu navegador em http://localhost:10000.

☁️ Implantação no Render.com
Crie um Web Service no Render.com e conecte este repositório do GitHub.

Configure os parâmetros do serviço:

Runtime: Python 3

Build Command: pip install -r requirements.txt

Start Command: python app.py

Em Environment Variables, adicione a chave:

Key: GROQ_API_KEY

Value: (Sua chave gerada no painel da Groq)

Clique em Create Web Service.

❓ 5. Exemplos de Perguntas que o Agente Responde
Perguntas de Visão Geral:

"Qual é o objetivo principal do projeto JADE?"

"Quem é você e como pode me ajudar?"

Perguntas Técnicas / Documentação:

"Quais são as principais etapas de execução da aplicação?"

"Como a arquitetura RAG foi otimizada para limites de memória?"

Dúvidas Gerais e Suporte:

"Me faça um resumo dos pontos mais importantes do projeto."

💬 6. Exemplos de Respostas Geradas pelo Agente
Exemplo 1:
Usuário: Quem é você?

JADE: Olá! Eu sou a JADE, uma assistente virtual inteligente, prestativa e amigável. Estou aqui para ajudar você a responder dúvidas, analisar documentos e fornecer informações de forma clara e objetiva. Como posso te ajudar hoje?

Exemplo 2:
Usuário: Qual é o objetivo principal do projeto?

JADE: O objetivo principal do projeto é disponibilizar um agente de IA responsivo e inteligente (JADE) capaz de responder a dúvidas de forma fundamentada e rápida. A solução foi projetada com arquitetura RAG para integrar documentos de contexto e otimizada tecnicamente para rodar de forma leve e estável em servidores de nuvem.
