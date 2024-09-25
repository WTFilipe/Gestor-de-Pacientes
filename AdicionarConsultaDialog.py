from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QTextEdit, QDateTimeEdit, \
    QHBoxLayout
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont

class AdicionarConsultaDialog(QDialog):
    def __init__(self, parent=None, paciente=None):
        super().__init__(parent)
        self.setWindowTitle('Adicionar Consulta')

        fonte_grande = QFont()
        fonte_grande.setPointSize(16)
        nome_paciente_label = QLabel(f"Paciente: {paciente['nome']}")
        nome_paciente_label.setFont(fonte_grande)

        idade_paciente_label = QLabel(f"Idade: {paciente['idade']}")
        idade_paciente_label.setFont(fonte_grande)

        fonte_pequena = QFont()
        fonte_pequena.setPointSize(12)
        responsavel_label = QLabel(f"Responsável: {paciente['responsavel']}")
        responsavel_label.setFont(fonte_pequena)

        # Data e Hora
        self.data_hora_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.data_hora_input.setCalendarPopup(True)

        self.planejamento_input = QTextEdit()
        self.planejamento_input.setFixedHeight(self.planejamento_input.fontMetrics().lineSpacing() * 5)

        # Campos de texto
        self.pontos_positivos_input = QTextEdit()
        self.pontos_positivos_input.setFixedHeight(self.pontos_positivos_input.fontMetrics().lineSpacing() * 5)

        self.pontos_atencao_input = QTextEdit()
        self.pontos_atencao_input.setFixedHeight(self.pontos_atencao_input.fontMetrics().lineSpacing() * 5)

        self.observacoes_input = QTextEdit()
        self.observacoes_input.setFixedHeight(self.observacoes_input.fontMetrics().lineSpacing() * 5)

        # Botões
        botao_confirmar = QPushButton('Confirmar')
        botao_cancelar = QPushButton('Cancelar')
        botao_confirmar.clicked.connect(self.accept)
        botao_cancelar.clicked.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(nome_paciente_label)
        layout.addWidget(idade_paciente_label)
        layout.addWidget(responsavel_label)

        layout_form = QFormLayout()
        layout_form.addRow('Data e Hora:', self.data_hora_input)
        layout_form.addRow('Planejamento:', self.planejamento_input)
        layout_form.addRow('Pontos Positivos:', self.pontos_positivos_input)
        layout_form.addRow('Pontos de Atenção:', self.pontos_atencao_input)
        layout_form.addRow('Observações:', self.observacoes_input)
        layout.addLayout(layout_form)

        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(botao_confirmar)
        layout_botoes.addWidget(botao_cancelar)
        layout.addLayout(layout_botoes)

        self.setLayout(layout)

    def get_dados_consulta(self):
        return {
            'data_hora': self.data_hora_input.dateTime().toString(Qt.ISODate),
            'pontos_positivos': self.pontos_positivos_input.toPlainText(),
            'pontos_atencao': self.pontos_atencao_input.toPlainText(),
            'observacoes': self.observacoes_input.toPlainText(),
            'planejamento': self.planejamento_input.toPlainText()
        }