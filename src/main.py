import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, 
                             QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QCheckBox, QTextEdit, QLineEdit)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from data import load_config, save_config
from dialogs import AddAppDialog
from installer import install_apt, install_snap, install_flatpak, install_deb, run_post_install_script

class InstallWorker(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, apps_to_install):
        super().__init__()
        self.apps_to_install = apps_to_install

    def run(self):
        for app in self.apps_to_install:
            self.log_signal.emit(f"=== Starting Installation: {app['name']} ===")
            
            def log_callback(msg):
                self.log_signal.emit(msg)

            if app.get("pre_script"):
                self.log_signal.emit(f"Running Pre-Install Script: {app['pre_script']}")
                run_post_install_script(app["pre_script"], log_callback)

            if app["type"] == "apt":
                install_apt(app["identifier"], log_callback)
            elif app["type"] == "snap":
                install_snap(app["identifier"], log_callback)
            elif app["type"] == "flatpak":
                install_flatpak(app["identifier"], log_callback)
            elif app["type"] == "deb":
                install_deb(app["identifier"], log_callback)
            
            if app.get("script"):
                run_post_install_script(app["script"], log_callback)
                
            self.log_signal.emit(f"=== Finished Installation: {app['name']} ===\n")
            
        self.finished_signal.emit()


class AppListItem(QWidget):
    def __init__(self, app_data, edit_callback=None, delete_callback=None):
        super().__init__()
        self.app_data = app_data
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # Tooltip for the whole item with description
        tooltip_text = f"<b>{app_data['name']}</b> ({app_data['type']})<br/>{app_data['description']}<br/>Identifier: {app_data['identifier']}"
        self.setToolTip(tooltip_text)
        
        icon_label = QLabel()
        if app_data.get("icon"):
            pixmap = QPixmap(app_data["icon"])
            if not pixmap.isNull():
                icon_label.setPixmap(pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setFixedSize(32, 32)
        layout.addWidget(icon_label)
        
        self.checkbox = QCheckBox(app_data["name"])
        self.checkbox.setStyleSheet("font-weight: bold; font-size: 15px;")
        layout.addWidget(self.checkbox)
        
        desc = QLabel(f"({app_data['type']}) {app_data['description']}")
        desc.setStyleSheet("color: #bac2de;")
        layout.addWidget(desc)
        layout.addStretch()
        
        if edit_callback:
            edit_btn = QPushButton("✎ Edit")
            edit_btn.setFixedSize(60, 26)
            edit_btn.setStyleSheet("""
                QPushButton { background-color: #f9e2af; color: #11111b; border-radius: 4px; padding: 4px;}
                QPushButton:hover { background-color: #f2cd8ae0; }
            """)
            edit_btn.clicked.connect(lambda checked, a=app_data: edit_callback(a))
            layout.addWidget(edit_btn)
            
        if delete_callback:
            del_btn = QPushButton("✖ Delete")
            del_btn.setFixedSize(70, 26)
            del_btn.setStyleSheet("""
                QPushButton { background-color: #f38ba8; color: #11111b; border-radius: 4px; padding: 4px;}
                QPushButton:hover { background-color: #eba0b6; }
            """)
            del_btn.clicked.connect(lambda checked, a=app_data: delete_callback(a))
            layout.addWidget(del_btn)

    def is_selected(self):
        return self.checkbox.isChecked()


STYLESHEET = """
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}
QListWidget {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 5px;
}
QListWidget::item {
    border-bottom: 1px solid #313244;
    padding: 5px;
}
QListWidget::item:hover {
    background-color: #313244;
    border-radius: 4px;
}
QPushButton {
    background-color: #89b4fa;
    color: #11111b;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #b4befe;
}
QPushButton:disabled {
    background-color: #45475a;
    color: #a6adc8;
}
QTextEdit, QLineEdit, QComboBox {
    background-color: #11111b;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 6px;
    padding: 6px;
}
QTextEdit {
    color: #a6e3a1;
    font-family: monospace;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #585b70;
}
QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
}
QDialog {
    background-color: #1e1e2e;
}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ubuntu AutoInstall")
        self.setWindowIcon(QIcon("app_icon.png"))
        self.resize(850, 700)
        self.setStyleSheet(STYLESHEET)
        
        self.apps = load_config()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        main_widget.setLayout(layout)
        
        title_label = QLabel("Ubuntu Package Installer")
        title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #89b4fa; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search applications (Name, Description, Type)...")
        self.search_bar.textChanged.connect(self.filter_list)
        layout.addWidget(self.search_bar)
        
        list_header_layout = QHBoxLayout()
        self.select_all_cb = QCheckBox("Select All")
        self.select_all_cb.setStyleSheet("font-weight: bold; color: #89b4fa;")
        self.select_all_cb.stateChanged.connect(self.toggle_select_all)
        list_header_layout.addWidget(self.select_all_cb)
        layout.addLayout(list_header_layout)
        
        self.list_widget = QListWidget()
        self.search_bar.setPlaceholderText("Search applications (Name, Description, Type)...")
        self.search_bar.textChanged.connect(self.filter_list)
        layout.addWidget(self.search_bar)
        
        layout.addWidget(self.list_widget, stretch=2)
        
        self.populate_list()
        
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Application")
        self.add_btn.clicked.connect(self.add_application)
        btn_layout.addWidget(self.add_btn)
        
        self.install_btn = QPushButton("Install Selected")
        self.install_btn.clicked.connect(self.install_selected)
        btn_layout.addWidget(self.install_btn)
        
        layout.addLayout(btn_layout)
        
        log_label = QLabel("Installation Logs")
        log_label.setStyleSheet("font-weight: bold; margin-top: 10px; font-size: 14px;")
        layout.addWidget(log_label)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output, stretch=1)
        
        self.worker = None

    def populate_list(self):
        self.list_widget.clear()
        for app in self.apps:
            item = QListWidgetItem(self.list_widget)
            widget = AppListItem(app, self.edit_application, self.delete_application)
            item.setSizeHint(widget.sizeHint())
            self.list_widget.setItemWidget(item, widget)

    def filter_list(self, text):
        search_term = text.lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            app = widget.app_data
            
            # Simple full-text search across relevant fields
            match = (search_term in app.get('name', '').lower() or 
                     search_term in app.get('description', '').lower() or 
                     search_term in app.get('type', '').lower())
                     
            item.setHidden(not match)

    def toggle_select_all(self, state):
        should_check = state == Qt.CheckState.Checked.value
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            # Only toggle items that are currently visible (matching the search filter)
            if not item.isHidden():
                widget = self.list_widget.itemWidget(item)
                widget.checkbox.setChecked(should_check)

    def edit_application(self, app_data):
        dialog = AddAppDialog(self, app_data)
        dialog.setStyleSheet(STYLESHEET)
        if dialog.exec():
            updated_app = dialog.get_app_data()
            try:
                idx = self.apps.index(app_data)
                self.apps[idx] = updated_app
            except ValueError:
                self.apps.append(updated_app)
            save_config(self.apps)
            self.populate_list()
            self.log_message(f"Application '{updated_app['name']}' updated.")
            
    def delete_application(self, app_data):
        if app_data in self.apps:
            self.apps.remove(app_data)
            save_config(self.apps)
            self.populate_list()
            self.log_message(f"Application '{app_data['name']}' deleted.")

    def add_application(self):
        dialog = AddAppDialog(self)
        dialog.setStyleSheet(STYLESHEET)
        if dialog.exec():
            new_app = dialog.get_app_data()
            self.apps.append(new_app)
            save_config(self.apps)
            self.populate_list()

    def log_message(self, msg):
        self.log_output.append(msg)
        
        # Scroll to bottom
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def installation_finished(self):
        self.install_btn.setEnabled(True)
        self.add_btn.setEnabled(True)
        self.list_widget.setEnabled(True)
        self.log_message("--- All selected installations completed ---")

    def install_selected(self):
        apps_to_install = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            if widget.is_selected():
                apps_to_install.append(widget.app_data)
                
        if not apps_to_install:
            self.log_message("No applications selected.")
            return
            
        self.install_btn.setEnabled(False)
        self.add_btn.setEnabled(False)
        self.list_widget.setEnabled(False)
        self.log_output.clear()
        self.log_message(f"Preparing to process {len(apps_to_install)} application(s)...")
        
        self.worker = InstallWorker(apps_to_install)
        self.worker.log_signal.connect(self.log_message)
        self.worker.finished_signal.connect(self.installation_finished)
        self.worker.start()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
