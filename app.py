import os
import sys
import traceback

# ============================================================
# JADE AI AGENT
# Aplicação Gradio + Groq para Render
# ============================================================

# Força os logs a aparecerem imediatamente no Render
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass


print("=" * 60, flush=True)
print("💎 JADE AI AGENT - INICIANDO", flush=True)
print("=" * 60, flush=True)


# ============================================================
# 1. CONFIGURAÇÃO
# ============================================================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()

PORT = int(os.environ.get("PORT", "10000"))

MODEL_NAME = "openai/gpt-oss-120b"


print(f"🌐 Porta configurada: {PORT}", flush=True)
print(f"🤖 Modelo configurado: {MODEL_NAME}", flush=True)


# ============================================================
# 2. VERIFICAÇÃO DA API KEY
# ============================================================

if not GROQ_API_KEY:
    print(
        "⚠️ AVISO: GROQ_API_KEY não foi encontrada.",
        flush=True
    )
else:
    print(
        "✅ GROQ_API_KEY encontrada.",
        flush=True
    )


# ============================================================
# 3. IMPORTS
# ============================================================

try:

    print("📦 Importando Gradio...", flush=True)

    import gradio as gr

    print("✅ Gradio importado.", flush=True)


    print("📦 Importando LangChain Groq...", flush=True)

    from langchain_groq import ChatGroq

    print("✅ LangChain Groq importado.", flush=True)


    print("✅ Todos os imports concluídos.", flush=True)


except Exception as e:

    print("❌ ERRO DURANTE OS IMPORTS", flush=True)
    print(str(e), flush=True)

    traceback.print_exc()

    sys.exit(1)


# ============================================================
# 4. INICIALIZAÇÃO DO MODELO
# ============================================================

llm = None


if GROQ_API_KEY:

    try:

        print(
            f"🔌 Conectando à Groq com {MODEL_NAME}...",
            flush=True
        )


        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=MODEL_NAME,
            temperature=0.2,
        )


        print(
            "✅ Cliente Groq inicializado com sucesso.",
            flush=True
        )


    except Exception as e:

        print(
            "❌ ERRO AO INICIALIZAR O MODELO GROQ",
            flush=True
        )

        print(str(e), flush=True)

        traceback.print_exc()


else:

    print(
        "⚠️ Modelo não inicializado porque GROQ_API_KEY está vazia.",
        flush=True
    )


# ============================================================
# 5. PERSONALIDADE DO JADE
# ============================================================

SYSTEM_PROMPT = """
Você é JADE, uma assistente virtual inteligente e profissional.

Seu objetivo é ajudar usuários de forma clara, objetiva,
educada e confiável.

Regras:

- Responda sempre de forma clara.
- Não invente informações.
- Quando não souber algo, diga claramente que não sabe.
- Organize respostas longas em tópicos quando apropriado.
- Use português quando o usuário escrever em português.
- Seja profissional e amigável.
- Evite respostas desnecessariamente longas.
"""


# ============================================================
# 6. FUNÇÃO PRINCIPAL
# ============================================================

def responder_jade(mensagem, historico):

    print("-" * 60, flush=True)
    print("📩 Nova mensagem recebida.", flush=True)


    # --------------------------------------------------------
    # Validação
    # --------------------------------------------------------

    if not mensagem:

        print(
            "⚠️ Mensagem vazia.",
            flush=True
        )

        return "Por favor, digite uma pergunta."


    mensagem = str(mensagem).strip()


    if not mensagem:

        return "Por favor, digite uma pergunta."


    # --------------------------------------------------------
    # Verificação do modelo
    # --------------------------------------------------------

    if llm is None:

        print(
            "❌ LLM não está inicializado.",
            flush=True
        )

        return (
            "⚠️ O JADE não conseguiu inicializar o modelo de IA. "
            "Verifique a GROQ_API_KEY no Render."
        )


    try:

        # ----------------------------------------------------
        # Construção das mensagens
        # ----------------------------------------------------

        mensagens = [
            (
                "system",
                SYSTEM_PROMPT
            )
        ]


        # ----------------------------------------------------
        # Histórico da conversa
        # ----------------------------------------------------

        if historico:

            for item in historico:

                try:

                    # Formato antigo:
                    # [usuario, assistente]

                    if isinstance(item, (list, tuple)):

                        if len(item) >= 2:

                            usuario = item[0]
                            assistente = item[1]


                            if usuario:

                                mensagens.append(
                                    (
                                        "human",
                                        str(usuario)
                                    )
                                )


                            if assistente:

                                mensagens.append(
                                    (
                                        "assistant",
                                        str(assistente)
                                    )
                                )


                    # Formato novo do Gradio:
                    # {"role": ..., "content": ...}

                    elif isinstance(item, dict):

                        role = item.get("role")
                        content = item.get("content")


                        if role == "user" and content:

                            mensagens.append(
                                (
                                    "human",
                                    str(content)
                                )
                            )


                        elif role == "assistant" and content:

                            mensagens.append(
                                (
                                    "assistant",
                                    str(content)
                                )
                            )

                except Exception:

                    continue


        # ----------------------------------------------------
        # Mensagem atual
        # ----------------------------------------------------

        mensagens.append(
            (
                "human",
                mensagem
            )
        )


        print(
            "🤖 Consultando modelo Groq...",
            flush=True
        )


        # ----------------------------------------------------
        # Chamada ao LLM
        # ----------------------------------------------------

        resposta = llm.invoke(mensagens)


        # ----------------------------------------------------
        # Resultado
        # ----------------------------------------------------

        if hasattr(resposta, "content"):

            conteudo = resposta.content

        else:

            conteudo = str(resposta)


        print(
            "✅ Resposta gerada com sucesso.",
            flush=True
        )


        return conteudo


    except Exception as e:

        print(
            "❌ ERRO AO CONSULTAR O MODELO",
            flush=True
        )

        print(
            str(e),
            flush=True
        )

        traceback.print_exc()


        return (
            "Ops! O JADE encontrou um erro ao consultar "
            "o modelo de IA.\n\n"
            f"Detalhes: {str(e)}"
        )


# ============================================================
# 7. INTERFACE GRADIO
# ============================================================

print("🎨 Criando interface Gradio...", flush=True)


theme = gr.themes.Soft(
    primary_hue="emerald",
    secondary_hue="teal",
    neutral_hue="slate"
)


with gr.Blocks(
    theme=theme,
    title="JADE AI Agent"
) as demo:

    gr.Markdown(
        """
        # 💎 JADE AI Agent

        ### Assistente Virtual Inteligente

        Faça uma pergunta para começar.
        """
    )


    gr.ChatInterface(
        fn=responder_jade,
        title="JADE",
        description="Assistente de Inteligência Artificial",
        textbox=gr.Textbox(
            placeholder="Digite sua pergunta...",
            container=True,
            scale=7
        ),
    )


print("✅ Interface Gradio criada.", flush=True)


# ============================================================
# 8. INICIALIZAÇÃO DO SERVIDOR
# ============================================================

if __name__ == "__main__":

    print("=" * 60, flush=True)

    print(
        f"🚀 INICIANDO SERVIDOR NA PORTA {PORT}",
        flush=True
    )

    print(
        "🌐 Endereço: 0.0.0.0",
        flush=True
    )

    print("=" * 60, flush=True)


    try:

        demo.launch(
            server_name="0.0.0.0",
            server_port=PORT,
            show_error=True,
            quiet=False,
        )


    except Exception as e:

        print(
            "❌ ERRO AO INICIAR O SERVIDOR GRADIO",
            flush=True
        )

        print(
            str(e),
            flush=True
        )

        traceback.print_exc()

        sys.exit(1)
