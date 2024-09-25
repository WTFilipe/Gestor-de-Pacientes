from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QVBoxLayout, QTableWidgetItem, QAbstractItemView, \
    QPushButton, QHBoxLayout, QDialog, QMessageBox
from PyQt5.QtCore import QDateTime, QTimer, Qt

from AdicionarConsultaDialog import AdicionarConsultaDialog
from FirebaseDatabase import FirebaseDatabase
from PacienteDetalhesDialog import PacienteDetalhesDialog
from PacienteDialog import PacienteDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Gestor de Pacientes')

        medico_label = self.setup_header()

        #Inicializa o DB
        self.db = FirebaseDatabase()

        # Tabela de Pacientes (inicialmente vazia)
        self.setupTable()

        # Layout dos botões (horizontal)
        layout_botoes = self.setupBotoes()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.data_hora_label)
        layout.addWidget(medico_label)
        layout.addLayout(layout_botoes)
        layout.addWidget(self.tabela_pacientes)

        self.setLayout(layout)
        self.adjustSize()

    def setup_header(self):
        fonte_maior = QFont()
        fonte_maior.setPointSize(14)
        medico_label = QLabel('Médica: Dra. Julia Pinheiro dos Santos')
        medico_label.setFont(fonte_maior)


        self.data_hora_label = QLabel()
        self.atualizar_data_hora()
        self.data_hora_label.setFont(fonte_maior)
        return medico_label

    def atualizar_data_hora(self):
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.atualizar_data_hora)
        self.timer.start(1000)

        agora = QDateTime.currentDateTime()
        data_formatada = agora.toString("dddd, d 'de' MMMM 'de' yyyy, hh:mm")
        data_formatada = data_formatada.capitalize()
        self.data_hora_label.setText(data_formatada)

    def setupTable(self):
        self.tabela_pacientes = QTableWidget()
        self.tabela_pacientes.setColumnCount(6)
        self.tabela_pacientes.setHorizontalHeaderLabels(['ID', 'Nome do Paciente', 'Idade', 'Nome do Responsável', 'Última Consulta', 'Próxima Consulta'])
        self.tabela_pacientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_pacientes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_pacientes.itemDoubleClicked.connect(self.abrir_dialog_detalhes)
        self.tabela_pacientes.horizontalHeader().sectionClicked.connect(self.ordenar_por_coluna)

        self.tabela_pacientes.setColumnWidth(0, 50)

        pacientes = self.db.get_pacientes()
        self.inserir_pacientes_na_tabela(pacientes)

    def ordenar_por_coluna(self, coluna):
        if coluna == 1:  # Coluna "Nome do Paciente"
            self.tabela_pacientes.sortItems(coluna, Qt.AscendingOrder)
        if coluna == 3:  # Coluna "Ultima Consulta"
            self.tabela_pacientes.sortItems(coluna, Qt.AscendingOrder)
        if coluna == 4:  # Coluna "Proxima Consulta"
            self.tabela_pacientes.sortItems(coluna, Qt.AscendingOrder)

    def inserir_pacientes_na_tabela(self, pacientes):
        self.tabela_pacientes.setRowCount(0)
        for paciente in pacientes:
            linha = self.tabela_pacientes.rowCount()
            self.tabela_pacientes.insertRow(linha)
            self.tabela_pacientes.setItem(linha, 0, QTableWidgetItem(str(paciente['id'])))
            self.tabela_pacientes.setItem(linha, 1, QTableWidgetItem(paciente['nome']))
            self.tabela_pacientes.setItem(linha, 2, QTableWidgetItem(str(paciente['idade'])))
            self.tabela_pacientes.setItem(linha, 3, QTableWidgetItem(paciente['responsavel']))

            try:
                ultima_consulta = QDateTime.fromString(paciente.get('ultima_consulta'), Qt.ISODate)
                ultima_consulta = ultima_consulta.toString("dd/MM/yyyy - hh:mm")
            except Exception as e:
                ultima_consulta = "N/A"

            self.tabela_pacientes.setItem(linha, 4, QTableWidgetItem(ultima_consulta))

            try:
                proxima_consulta = QDateTime.fromString(paciente.get('proxima_consulta'), Qt.ISODate)
                proxima_consulta = proxima_consulta.toString("dd/MM/yyyy - hh:mm")
            except Exception as e:
                proxima_consulta = "N/A"

            self.tabela_pacientes.setItem(linha, 5, QTableWidgetItem(proxima_consulta))
        self.tabela_pacientes.resizeColumnsToContents()

    def inserir_paciente_na_tabela(self, paciente):
        linha = self.tabela_pacientes.rowCount()

        if 'id' in paciente:
            id =  paciente['id']
        else:
            id = "..."

        self.tabela_pacientes.insertRow(linha)
        self.tabela_pacientes.setItem(linha, 0, QTableWidgetItem(id))
        self.tabela_pacientes.setItem(linha, 1, QTableWidgetItem(paciente['nome']))
        self.tabela_pacientes.setItem(linha, 2, QTableWidgetItem(str(paciente['idade'])))
        self.tabela_pacientes.setItem(linha, 3, QTableWidgetItem(paciente['responsavel']))

        try:
            ultima_consulta = QDateTime.fromString(paciente.get('ultima_consulta'), Qt.ISODate)
            ultima_consulta = ultima_consulta.toString("dd/MM/yyyy - hh:mm")
        except Exception as e:
            ultima_consulta = "N/A"

        self.tabela_pacientes.setItem(linha, 4, QTableWidgetItem(ultima_consulta))

        try:
            proxima_consulta = QDateTime.fromString(paciente.get('proxima_consulta'), Qt.ISODate)
            proxima_consulta = proxima_consulta.toString("dd/MM/yyyy - hh:mm")
        except Exception as e:
            proxima_consulta = "N/A"

        self.tabela_pacientes.setItem(linha, 5, QTableWidgetItem(proxima_consulta))

        self.tabela_pacientes.resizeColumnsToContents()

    def atualizar_paciente_na_tabela(self, linha, paciente, paciente_id):
        self.tabela_pacientes.setItem(linha, 0, QTableWidgetItem(str(paciente_id)))
        self.tabela_pacientes.setItem(linha, 1, QTableWidgetItem(paciente['nome']))
        self.tabela_pacientes.setItem(linha, 2, QTableWidgetItem(str(paciente['idade'])))
        self.tabela_pacientes.setItem(linha, 3, QTableWidgetItem(paciente['responsavel']))

        ultima_consulta = paciente.get('ultima_consulta')
        if ultima_consulta:
            data_hora = QDateTime.fromString(ultima_consulta, Qt.ISODate)
            ultima_consulta_formatada = data_hora.toString('dd/MM/yyyy - hh:mm')
            self.tabela_pacientes.setItem(linha, 4, QTableWidgetItem(ultima_consulta_formatada))
        else:
            self.tabela_pacientes.setItem(linha, 4, QTableWidgetItem('N/A'))

        proxima_consulta = paciente.get('proxima_consulta')
        if ultima_consulta:
            data_hora = QDateTime.fromString(proxima_consulta, Qt.ISODate)
            proxima_consulta_formatada = data_hora.toString('dd/MM/yyyy - hh:mm')
            self.tabela_pacientes.setItem(linha, 4, QTableWidgetItem(proxima_consulta_formatada))
        else:
            self.tabela_pacientes.setItem(linha, 4, QTableWidgetItem('N/A'))


    def setupBotoes(self):
        self.botao_adicionar = QPushButton('Adicionar Paciente')
        self.botao_editar = QPushButton('Editar Paciente')
        self.botao_remover = QPushButton('Remover Paciente')
        self.botao_adicionar_consulta = QPushButton('Adicionar Consulta')

        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.botao_adicionar)
        layout_botoes.addWidget(self.botao_editar)
        layout_botoes.addWidget(self.botao_remover)
        layout_botoes.addWidget(self.botao_adicionar_consulta)
        self.botao_adicionar.clicked.connect(lambda: self.abrir_dialog_paciente(modo='adicionar'))
        self.botao_editar.clicked.connect(lambda: self.abrir_dialog_paciente(modo='editar'))
        self.botao_remover.clicked.connect(self.remover_paciente_selecionado)
        self.botao_adicionar_consulta.clicked.connect(self.abrir_dialog_adicionar_consulta)

        self.botao_editar.setEnabled(False)
        self.botao_remover.setEnabled(False)
        self.botao_adicionar_consulta.setEnabled(False)

        self.tabela_pacientes.itemSelectionChanged.connect(self.atualizar_botoes)
        return layout_botoes

    def atualizar_botoes(self):
        tem_selecao = self.tabela_pacientes.selectedItems()
        self.botao_editar.setEnabled(bool(tem_selecao))
        self.botao_remover.setEnabled(bool(tem_selecao))
        self.botao_adicionar_consulta.setEnabled(bool(tem_selecao))

    def abrir_dialog_paciente(self, modo='adicionar'):
        if modo == 'editar':
            linha_selecionada = self.tabela_pacientes.currentRow()
            if linha_selecionada == -1:
                QMessageBox.warning(self, 'Erro', 'Selecione um paciente para editar.')
                return

            paciente_id = self.tabela_pacientes.item(linha_selecionada, 0).text()
            paciente = self.db.obter_paciente_pelo_id(paciente_id)

            if paciente is None:
                QMessageBox.warning(self, 'Erro', 'Paciente não encontrado no banco de dados.')
                return
            dialog = PacienteDialog(self, paciente_id, paciente['nome'], str(paciente['idade']),
                                    paciente['responsavel'])
        else:  # modo == 'adicionar'
            dialog = PacienteDialog(self)  # Nenhum paciente para edição


        if dialog.exec_() == QDialog.Accepted:
            try:
                paciente_dados = {
                    'nome': dialog.nome_input.text(),
                    'idade': int(dialog.idade_input.text()),
                    'responsavel': dialog.responsavel_input.text()
                }

                if modo == 'adicionar':
                    self.db.inserir_paciente(paciente_dados)
                    self.inserir_paciente_na_tabela(paciente_dados)
                else:  # modo == 'editar'
                    self.db.atualizar_paciente(paciente_id, paciente_dados)  # Implemente este método na classe Database
                    self.atualizar_paciente_na_tabela(linha_selecionada, paciente_dados, paciente_id)  # Atualiza a tabela

            except Exception as e:
                print(e)

    def remover_paciente_selecionado(self):
        linha_selecionada = self.tabela_pacientes.currentRow()
        if linha_selecionada != -1:
            paciente_id = self.tabela_pacientes.item(linha_selecionada, 0).text()
            self.db.remover_paciente(paciente_id)
            self.tabela_pacientes.removeRow(linha_selecionada)

    def abrir_dialog_adicionar_consulta(self):
        try:
            linha_selecionada = self.tabela_pacientes.currentRow()
            if linha_selecionada != -1:
                paciente_id = self.tabela_pacientes.item(linha_selecionada, 0).text()
                paciente = self.db.obter_paciente_pelo_id(paciente_id)

                dialog = AdicionarConsultaDialog(self, paciente)
                if dialog.exec_() == QDialog.Accepted:
                    dados_consulta = dialog.get_dados_consulta()
                    self.db.inserir_consulta(dados_consulta, paciente_id)
        except Exception as e:
            print(e)

    def abrir_dialog_detalhes(self):
        try:
            linha_selecionada = self.tabela_pacientes.currentRow()
            if linha_selecionada != -1:
                paciente_id = self.tabela_pacientes.item(linha_selecionada, 0).text()
                paciente = self.db.obter_paciente_pelo_id(paciente_id)

                if paciente:
                    consultas = self.db.obter_consultas_por_paciente_id(paciente_id)

                    dialog = PacienteDetalhesDialog(self, paciente, consultas)
                    dialog.exec_()
                else:
                    QMessageBox.warning(self, 'Erro', 'Paciente não encontrado no banco de dados.')
        except Exception as e:
            print(e)
