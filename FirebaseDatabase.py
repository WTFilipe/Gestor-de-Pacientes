import firebase_admin
import datetime
from firebase_admin import credentials, firestore

class FirebaseDatabase:
    def __init__(self):
        cred = credentials.Certificate('firebase.json')
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def get_pacientes(self):
        pacientes_ref = self.db.collection('pacientes')
        docs = pacientes_ref.stream()

        pacientes = []
        for doc in docs:
            paciente_dict = doc.to_dict()
            paciente_dict['id'] = doc.id

            agora = datetime.datetime.now().isoformat()

            # Obter a última consulta do paciente
            consultas_ref_ultima = self.db.collection('consultas') \
                .where('paciente_id', '==', doc.id) \
                .where('data_hora', '<', agora) \
                .order_by('data_hora', direction=firestore.Query.DESCENDING) \
                .limit(1)
            ultima_consulta_doc = consultas_ref_ultima.get()
            if ultima_consulta_doc:
                paciente_dict['ultima_consulta'] = ultima_consulta_doc[0].to_dict()['data_hora']
            else:
                paciente_dict['ultima_consulta'] = 'N/A'

            # Obter a próxima consulta do paciente
            consultas_ref_proxima = self.db.collection('consultas') \
                .where('paciente_id', '==', doc.id) \
                .where('data_hora', '>', agora) \
                .order_by('data_hora') \
                .limit(1)
            proxima_consulta_doc = consultas_ref_proxima.get()
            if proxima_consulta_doc:
                paciente_dict['proxima_consulta'] = proxima_consulta_doc[0].to_dict()['data_hora']
            else:
                paciente_dict['proxima_consulta'] = 'N/A'

            pacientes.append(paciente_dict)

        return pacientes

    def obter_paciente_pelo_id(self, paciente_id):
        doc_ref = self.db.collection('pacientes').document(paciente_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def inserir_paciente(self, paciente):
        self.db.collection('pacientes').add(paciente)

    def remover_paciente(self, paciente):
        self.db.collection('pacientes').add(paciente)

    def inserir_consulta(self, consulta, paciente_id):
        consulta['paciente_id'] = paciente_id
        self.db.collection('consultas').add(consulta)

    def obter_consultas_por_paciente_id(self, paciente_id):
        consultas_ref = self.db.collection('consultas').where('paciente_id', '==', paciente_id).order_by('data_hora', direction=firestore.Query.DESCENDING)
        docs = consultas_ref.stream()

        consultas = []
        for doc in docs:
            consulta_dict = doc.to_dict()
            consulta_dict['id'] = doc.id
            consultas.append(consulta_dict)

        return consultas

    def atualizar_paciente(self, paciente_id, novos_dados):
        paciente_ref = self.db.collection('pacientes').document(paciente_id)

        ultima_consulta = novos_dados.get('ultima_consulta')
        if ultima_consulta and ultima_consulta != 'N/A':
            novos_dados['ultima_consulta'] = firestore.SERVER_TIMESTAMP

        paciente_ref.update(novos_dados)

    def remover_paciente(self, paciente_id):
        # Remover o paciente
        paciente_ref = self.db.collection('pacientes').document(paciente_id)
        paciente_ref.delete()

        # Remover as consultas associadas ao paciente
        consultas_ref = self.db.collection('consultas').where('paciente_id', '==', paciente_id)
        docs = consultas_ref.stream()
        for doc in docs:
            doc.reference.delete()