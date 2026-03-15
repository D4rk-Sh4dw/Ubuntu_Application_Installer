from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QFileDialog, QHBoxLayout

class AddAppDialog(QDialog):
    def __init__(self, parent=None, app_data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Application" if app_data else "Add Application")
        self.resize(400, 300)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.desc_input = QLineEdit()
        
        self.type_input = QComboBox()
        self.type_input.addItems(["apt", "snap", "flatpak", "deb", "none"])
        
        self.identifier_input = QLineEdit()
        self.icon_path_input = QLineEdit()
        
        if app_data:
            self.name_input.setText(app_data.get("name", ""))
            self.desc_input.setText(app_data.get("description", ""))
            self.type_input.setCurrentText(app_data.get("type", "apt"))
            self.identifier_input.setText(app_data.get("identifier", ""))
            self.icon_path_input.setText(app_data.get("icon", ""))
        
        self.icon_btn = QPushButton("Browse...")
        self.icon_btn.clicked.connect(self.browse_icon)
        
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_path_input)
        icon_layout.addWidget(self.icon_btn)
        
        self.pre_script_path_input = QLineEdit()
        if app_data:
            self.pre_script_path_input.setText(app_data.get("pre_script", ""))
            
        self.pre_script_btn = QPushButton("Browse...")
        self.pre_script_btn.clicked.connect(self.browse_pre_script)
        
        pre_script_layout = QHBoxLayout()
        pre_script_layout.addWidget(self.pre_script_path_input)
        pre_script_layout.addWidget(self.pre_script_btn)

        self.script_path_input = QLineEdit()
        if app_data:
            self.script_path_input.setText(app_data.get("script", ""))
            
        self.script_btn = QPushButton("Browse...")
        self.script_btn.clicked.connect(self.browse_script)
        
        script_layout = QHBoxLayout()
        script_layout.addWidget(self.script_path_input)
        script_layout.addWidget(self.script_btn)
        
        self.form_layout.addRow("Name:", self.name_input)
        self.form_layout.addRow("Description:", self.desc_input)
        self.form_layout.addRow("Package Type:", self.type_input)
        self.form_layout.addRow("Identifier/URL:", self.identifier_input)
        self.form_layout.addRow("Icon Path:", icon_layout)
        self.form_layout.addRow("Pre-Install Script:", pre_script_layout)
        self.form_layout.addRow("Post-Install Script:", script_layout)
        
        self.layout.addLayout(self.form_layout)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.layout.addWidget(self.save_btn)

    def browse_icon(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Icon", "", "Images (*.png *.xpm *.jpg *.svg)")
        if filename:
            self.icon_path_input.setText(filename)
            
    def browse_pre_script(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Pre-Script", "", "Shell Scripts (*.sh);;All Files (*)")
        if filename:
            self.pre_script_path_input.setText(filename)

    def browse_script(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Script", "", "Shell Scripts (*.sh);;All Files (*)")
        if filename:
            self.script_path_input.setText(filename)

    def get_app_data(self):
        return {
            "name": self.name_input.text(),
            "description": self.desc_input.text(),
            "type": self.type_input.currentText(),
            "identifier": self.identifier_input.text(),
            "icon": self.icon_path_input.text(),
            "pre_script": self.pre_script_path_input.text(),
            "script": self.script_path_input.text()
        }
