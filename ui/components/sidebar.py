from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

from ..styles.colors import *

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.is_collapsed = False
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedWidth(220)
        self.setStyleSheet(f"background-color: {DARK_BG}; border-left: 1px solid {DARK_BORDER};")
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar header
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet(f"background-color: {DARK_BG}; border-bottom: 1px solid {DARK_BORDER};")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(13, 0, 13, 0)
        
        self.logo = QLabel("Fanus")
        self.logo.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        
        self.profile = QLabel("U")
        self.profile.setFixedSize(36, 36)
        self.profile.setStyleSheet(f"""
            QLabel {{
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 {PRIMARY_COLOR}, stop: 1 {PRIMARY_LIGHT});
                color: white;
                font-weight: bold;
                border-radius: 18px;
                qproperty-alignment: AlignCenter;
            }}
        """)
        
        header_layout.addWidget(self.profile)
        header_layout.addWidget(self.logo)
        header_layout.addStretch()
        
        # Menu items
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {DARK_BG};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {DARK_BG};
                width: 5px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {PRIMARY_COLOR};
                border-radius: 2px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_widget)
        self.menu_layout.setContentsMargins(10, 13, 10, 13)
        self.menu_layout.setSpacing(4)
        
        # Create menu items
        self.create_menu_items()
        
        self.menu_layout.addStretch()
        
        scroll_area.setWidget(self.menu_widget)
        
        # Add widgets to sidebar
        layout.addWidget(header)
        layout.addWidget(scroll_area)
        
        # Toggle button
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(28, 28)
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_BG};
                border: 1px solid {DARK_BORDER};
                border-radius: 14px;
                color: {DARK_TEXT};
            }}
            QPushButton:hover {{
                background-color: {DARK_HOVER};
            }}
        """)
        self.toggle_btn.setText("→")
        
        # Connect toggle button
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
    def create_menu_items(self):
        # Home
        self.add_menu_item("صفحه اصلی", "home", "🏠")
        
        # Settings
        self.add_menu_item("تنظیمات", "settings", "⚙️")
        
        # Robots menu with submenu
        robots_item = self.add_menu_item("ربات ها", None, "🤖", has_submenu=True)
        
        # Submenu for robots
        submenu_frame = QFrame()
        submenu_frame.setStyleSheet(f"background-color: rgba(42, 42, 61, 0.7); border-radius: 6px; margin: 5px 0px;")
        submenu_layout = QVBoxLayout(submenu_frame)
        submenu_layout.setContentsMargins(15, 8, 15, 8)
        submenu_layout.setSpacing(3)
        
        # Submenu items
        self.add_submenu_item(submenu_layout, "ربات وام ازدواج", "marriage-loan", "❤️")
        self.add_submenu_item(submenu_layout, "ربات وام فرزند", "child-loan", "👶")
        
        self.menu_layout.addWidget(submenu_frame)
        
        # News
        self.add_menu_item("اخبار", "news", "📰")
        
        # Education
        self.add_menu_item("آموزش ها", "education", "🎓")
        
        # Contact
        self.add_menu_item("ارتباط با ما", "contact", "✉️")
    
    def add_menu_item(self, text, page, icon, has_submenu=False):
        btn = QPushButton()
        btn.setProperty('page', page)
        btn.setProperty('has_submenu', has_submenu)
        btn.setProperty('text', text)
        btn.setProperty('icon', icon)
        btn.setCursor(Qt.PointingHandCursor)
        
        # Create layout for icon and text
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(15, 10, 15, 10)
        btn_layout.setSpacing(10)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"color: {DARK_TEXT}; font-size: 16px;")
        
        text_label = QLabel(text)
        text_label.setStyleSheet(f"color: {DARK_TEXT}; font-size: 14px;")
        text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()
        
        # Set style with hover effects
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {DARK_SECONDARY};
                color: {DARK_TEXT};
                border: none;
                border-radius: 8px;
                text-align: right;
            }}
            QPushButton:hover {{
                background-color: {DARK_HOVER};
                padding-right: 3px;
            }}
            QPushButton:pressed {{
                background-color: {DARK_ACTIVE};
                color: white;
            }}
        """)
        
        # Connect click event
        if page:
            btn.clicked.connect(lambda: self.parent.change_page(page))
        elif has_submenu:
            btn.clicked.connect(self.toggle_submenu)
        
        self.menu_layout.addWidget(btn)
        return btn
    
    def add_submenu_item(self, layout, text, page, icon):
        btn = QPushButton()
        btn.setProperty('page', page)
        btn.setProperty('text', text)
        btn.setProperty('icon', icon)
        btn.setCursor(Qt.PointingHandCursor)
        
        # Create layout for icon and text
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(12, 8, 12, 8)
        btn_layout.setSpacing(8)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"color: {DARK_TEXT}; font-size: 14px;")
        
        text_label = QLabel(text)
        text_label.setStyleSheet(f"color: {DARK_TEXT}; font-size: 13px;")
        text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label)
        btn_layout.addStretch()
        
        # Set style with hover effects
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(42, 42, 61, 0.7);
                color: {DARK_TEXT};
                border: none;
                border-radius: 6px;
                text-align: right;
            }}
            QPushButton:hover {{
                background-color: {DARK_HOVER};
                padding-right: 3px;
                opacity: 1;
            }}
            QPushButton:pressed {{
                background-color: {PRIMARY_DARK};
                color: white;
                font-weight: bold;
            }}
        """)
        
        # Connect click event
        btn.clicked.connect(lambda: self.parent.change_page(page))
        
        layout.addWidget(btn)
        return btn
    
    def toggle_submenu(self):
        # This would toggle the submenu visibility
        pass
        
    def toggle_sidebar(self):
        if self.is_collapsed:
            self.expand()
        else:
            self.collapse()
    
    def collapse(self):
        self.setFixedWidth(80)
        self.is_collapsed = True
        self.toggle_btn.setText("←")
        self.logo.hide()
        
        # Hide text in all buttons, show only icons
        for i in range(self.menu_layout.count()):
            item = self.menu_layout.itemAt(i)
            if item.widget() and isinstance(item.widget(), QPushButton):
                text_label = item.widget().findChild(QLabel, None)
                if text_label and text_label.property('text'):
                    text_label.hide()
    
    def expand(self):
        self.setFixedWidth(220)
        self.is_collapsed = False
        self.toggle_btn.setText("→")
        self.logo.show()
        
        # Show text in all buttons
        for i in range(self.menu_layout.count()):
            item = self.menu_layout.itemAt(i)
            if item.widget() and isinstance(item.widget(), QPushButton):
                text_label = item.widget().findChild(QLabel, None)
                if text_label:
                    text_label.show()
    
    def resizeEvent(self, event):
        # Position toggle button
        self.toggle_btn.move(self.width() - 14, self.height() // 2 - 14)
        super().resizeEvent(event)