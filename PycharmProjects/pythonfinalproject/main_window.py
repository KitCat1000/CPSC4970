"""Main application window for the Curling League Manager."""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QMessageBox, QFileDialog, QAction, QMenuBar, QStatusBar,
    QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from ..models.database import Database
from ..models.league import League
from .league_editor import LeagueEditorDialog


MAIN_STYLE = """
    QMainWindow {
        background-color: #111520;
    }
    QWidget#central {
        background-color: #111520;
    }
    QMenuBar {
        background-color: #0d1018;
        color: #7090a8;
        font-family: 'Georgia', serif;
        font-size: 12px;
        border-bottom: 1px solid #1e2535;
        padding: 2px 0;
    }
    QMenuBar::item:selected {
        background-color: #1e2535;
        color: #7ec8c8;
    }
    QMenu {
        background-color: #141922;
        color: #d8e0e8;
        border: 1px solid #2a3548;
        font-family: 'Georgia', serif;
        font-size: 12px;
    }
    QMenu::item:selected {
        background-color: #1e3d52;
        color: #7ec8c8;
    }
    QMenu::separator {
        height: 1px;
        background-color: #2a3548;
        margin: 4px 10px;
    }
    QLabel {
        color: #c8d8e8;
        font-family: 'Georgia', serif;
    }
    QLabel#app_title {
        font-size: 26px;
        font-weight: bold;
        color: #7ec8c8;
        letter-spacing: 1px;
    }
    QLabel#app_subtitle {
        font-size: 11px;
        color: #4a6a80;
        letter-spacing: 3px;
    }
    QLabel#section_label {
        font-size: 11px;
        color: #4a6a80;
        letter-spacing: 2px;
        padding-top: 4px;
    }
    QListWidget {
        background-color: #161c28;
        border: 1px solid #233040;
        border-radius: 8px;
        color: #c8d8e8;
        font-family: 'Georgia', serif;
        font-size: 14px;
        padding: 6px;
        outline: none;
    }
    QListWidget::item {
        padding: 12px 16px;
        border-radius: 5px;
        margin: 2px 0;
    }
    QListWidget::item:selected {
        background-color: #1e3d52;
        color: #7ec8c8;
    }
    QListWidget::item:hover:!selected {
        background-color: #1a2535;
    }
    QLineEdit {
        background-color: #161c28;
        border: 1px solid #233040;
        border-radius: 6px;
        color: #c8d8e8;
        font-family: 'Georgia', serif;
        font-size: 13px;
        padding: 9px 12px;
    }
    QLineEdit:focus {
        border-color: #7ec8c8;
        background-color: #1a2030;
    }
    QLineEdit::placeholder {
        color: #3a5060;
    }
    QPushButton {
        background-color: #1a3040;
        color: #7ec8c8;
        border: 1px solid #2a5060;
        border-radius: 6px;
        font-family: 'Georgia', serif;
        font-size: 12px;
        padding: 9px 18px;
        min-width: 90px;
    }
    QPushButton:hover {
        background-color: #2a5060;
        color: #a0e0e0;
    }
    QPushButton:pressed {
        background-color: #0e2030;
    }
    QPushButton:disabled {
        background-color: #141820;
        color: #2a4050;
        border-color: #1a2530;
    }
    QPushButton#danger {
        background-color: #2e1a1a;
        color: #d07070;
        border-color: #4a2828;
    }
    QPushButton#danger:hover {
        background-color: #4a2828;
        color: #f09090;
    }
    QPushButton#primary {
        background-color: #103848;
        color: #80e0e0;
        border-color: #206878;
        font-weight: bold;
    }
    QPushButton#primary:hover {
        background-color: #206878;
    }
    QStatusBar {
        background-color: #0d1018;
        color: #4a6a80;
        font-family: 'Georgia', serif;
        font-size: 11px;
        border-top: 1px solid #1e2535;
    }
    QFrame#separator {
        background-color: #1e2535;
    }
"""


class MainWindow(QMainWindow):
    """Main application window managing the league database."""

    def __init__(self):
        super().__init__()
        self._db = Database()
        self._current_file: str = None
        self._selected_index = -1
        self.setWindowTitle("Curling League Manager")
        self.setMinimumSize(600, 620)
        self._init_ui()
        self._update_status()

    def _init_ui(self):
        self.setStyleSheet(MAIN_STYLE)

        # Menu bar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        file_menu = menubar.addMenu("File")
        new_action = QAction("New Database", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_database)

        load_action = QAction("Load Database...", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self._load_database)

        save_action = QAction("Save Database", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_database)

        save_as_action = QAction("Save Database As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self._save_database_as)

        file_menu.addAction(new_action)
        file_menu.addSeparator()
        file_menu.addAction(load_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)

        # Central widget
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        # Header
        title_label = QLabel("Curling League Manager")
        title_label.setObjectName("app_title")
        layout.addWidget(title_label)

        sub_label = QLabel("DATABASE ADMINISTRATION")
        sub_label.setObjectName("app_subtitle")
        layout.addWidget(sub_label)

        # Separator
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        layout.addWidget(sep)

        # Section label
        section_lbl = QLabel("LEAGUES")
        section_lbl.setObjectName("section_label")
        layout.addWidget(section_lbl)

        # League list
        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._on_selection_changed)
        self._list.itemDoubleClicked.connect(self._edit_league)
        layout.addWidget(self._list, stretch=1)

        # Add league row
        add_row = QHBoxLayout()
        add_row.setSpacing(10)
        self._league_name_edit = QLineEdit()
        self._league_name_edit.setPlaceholderText("Enter new league name...")
        add_btn = QPushButton("Add League")
        add_btn.setObjectName("primary")
        add_btn.clicked.connect(self._add_league)
        self._league_name_edit.returnPressed.connect(self._add_league)
        add_row.addWidget(self._league_name_edit, stretch=1)
        add_row.addWidget(add_btn)
        layout.addLayout(add_row)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self._edit_btn = QPushButton("Edit League")
        self._edit_btn.clicked.connect(self._edit_league)
        self._edit_btn.setEnabled(False)

        self._delete_btn = QPushButton("Delete League")
        self._delete_btn.setObjectName("danger")
        self._delete_btn.clicked.connect(self._delete_league)
        self._delete_btn.setEnabled(False)

        load_btn = QPushButton("Load DB...")
        load_btn.clicked.connect(self._load_database)

        save_btn = QPushButton("Save DB")
        save_btn.clicked.connect(self._save_database)

        btn_row.addWidget(self._edit_btn)
        btn_row.addWidget(self._delete_btn)
        btn_row.addStretch()
        btn_row.addWidget(load_btn)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

        # Status bar
        self._status = QStatusBar()
        self.setStatusBar(self._status)

    def _refresh_list(self):
        self._list.clear()
        for league in self._db.leagues:
            count = len(league.teams)
            item = QListWidgetItem(
                f"{league.name}   —   {count} team{'s' if count != 1 else ''}"
            )
            self._list.addItem(item)

    def _on_selection_changed(self, row: int):
        self._selected_index = row
        enabled = row >= 0
        self._edit_btn.setEnabled(enabled)
        self._delete_btn.setEnabled(enabled)

    def _add_league(self):
        name = self._league_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Required", "League name cannot be empty.")
            return
        try:
            self._db.add_league(League(name=name))
            self._refresh_list()
            self._league_name_edit.clear()
            self._update_status()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def _edit_league(self):
        idx = self._selected_index
        if idx < 0:
            idx = self._list.currentRow()
        if idx < 0:
            return
        leagues = self._db.leagues
        if idx >= len(leagues):
            return
        dlg = LeagueEditorDialog(leagues[idx], parent=self)
        dlg.exec_()
        self._refresh_list()
        self._update_status()

    def _delete_league(self):
        idx = self._selected_index
        if idx < 0:
            return
        leagues = self._db.leagues
        name = leagues[idx].name if idx < len(leagues) else "this league"
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete league '{name}' and all its data?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                self._db.remove_league(idx)
                self._refresh_list()
                self._selected_index = -1
                self._edit_btn.setEnabled(False)
                self._delete_btn.setEnabled(False)
                self._update_status()
            except IndexError as e:
                QMessageBox.critical(self, "Error", str(e))

    def _new_database(self):
        if self._db.leagues:
            reply = QMessageBox.question(
                self, "New Database",
                "Create a new empty database? Unsaved changes will be lost.",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        self._db = Database()
        self._current_file = None
        self._refresh_list()
        self._update_status()

    def _load_database(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Database", "",
            "JSON Files (*.json);;All Files (*)"
        )
        if path:
            try:
                self._db = Database.load(path)
                self._current_file = path
                self._refresh_list()
                self._selected_index = -1
                self._edit_btn.setEnabled(False)
                self._delete_btn.setEnabled(False)
                self._update_status(f"Loaded: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"Could not load database:\n{e}")

    def _save_database(self):
        if self._current_file:
            try:
                self._db.save(self._current_file)
                self._update_status(f"Saved: {self._current_file}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Could not save database:\n{e}")
        else:
            self._save_database_as()

    def _save_database_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Database As", "leagues.json",
            "JSON Files (*.json);;All Files (*)"
        )
        if path:
            try:
                self._db.save(path)
                self._current_file = path
                self._update_status(f"Saved: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Could not save database:\n{e}")

    def _update_status(self, message: str = None):
        if message:
            self._status.showMessage(message, 5000)
        else:
            count = len(self._db.leagues)
            file_part = f"  |  {self._current_file}" if self._current_file else "  |  Unsaved"
            self._status.showMessage(
                f"{count} league{'s' if count != 1 else ''}{file_part}"
            )
