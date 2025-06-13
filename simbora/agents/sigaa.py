import os
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from simbora.tools.sigaa import SigaaAPI

CLIENT_ID = os.getenv("SIGAA_API_CLIENT_ID")
CLIENT_SECRET = os.getenv("SIGAA_API_CLIENT_SECRET") 
X_API_KEY = os.getenv("SIGAA_API_X_API_KEY")

sigaa_api = SigaaAPI(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    x_api_key=X_API_KEY,
)

agent_prompt = (
    "Você é um especialista em informações acadêmicas e administrativas do SIGAA."
    "SIGAA é o Sistema Integrado de Gestão de Atividades Acadêmicas utilizado por diversas instituições de ensino superior no Brasil."
    "Enriqueça a solicitação do usuário com informações relevantes obtidas pelas suas ferramentas."
    "Se mais de um curso for mencionado, responda com informações de ambos os cursos."
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

sigaa_agent = create_react_agent(
    name="sigaa_agent",
    model=llm,
    tools=[
        sigaa_api.get_avaliacoes_docentes,
        sigaa_api.get_calendarios_academicos,
        sigaa_api.get_componentes_curriculares,
        sigaa_api.get_cursos,
        sigaa_api.get_foruns_curso,
        sigaa_api.get_mensagens_forum,
        sigaa_api.get_noticias,
        sigaa_api.get_unidades
    ],
    prompt=agent_prompt
)

if __name__ == "__main__":
    user_input = input("Digite sua pergunta: ")
    response = sigaa_agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )

    for message in response["messages"]:
        print(f"{message.content}")