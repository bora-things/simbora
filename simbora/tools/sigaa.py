from typing import Optional
import requests

class SigaaAPI:
    AUTH_URL = 'https://api.info.ufrn.br/authz-server/oauth/token'
    UNIDADES_URL = 'https://api.info.ufrn.br/unidade/v1/unidades'
    AVALIACOES_DOCENTES_URL = 'https://api.info.ufrn.br/avaliacao-institucional/v1/avaliacoes-docentes'
    NOTICIAS_URL = 'https://api.info.ufrn.br/noticia/v1/noticias'
    COMPONENTES_CURRICULARES_URL = 'https://api.info.ufrn.br/curso/v1/componentes-curriculares'
    MATRIZES_CURRICULARES_URL = 'https://api.info.ufrn.br/curso/v1/matrizes-curriculares'
    CALENDARIOS_ACADEMICOS_URL = 'https://api.info.ufrn.br/calendario/v1/calendarios'
    FORUNS_CURSOS_URL = 'https://api.info.ufrn.br/curso/v1/foruns-cursos'
    MENSAGENS_FORUNS_CURSOS_URL = 'https://api.info.ufrn.br/curso/v1/mensagens-foruns'

    def __init__(self, client_id, client_secret, x_api_key):
        self._client_id = client_id
        self._client_secret = client_secret
        self._x_api_key = x_api_key
        self._access_token = self._get_access_token()

    def _get_access_token(self):
        url = SigaaAPI.AUTH_URL
        params = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception('Authentication failed: {}'.format(response.text))
    
    def get_unidades(self, nome_ou_sigla_do_departamento_da_ufrn: str):
        """
        Útil quando se deseja buscar o ID de uma unidade (departamento da UFRN) pelo nome ou sigla.
        É importante que o usuário informe o nome ou sigla da unidade para que possa buscar o ID correspondente.
        
        :param str nome_ou_sigla: Nome ou sigla da unidade para a qual se deseja buscar o ID. Exemplos: "IMD", "Instituto Metrópole Digital"
        """
        url = SigaaAPI.UNIDADES_URL
        
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'x-api-key': self._x_api_key,
        }

        params = {
            'nome-ou-sigla': nome_ou_sigla_do_departamento_da_ufrn
        }

        unidades = []
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            unidades = data
        else:
            raise Exception('Failed to fetch unidades: {}'.format(response.text))
        return unidades

    def get_avaliacoes_docentes(self, id_unidade: int, nome_docente: Optional[str] =None):
        """
        Útil quando se deseja buscar avaliações de docentes em uma unidade.

        :param int id_unidade: ID da unidade para a qual se deseja buscar as avaliações.
        :param str docente: Nome do docente para filtrar as avaliações (opcional).
        """
        url = SigaaAPI.AVALIACOES_DOCENTES_URL
        
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'x-api-key': self._x_api_key,
        }

        params = {
            'id-unidade': id_unidade,
            'docente': nome_docente
        }

        avaliacoes = []
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            avaliacoes = data
        else:
            raise Exception('Failed to fetch avaliações docentes: {}'.format(response.text))
        return avaliacoes

    def get_noticias(self):
        """
        Útil quando se deseja buscar notícias relacionadas à UFRN.
        """
        url = SigaaAPI.NOTICIAS_URL
        
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'x-api-key': self._x_api_key,
        }

        noticias = []
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            noticias = data
        else:
            raise Exception('Failed to fetch notícias: {}'.format(response.text))
        
        return noticias

    def get_componentes_curriculares(
            self,
            nome_componente: Optional[str] = None,
            codigo_componente: Optional[str] = None,
            nome_departamento: Optional[str] = None
        ):
        """
        Útil quando se deseja buscar componentes curriculares por nome, código ou departamento.

        :param str nome_componente: Nome do componente curricular para busca (opcional).
        :param str codigo_componente: Código do componente curricular para busca (opcional).
        :param str nome_departamento: Nome do departamento ao qual o componente curricular pertence (opcional).
        """
        url = SigaaAPI.COMPONENTES_CURRICULARES_URL
        
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'x-api-key': self._x_api_key,
        }

        params = {
            'nome': nome_componente,
            'codigo': codigo_componente,
            'departamento': nome_departamento
        }

        componentes = []
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            componentes = data
        else:
            raise Exception('Failed to fetch componentes curriculares: {}'.format(response.text))
            
        return componentes

    def get_matrizes_curriculares(self, nome_curso: str, matrizes_ativas: Optional[bool] = True):
        """
        Útil quando se deseja buscar a matriz curricular de um curso específico.

        :param str nome_curso: Nome do curso para o qual se deseja buscar as matrizez curriculares.
        :param bool matrizes_ativas: Se True, busca apenas matrizes ativas. Se False, busca todas as matrizes (ativas e inativas).
        """
        url = SigaaAPI.MATRIZES_CURRICULARES_URL
        
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'x-api-key': self._x_api_key,
        }
        
        params = {
            'nome-curso': nome_curso,
            'ativo': matrizes_ativas
        }

        matrizes = []
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            matrizes = data
        else:
            raise Exception('Failed to fetch matrizes curriculares: {}'.format(response.text))
        return matrizes

    def get_calendarios_academicos(self, ano: int, periodo: int, vigente: Optional[bool] = True):
        """
        Útil quando se deseja buscar calendários acadêmicos de um ano específico.
        Os calendários acadêmicos são utilizados para verificar datas importantes do calendário, como início e fim de semestres, períodos de matrícula, etc.

        :param int ano: Ano para o qual se deseja buscar os calendários acadêmicos.
        :param int periodo: Período do ano (1 para primeiro semestre, 2 para segundo semestre).
        :param bool vigente: Se True, busca apenas calendários vigentes. Se False, busca todos os calendários (vigentes e não vigentes).
        """
        url = SigaaAPI.CALENDARIOS_ACADEMICOS_URL
        
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'x-api-key': self._x_api_key,
        }

        params = {
            'ano': ano,
            'periodo': periodo,
            'vigente': vigente
        }

        calendarios = []
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            calendarios = data
        else:
            raise Exception('Failed to fetch calendários acadêmicos: {}'.format(response.text))
        return calendarios

    def get_cursos(self, nome_curso: Optional[str] = None, id_unidade: Optional[int] = None):
        """
        Útil quando se deseja buscar cursos por nome ou unidade.
        Os cursos são utilizados para verificar informações sobre disciplinas, matrículas e outros aspectos acadêmicos.

        :param str nome_curso: Nome do curso para o qual se deseja buscar as informações (opcional).
        :param int id_unidade: ID da unidade (departamento) ao qual o curso pertence (opcional).
        """
        url = SigaaAPI.MATRIZES_CURRICULARES_URL
        
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'x-api-key': self._x_api_key,
        }

        params = {
            'nome-curso': nome_curso,
            'id-unidade': id_unidade
        }

        cursos = []
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            cursos = data
        else:
            raise Exception('Failed to fetch cursos: {}'.format(response.text))
        return cursos
    
    def get_foruns_curso(self, id_curso: int):
        """
        Útil quando se deseja buscar fóruns de um curso específico.
        Os fóruns são utilizados para discussões e interações entre alunos e professores sobre temas relacionados ao curso.
        Utilize este método para obter fóruns que podem conter discussões sobre ofertas de disciplinas e período de matrículas.

        :param int id_curso: ID do curso para o qual se deseja buscar os fóruns.
        """
        url = SigaaAPI.FORUNS_CURSOS_URL
        
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'x-api-key': self._x_api_key,
        }

        params = {
            'id-curso': id_curso
        }

        foruns = []
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            foruns = data
        else:
            raise Exception('Failed to fetch fóruns de cursos: {}'.format(response.text))
        return foruns

    def get_mensagens_forum(self, id_forum: int):
        """
        Útil quando se deseja buscar mensagens de um fórum específico.
        As mensagens contêm discussões e interações entre alunos e professores sobre temas relacionados ao curso (teoricamente).
        Utilize este método para obter mensagens que podem conter informações sobre ofertas de disciplinas e período de matrículas.

        :param int id_forum: ID do fórum para o qual se deseja buscar as mensagens.
        """
        url = SigaaAPI.MENSAGENS_FORUNS_CURSOS_URL
        
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'x-api-key': self._x_api_key,
        }

        params = {
            'id-topico': id_forum
        }

        mensagens = []
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            mensagens = data
        else:
            raise Exception('Failed to fetch mensagens de fóruns: {}'.format(response.text))
        return mensagens
    