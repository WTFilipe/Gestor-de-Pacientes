from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QFormLayout, QWidget, QListWidgetItem, QHBoxLayout, QScrollArea, QListWidget


class PacienteDetalhesDialog(QDialog):
    def __init__(self, parent=None, paciente=None, consultas=[]):
        super().__init__(parent)
        self.setWindowTitle('Detalhes do Paciente')

        # Informações do Paciente
        nome_label = QLabel(f"{paciente['nome']}")
        idade_label = QLabel(f"{paciente['idade']}")
        responsavel_label = QLabel(f"{paciente['responsavel']}")

        # Lista de Consultas
        self.lista_consultas = QListWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.lista_consultas)

        self.adicionar_consultas_lista(consultas)

        layout_horizontal = QHBoxLayout()

        # Lado Esquerdo - Informações do Paciente
        layout_paciente = QFormLayout()
        layout_paciente.addRow('Nome:', nome_label)
        layout_paciente.addRow('Idade:', idade_label)
        layout_paciente.addRow('Responsável:', responsavel_label)
        layout_horizontal.addLayout(layout_paciente)

        # Lado Direito - Histórico de Consultas (com scroll)
        layout_horizontal.addWidget(scroll_area)

        self.setLayout(layout_horizontal)

    def adicionar_consultas_lista(self, consultas):
        self.lista_consultas.clear()

        for consulta in consultas:
            item_widget = ConsultaItemWidget(consulta)
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.lista_consultas.addItem(item)
            self.lista_consultas.setItemWidget(item, item_widget)

class ConsultaItemWidget(QWidget):
    def __init__(self, consulta):
        super().__init__()

        layout = QVBoxLayout()

        data_formatada = QDateTime.fromString(consulta['data_hora'], Qt.ISODate)
        data_formatada = data_formatada.toString("dd/MM/yyyy - hh:mm")

        if consulta['planejamento']:
            planejamento = consulta['planejamento']
        else:
            planejamento = 'N/A'

        if consulta['pontos_positivos']:
            pontos_positivos = consulta['pontos_positivos']
        else:
            pontos_positivos = 'N/A'

        if consulta['pontos_atencao']:
            pontos_atencao = consulta['pontos_atencao']
        else:
            pontos_atencao = 'N/A'

        if consulta['observacoes']:
            observacoes = consulta['observacoes']
        else:
            observacoes = 'N/A'

        data_label = QLabel(f"<b>Data:</b> {data_formatada}")
        planejamento_label = QLabel(f"<b>Planejamento:</b> {planejamento}")
        pontos_positivos_label = QLabel(f"<b>Pontos Positivos:</b> {pontos_positivos}")
        pontos_atencao_label = QLabel(f"<b>Pontos de Atenção:</b> {pontos_atencao}")
        observacoes_label = QLabel(f"<b>Observações:</b> {observacoes}")

        layout.addWidget(data_label)
        layout.addWidget(planejamento_label)
        layout.addWidget(pontos_positivos_label)
        layout.addWidget(pontos_atencao_label)
        layout.addWidget(observacoes_label)

        self.setLayout(layout)