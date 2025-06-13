from langgraph_supervisor import create_supervisor
from simbora.agents.rag import rag_agent
from simbora.agents.sigaa import sigaa_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

supervisor = create_supervisor(
    supervisor_name="simbora_supervisor",
    model=llm,
    agents=[rag_agent, sigaa_agent],
    prompt=(
        "Você é um supervisor que gerencia dois agentes:\n"
        "- um agente de RAG. Atribua tarefas relacionadas à dúvidas relacionadas à PPCs de cursos, FAQs e regulamentos da UFRN para este agente\n"
        "- um agente consumidor da API do SIGAA. Atribua tarefas relacionadas à informações dinâmicas da UFRN como notícias, calendários acadêmicos, avaliações de docentes, componentes curriculares (disciplinas) para este agente\n"
        "Não execute nenhum trabalho você mesmo."
        "A resposta final deve ser uma resposta completa e concisa, que responda à pergunta do usuário."
    )
).compile()


if __name__ == "__main__":
    user_input = input("Digite sua pergunta: ")
    response = supervisor.invoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )

    for message in response["messages"]:
        print(f"{message.content}")