"""
Nicole Tressler
April 23, 2026.
CPSC 4970, Auburn University

Final Project: PyQt5 Interface

"""


"""Team Editor window for managing team members."""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox,
    QGroupBox, QFormLayout, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ..models.team import Team
from ..models.member import Member


class TeamEditorDialog(QDialog):
    """Modal dialog for editing a team and its members."""

    def __init__(self, team: Team, parent=None):
        super().__init__(parent)
        self._team = team
        self._selected_index = -1
        self.setWindowTitle(f"Edit Team: {team.name}")
        self.setMinimumSize(520, 560)
        self._init_ui()
        self._refresh_list()

    def _init_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1f2e;
                color: #e8e0d4;
            }
            QLabel {
                color: #e8e0d4;
                font-family: 'Georgia', serif;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                color: #7ec8c8;
                padding: 8px 0;
            }
            QLabel#subtitle {
                font-size: 11px;
                color: #8a9bb0;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            QListWidget {
                background-color: #232838;
                border: 1px solid #3a4258;
                border-radius: 6px;
                color: #e8e0d4;
                font-family: 'Georgia', serif;
                font-size: 13px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #2a4a5e;
                color: #7ec8c8;
            }
            QListWidget::item:hover {
                background-color: #2d3548;
            }
            QLineEdit {
                background-color: #232838;
                border: 1px solid #3a4258;
                border-radius: 5px;
                color: #e8e0d4;
                font-family: 'Georgia', serif;
                font-size: 13px;
                padding: 7px 10px;
            }
            QLineEdit:focus {
                border-color: #7ec8c8;
            }
            QGroupBox {
                color: #7ec8c8;
                font-family: 'Georgia', serif;
                font-size: 12px;
                border: 1px solid #3a4258;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }
            QPushButton {
                background-color: #2a4a5e;
                color: #7ec8c8;
                border: 1px solid #3a6b7e;
                border-radius: 5px;
                font-family: 'Georgia', serif;
                font-size: 12px;
                padding: 7px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #3a6a7e;
                color: #a0e0e0;
            }
            QPushButton:pressed {
                background-color: #1a3a4e;
            }
            QPushButton#danger {
                background-color: #4a2a2a;
                color: #e07878;
                border-color: #6a3a3a;
            }
            QPushButton#danger:hover {
                background-color: #6a3a3a;
                color: #f09898;
            }
            QPushButton#primary {
                background-color: #1e5a6e;
                color: #a0e8e8;
                border-color: #2a7a8e;
                font-weight: bold;
            }
            QPushButton#primary:hover {
                background-color: #2a7a8e;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        title = QLabel(f"Team: {self._team.name}")
        title.setObjectName("title")
        layout.addWidget(title)

        sub = QLabel("MEMBER ROSTER")
        sub.setObjectName("subtitle")
        layout.addWidget(sub)

        # Member list
        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._on_selection_changed)
        layout.addWidget(self._list, stretch=1)

        # Form group
        form_group = QGroupBox("Member Details")
        form_layout = QFormLayout(form_group)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(14, 18, 14, 14)

        name_label = QLabel("Name:")
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Enter member name...")
        form_layout.addRow(name_label, self._name_edit)

        email_label = QLabel("Email:")
        self._email_edit = QLineEdit()
        self._email_edit.setPlaceholderText("Enter email address...")
        form_layout.addRow(email_label, self._email_edit)

        layout.addWidget(form_group)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self._add_btn = QPushButton("Add Member")
        self._add_btn.setObjectName("primary")
        self._add_btn.clicked.connect(self._add_member)

        self._update_btn = QPushButton("Update")
        self._update_btn.clicked.connect(self._update_member)
        self._update_btn.setEnabled(False)

        self._delete_btn = QPushButton("Delete")
        self._delete_btn.setObjectName("danger")
        self._delete_btn.clicked.connect(self._delete_member)
        self._delete_btn.setEnabled(False)

        btn_row.addWidget(self._add_btn)
        btn_row.addWidget(self._update_btn)
        btn_row.addWidget(self._delete_btn)
        layout.addLayout(btn_row)

        # Close button
        close_btn = QPushButton("Done")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

    def _refresh_list(self):
        self._list.clear()
        for member in self._team.members:
            display = member.name
            if member.email:
                display += f"  <{member.email}>"
            item = QListWidgetItem(display)
            self._list.addItem(item)

    def _on_selection_changed(self, row: int):
        self._selected_index = row
        enabled = row >= 0
        self._update_btn.setEnabled(enabled)
        self._delete_btn.setEnabled(enabled)

        if enabled:
            members = self._team.members
            if row < len(members):
                m = members[row]
                self._name_edit.setText(m.name)
                self._email_edit.setText(m.email)

    def _add_member(self):
        name = self._name_edit.text().strip()
        email = self._email_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Required", "Member name cannot be empty.")
            return
        self._team.add_member(Member(name=name, email=email))
        self._refresh_list()
        self._name_edit.clear()
        self._email_edit.clear()

    def _update_member(self):
        idx = self._selected_index
        if idx < 0:
            return
        name = self._name_edit.text().strip()
        email = self._email_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Required", "Member name cannot be empty.")
            return
        try:
            self._team.update_member(idx, name, email)
            self._refresh_list()
            self._list.setCurrentRow(idx)
        except IndexError as e:
            QMessageBox.critical(self, "Error", str(e))

    def _delete_member(self):
        idx = self._selected_index
        if idx < 0:
            return
        members = self._team.members
        name = members[idx].name if idx < len(members) else "this member"
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete member '{name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                self._team.remove_member(idx)
                self._refresh_list()
                self._name_edit.clear()
                self._email_edit.clear()
                self._selected_index = -1
                self._update_btn.setEnabled(False)
                self._delete_btn.setEnabled(False)
            except IndexError as e:
                QMessageBox.critical(self, "Error", str(e))
