from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QDateTimeEdit


class PacienteDialog(QDialog):
    def __init__(self, parent=None, id=None, nome=None, idade=None, responsavel=None):
        super().__init__(parent)
        self.setWindowTitle('Adicionar/Editar Paciente')

        # Campos de entrada
        self.id_input = QLineEdit(id)
        self.nome_input = QLineEdit(nome)
        self.idade_input = QLineEdit(idade)
        self.responsavel_input = QLineEdit(responsavel)

        # Botões
        botao_cancelar = QPushButton('Cancelar')
        botao_confirmar = QPushButton('Confirmar')
        botao_confirmar.clicked.connect(self.confirmar_paciente)
        botao_cancelar.clicked.connect(self.reject)

        # Layout
        layout = QFormLayout()
        layout.addRow('Nome:', self.nome_input)
        layout.addRow('Idade:', self.idade_input)
        layout.addRow('Responsável:', self.responsavel_input)
        layout.addRow(botao_cancelar, botao_confirmar)

        self.setLayout(layout)

    def confirmar_paciente(self):
        self.accept()