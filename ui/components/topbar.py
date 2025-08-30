from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from ui.styles.colors import *

class TopMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedHeight(60)
        self.setStyleSheet(f"background-color: {DARK_SECONDARY}; border-bottom: 1px solid {DARK_BORDER};")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Title with icon
        self.title_widget = QWidget()
        title_layout = QHBoxLayout(self.title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        
        self.title_icon = QLabel()
        self.title_icon.setFixedSize(20, 20)
        self.title_icon.setStyleSheet("color: #3b82f6; font-size: 16px;")
        
        self.title_text = QLabel("صفحه اصلی")
        self.title_text.setStyleSheet(f"color: {DARK_TEXT}; font-size: 18px; font-weight: bold;")
        
        title_layout.addWidget(self.title_icon)
        title_layout.addWidget(self.title_text)
        title_layout.addStretch()
        
        layout.addWidget(self.title_widget)
        layout.addStretch()
        
        # Menu items
        self.menu_items_widget = QWidget()
        self.menu_layout = QHBoxLayout(self.menu_items_widget)
        self.menu_layout.setSpacing(10)
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(self.menu_items_widget)
    
    def update_menu(self, title, icon, items):
        self.title_text.setText(title)
        self.title_icon.setText(icon)
        
        # Clear existing items
        for i in reversed(range(self.menu_layout.count())): 
            self.menu_layout.itemAt(i).widget().setParent(None)
        
        # Add new items
        for item in items:
            btn = QPushButton(item['text'])
            btn.setProperty('icon', item['icon'])
            btn.setCursor(Qt.PointingHandCursor)
            
            # Set style with hover effects
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(42, 42, 61, 0.7);
                    color: {DARK_TEXT};
                    border: 1px solid {DARK_BORDER};
                    border-radius: 6px;
                    padding: 8px 15px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {DARK_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: {DARK_ACTIVE};
                    color: white;
                    border-color: {PRIMARY_COLOR};
                }}
            """)
            
            if item.get('active', False):
                btn.setStyleSheet(btn.styleSheet() + f"""
                    QPushButton {{
                        background-color: {DARK_ACTIVE};
                        color: white;
                        border-color: {PRIMARY_COLOR};
                    }}
                """)
            
            self.menu_layout.addWidget(btn)