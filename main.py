import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QScrollArea, 
                             QFrame, QSizePolicy, QStackedWidget)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QPainter, QBrush
from PyQt5.QtSvg import QSvgWidget

class RoundedButton(QPushButton):
    def __init__(self, icon=None, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2A2A3D;
                color: #E0E0E0;
                border: none;
                border-radius: 8px;
                padding: 10px;
                text-align: right;
            }
            QPushButton:hover {
                background-color: #3A3A4D;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        
        if icon:
            # For simplicity, using text as icon. In real app, use QIcon with SVG
            self.setIcon(icon)

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setStyleSheet("background-color: #1E1E2D; border-left: 1px solid #3D3D50;")
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar header
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #1E1E2D; border-bottom: 1px solid #3D3D50;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(13, 0, 13, 0)
        
        self.logo = QLabel("Fanus")
        self.logo.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        
        self.profile = QLabel("U")
        self.profile.setFixedSize(36, 36)
        self.profile.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #2563eb, stop: 1 #3b82f6);
                color: white;
                font-weight: bold;
                border-radius: 18px;
                qproperty-alignment: AlignCenter;
            }
        """)
        
        header_layout.addWidget(self.profile)
        header_layout.addWidget(self.logo)
        header_layout.addStretch()
        
        # Menu items
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1E1E2D;
            }
            QScrollBar:vertical {
                border: none;
                background: #1E1E2D;
                width: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #2563eb;
                border-radius: 2px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        menu_widget = QWidget()
        menu_layout = QVBoxLayout(menu_widget)
        menu_layout.setContentsMargins(10, 13, 10, 13)
        menu_layout.setSpacing(4)
        
        # Menu items
        self.menu_items = []
        
        # Home
        home_btn = RoundedButton(text="صفحه اصلی")
        home_btn.setProperty('page', 'home')
        menu_layout.addWidget(home_btn)
        self.menu_items.append(home_btn)
        
        # Settings
        settings_btn = RoundedButton(text="تنظیمات")
        settings_btn.setProperty('page', 'settings')
        menu_layout.addWidget(settings_btn)
        self.menu_items.append(settings_btn)
        
        # Robots menu
        robots_btn = RoundedButton(text="ربات ها")
        robots_btn.setProperty('has_submenu', True)
        menu_layout.addWidget(robots_btn)
        self.menu_items.append(robots_btn)
        
        # Submenu for robots
        submenu_frame = QFrame()
        submenu_frame.setStyleSheet("background-color: rgba(42, 42, 61, 0.7); border-radius: 6px;")
        submenu_layout = QVBoxLayout(submenu_frame)
        submenu_layout.setContentsMargins(15, 8, 15, 8)
        submenu_layout.setSpacing(3)
        
        marriage_loan_btn = RoundedButton(text="ربات وام ازدواج")
        marriage_loan_btn.setProperty('page', 'marriage-loan')
        marriage_loan_btn.setStyleSheet(marriage_loan_btn.styleSheet() + "font-size: 13px;")
        submenu_layout.addWidget(marriage_loan_btn)
        self.menu_items.append(marriage_loan_btn)
        
        child_loan_btn = RoundedButton(text="ربات وام فرزند")
        child_loan_btn.setProperty('page', 'child-loan')
        child_loan_btn.setStyleSheet(child_loan_btn.styleSheet() + "font-size: 13px;")
        submenu_layout.addWidget(child_loan_btn)
        self.menu_items.append(child_loan_btn)
        
        menu_layout.addWidget(submenu_frame)
        
        # News
        news_btn = RoundedButton(text="اخبار")
        news_btn.setProperty('page', 'news')
        menu_layout.addWidget(news_btn)
        self.menu_items.append(news_btn)
        
        # Education
        education_btn = RoundedButton(text="آموزش ها")
        education_btn.setProperty('page', 'education')
        menu_layout.addWidget(education_btn)
        self.menu_items.append(education_btn)
        
        # Contact
        contact_btn = RoundedButton(text="ارتباط با ما")
        contact_btn.setProperty('page', 'contact')
        menu_layout.addWidget(contact_btn)
        self.menu_items.append(contact_btn)
        
        menu_layout.addStretch()
        
        scroll_area.setWidget(menu_widget)
        
        # Add widgets to sidebar
        layout.addWidget(header)
        layout.addWidget(scroll_area)
        
        # Toggle button
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(28, 28)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E1E2D;
                border: 1px solid #3D3D50;
                border-radius: 14px;
                color: #E0E0E0;
            }
            QPushButton:hover {
                background-color: #3A3A4D;
            }
        """)
        self.toggle_btn.setText("←")  # Using text instead of icon for simplicity
        
        # Connect toggle button
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
    def toggle_sidebar(self):
        # This would be connected to the parent window to handle collapsing
        pass
        
    def resizeEvent(self, event):
        # Position toggle button
        self.toggle_btn.move(-14, self.height() // 2 - 14)
        super().resizeEvent(event)

class TopMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setStyleSheet("background-color: #2A2A3D; border-bottom: 1px solid #3D3D50;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        self.title = QLabel("صفحه اصلی")
        self.title.setStyleSheet("color: #E0E0E0; font-size: 18px; font-weight: bold;")
        
        self.menu_items = QWidget()
        menu_layout = QHBoxLayout(self.menu_items)
        menu_layout.setSpacing(10)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.menu_items)

class MainContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        self.stacked_widget = QStackedWidget()
        
        # Home content
        home_content = QWidget()
        home_layout = QVBoxLayout(home_content)
        home_title = QLabel("صفحه اصلی")
        home_title.setStyleSheet("color: #3b82f6; font-size: 18px; padding-bottom: 10px; border-bottom: 1px solid #3D3D50;")
        home_text = QLabel("به سامانه Fanus خوش آمدید. از منوی سمت راست بخش مورد نظر خود را انتخاب کنید.")
        home_text.setStyleSheet("color: #E0E0E0;")
        home_layout.addWidget(home_title)
        home_layout.addWidget(home_text)
        home_layout.addStretch()
        self.stacked_widget.addWidget(home_content)
        
        # Add other content pages similarly...
        # For brevity, I'm only implementing the home page
        
        layout.addWidget(self.stacked_widget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سایدبار Fanus")
        self.setGeometry(100, 100, 1200, 700)
        
        # Set background color
        self.setStyleSheet("background-color: #0F0F1A;")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Right side container (top menu + main content)
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setSpacing(0)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top menu
        self.top_menu = TopMenu()
        right_layout.addWidget(self.top_menu)
        
        # Main content
        self.main_content = MainContent()
        right_layout.addWidget(self.main_content)
        
        main_layout.addWidget(right_container)
        
        # Add toggle button to sidebar (needs to be on top of other widgets)
        self.sidebar.toggle_btn.setParent(self)
        self.sidebar.toggle_btn.show()
        
        # Connect toggle button
        self.sidebar.toggle_btn.clicked.connect(self.toggle_sidebar)
        
        # Connect menu items
        for item in self.sidebar.menu_items:
            if item.property('page'):
                item.clicked.connect(lambda checked, p=item.property('page'): self.change_page(p))
    
    def toggle_sidebar(self):
        current_width = self.sidebar.width()
        if current_width == 220:
            # Collapse sidebar
            self.sidebar.setFixedWidth(80)
            self.sidebar.logo.hide()
            # Update toggle button text
            self.sidebar.toggle_btn.setText("→")
        else:
            # Expand sidebar
            self.sidebar.setFixedWidth(220)
            self.sidebar.logo.show()
            # Update toggle button text
            self.sidebar.toggle_btn.setText("←")
    
    def change_page(self, page_name):
        # Change the page content based on page_name
        # This would update the stacked widget in main_content
        # and update the top menu
        pass
    
    def resizeEvent(self, event):
        # Reposition toggle button when window is resized
        self.sidebar.toggle_btn.move(self.sidebar.width() - 14, self.height() // 2 - 14)
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application font (using a default font that supports RTL)
    font = QFont("Arial", 10)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())