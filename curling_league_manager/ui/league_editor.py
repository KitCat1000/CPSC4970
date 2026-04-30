"""
Nicole Tressler
April 23, 2026.
CPSC 4970, Auburn University

Final Project: PyQt5 Interface

"""


"""League Editor window for managing teams within a league."""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox,
    QFileDialog, QMenuBar, QAction
)
from PyQt5.QtCore import Qt

from ..models.league import League
from ..models.team import Team
from ..utils.csv_io import export_league_csv, import_league_csv
from team_editor import TeamEditorDialog

STYLE = """
    QDialog {
        background-color: #1a1f2e;
        color: #e8e0d4;
    }
    QMenuBar {
        background-color: #12161f;
        color: #8a9bb0;
        font-family: 'Georgia', serif;
        font-size: 12px;
        border-bottom: 1px solid #2a3040;
    }
    QMenuBar::item:selected {
        background-color: #2a3040;
        color: #7ec8c8;
    }
    QMenu {
        background-color: #1a2030;
        color: #e8e0d4;
        border: 1px solid #3a4258;
        font-family: 'Georgia', serif;
    }
    QMenu::item:selected {
        background-color: #2a4a5e;
        color: #7ec8c8;
    }
    QLabel {
        color: #e8e0d4;
        font-family: 'Georgia', serif;
    }
    QLabel#title {
        font-size: 18px;
        font-weight: bold;
        color: #c8a87e;
        padding: 8px 0;
    }
    QLabel#subtitle {
        font-size: 11px;
        color: #8a9bb0;
        letter-spacing: 2px;
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
        padding: 10px 12px;
        border-radius: 4px;
    }
    QListWidget::item:selected {
        background-color: #3a3020;
        color: #c8a87e;
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
        border-color: #c8a87e;
    }
    QPushButton {
        background-color: #3a3020;
        color: #c8a87e;
        border: 1px solid #5a4a30;
        border-radius: 5px;
        font-family: 'Georgia', serif;
        font-size: 12px;
        padding: 7px 16px;
        min-width: 80px;
    }
    QPushButton:hover {
        background-color: #4a4030;
        color: #e8c898;
    }
    QPushButton:pressed {
        background-color: #2a2010;
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
        background-color: #4a3a10;
        color: #f0c870;
        border-color: #6a5a30;
        font-weight: bold;
    }
    QPushButton#primary:hover {
        background-color: #6a5a30;
    }
"""


class LeagueEditorDialog(QDialog):
    """Modal dialog for editing a league and its teams."""

    def __init__(self, league: League, parent=None):
        super().__init__(parent)
        self._league = league
        self._selected_index = -1
        self.setWindowTitle(f"Edit League: {league.name}")
        self.setMinimumSize(500, 520)
        self._init_ui()
        self._refresh_list()

    def _init_ui(self):
        self.setStyleSheet(STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 16)

        # Menu bar
        menubar = QMenuBar(self)
        menubar.setNativeMenuBar(False)
        layout.setMenuBar(menubar)

        file_menu = menubar.addMenu("League Data")
        import_action = QAction("Import from CSV...", self)
        import_action.triggered.connect(self._import_csv)
        export_action = QAction("Export to CSV...", self)
        export_action.triggered.connect(self._export_csv)
        file_menu.addAction(import_action)
        file_menu.addAction(export_action)

        inner = QVBoxLayout()
        inner.setSpacing(10)
        inner.setContentsMargins(20, 8, 20, 0)
        layout.addLayout(inner)

        # Header
        title = QLabel(f"League: {self._league.name}")
        title.setObjectName("title")
        inner.addWidget(title)

        sub = QLabel("TEAM ROSTER")
        sub.setObjectName("subtitle")
        inner.addWidget(sub)

        # Team list
        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._on_selection_changed)
        self._list.itemDoubleClicked.connect(self._edit_team)
        inner.addWidget(self._list, stretch=1)

        # Add team row
        add_row = QHBoxLayout()
        add_row.setSpacing(8)
        self._team_name_edit = QLineEdit()
        self._team_name_edit.setPlaceholderText("New team name...")
        add_btn = QPushButton("Add Team")
        add_btn.setObjectName("primary")
        add_btn.clicked.connect(self._add_team)
        add_row.addWidget(self._team_name_edit, stretch=1)
        add_row.addWidget(add_btn)
        inner.addLayout(add_row)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self._edit_btn = QPushButton("Edit Team")
        self._edit_btn.clicked.connect(self._edit_team)
        self._edit_btn.setEnabled(False)

        self._delete_btn = QPushButton("Delete Team")
        self._delete_btn.setObjectName("danger")
        self._delete_btn.clicked.connect(self._delete_team)
        self._delete_btn.setEnabled(False)

        close_btn = QPushButton("Done")
        close_btn.clicked.connect(self.accept)

        btn_row.addWidget(self._edit_btn)
        btn_row.addWidget(self._delete_btn)
        btn_row.addStretch()
        btn_row.addWidget(close_btn)
        inner.addLayout(btn_row)

    def _refresh_list(self):
        self._list.clear()
        for team in self._league.teams:
            count = len(team.members)
            item = QListWidgetItem(f"{team.name}  ({count} member{'s' if count != 1 else ''})")
            self._list.addItem(item)

    def _on_selection_changed(self, row: int):
        self._selected_index = row
        enabled = row >= 0
        self._edit_btn.setEnabled(enabled)
        self._delete_btn.setEnabled(enabled)

    def _add_team(self):
        name = self._team_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Required", "Team name cannot be empty.")
            return
        try:
            self._league.add_team(Team(name=name))
            self._refresh_list()
            self._team_name_edit.clear()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def _edit_team(self):
        idx = self._selected_index
        if idx < 0:
            idx = self._list.currentRow()
        if idx < 0:
            return
        teams = self._league.teams
        if idx >= len(teams):
            return
        dlg = TeamEditorDialog(teams[idx], parent=self)
        dlg.exec_()
        self._refresh_list()

    def _delete_team(self):
        idx = self._selected_index
        if idx < 0:
            return
        teams = self._league.teams
        name = teams[idx].name if idx < len(teams) else "this team"
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete team '{name}' and all its members?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                self._league.remove_team(idx)
                self._refresh_list()
                self._selected_index = -1
                self._edit_btn.setEnabled(False)
                self._delete_btn.setEnabled(False)
            except IndexError as e:
                QMessageBox.critical(self, "Error", str(e))

    def _export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export League to CSV", f"{self._league.name}.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        if path:
            try:
                export_league_csv(self._league, path)
                QMessageBox.information(self, "Export Successful", f"League exported to:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", str(e))

    def _import_csv(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import League from CSV", "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if path:
            try:
                imported = import_league_csv(path, league_name=self._league.name)
                # Merge: add teams from imported league
                for team in imported.teams:
                    self._league.add_team(team)
                self._refresh_list()
                QMessageBox.information(
                    self, "Import Successful",
                    f"Imported {len(imported.teams)} team(s) from CSV."
                )
            except Exception as e:
                QMessageBox.critical(self, "Import Error", str(e))
