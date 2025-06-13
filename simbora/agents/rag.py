from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from simbora.tools.rag import (
    enriquecer_solicitacao_do_usuario,
    obter_caminhos_documentos
)

agent_prompt = (
    "Você é um assistente para tarefas de perguntas e respostas."
    "Se você não souber a resposta, diga que não sabe."
    "Sempre que necessário enriqueça a solicitação do usuário com informações relevantes de documentos do sistema."
    "Se mais de um curso for mencionado, responda com informações de ambos os cursos."
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

rag_agent = create_react_agent(
    name="rag_agent",
    model=llm,
    tools=[obter_caminhos_documentos, enriquecer_solicitacao_do_usuario],
    prompt=agent_prompt
)

if __name__ == "__main__":
    user_input = input("Digite sua pergunta: ")
    response = rag_agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )

    for message in response["messages"]:
        print(f"{message.content}")