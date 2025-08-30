from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QStackedWidget)
from PyQt5.QtCore import Qt

from ui.components.sidebar import Sidebar
from ui.components.topbar import TopMenu
from ui.pages.home_page import HomePage
from ui.pages.base_page import BasePage
from ui.styles.colors import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سایدبار Fanus")
        self.setGeometry(100, 100, 1200, 700)
        
        # Set background color
        self.setStyleSheet(f"background-color: #0F0F1A;")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Right side container (top menu + main content)
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setSpacing(0)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top menu
        self.top_menu = TopMenu(self)
        right_layout.addWidget(self.top_menu)
        
        # Main content
        self.main_content = QWidget()
        main_content_layout = QVBoxLayout(self.main_content)
        main_content_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {DARK_SECONDARY};
                border-radius: 10px;
                border: 1px solid {DARK_BORDER};
                margin: 20px;
            }}
        """)
        main_content_layout.addWidget(self.stacked_widget)
        
        right_layout.addWidget(self.main_content)
        
        # Add right container first (left side)
        main_layout.addWidget(right_container)
        
        # Create sidebar (right side)
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)
        
        # Add toggle button to sidebar (needs to be on top of other widgets)
        self.sidebar.toggle_btn.setParent(self)
        self.sidebar.toggle_btn.show()
        
        # Create pages
        self.create_pages()
        
        # Set initial page
        self.change_page('home')
    
    def create_pages(self):
        # Home page
        home_page = HomePage()
        self.stacked_widget.addWidget(home_page)
        
        # Other pages
        settings_page = BasePage("تنظیمات سیستم", "این بخش مربوط به تنظیمات کلی سیستم می‌باشد.")
        self.stacked_widget.addWidget(settings_page)
        
        marriage_loan_page = BasePage("ربات وام ازدواج", "این بخش مربوط به مدیریت وام ازدواج می‌باشد.")
        self.stacked_widget.addWidget(marriage_loan_page)
        
        child_loan_page = BasePage("ربات وام فرزند", "این بخش مربوط به مدیریت وام فرزند می‌باشد.")
        self.stacked_widget.addWidget(child_loan_page)
        
        news_page = BasePage("اخبار و اطلاعیه‌ها", "آخرین اخبار و اطلاعیه‌های سیستم در این بخش نمایش داده می‌شود.")
        self.stacked_widget.addWidget(news_page)
        
        education_page = BasePage("آموزش‌های سیستم", "آموزش‌های مربوط به استفاده از سیستم در این بخش قرار دارد.")
        self.stacked_widget.addWidget(education_page)
        
        contact_page = BasePage("ارتباط با ما", "راه‌های ارتباطی با پشتیبانی سیستم در این بخش قرار دارد.")
        self.stacked_widget.addWidget(contact_page)
    
    def change_page(self, page_name):
        page_index = {
            'home': 0,
            'settings': 1,
            'marriage-loan': 2,
            'child-loan': 3,
            'news': 4,
            'education': 5,
            'contact': 6
        }.get(page_name, 0)
        
        self.stacked_widget.setCurrentIndex(page_index)
        
        # Update top menu based on page
        menu_templates = {
            'home': {
                'title': 'صفحه اصلی',
                'icon': 'fas fa-home',
                'items': []
            },
            'settings': {
                'title': 'تنظیمات سیستم',
                'icon': 'fas fa-cog',
                'items': []
            },
            'marriage-loan': {
                'title': 'ربات وام ازدواج',
                'icon': 'fas fa-heart',
                'items': [
                    {'icon': 'fas fa-cog', 'text': 'تنظیمات وام', 'active': True},
                    {'icon': 'fas fa-graduation-cap', 'text': 'آموزش استفاده'},
                    {'icon': 'fas fa-users', 'text': 'متقاضیان'},
                    {'icon': 'fas fa-bell', 'text': 'اطلاع‌رسانی'}
                ]
            },
            'child-loan': {
                'title': 'ربات وام فرزند',
                'icon': 'fas fa-baby',
                'items': [
                    {'icon': 'fas fa-cog', 'text': 'تنظیمات وام', 'active': True},
                    {'icon': 'fas fa-graduation-cap', 'text': 'آموزش استفاده'},
                    {'icon': 'fas fa-users', 'text': 'متقاضیان'},
                    {'icon': 'fas fa-bell', 'text': 'اطلاع‌رسانی'}
                ]
            },
            'news': {
                'title': 'اخبار و اطلاعیه‌ها',
                'icon': 'fas fa-newspaper',
                'items': []
            },
            'education': {
                'title': 'آموزش‌های سیستم',
                'icon': 'fas fa-graduation-cap',
                'items': [
                    {'icon': 'fas fa-heart', 'text': 'آموزش وام ازدواج'},
                    {'icon': 'fas fa-baby', 'text': 'آموزش وام فرزند', 'active': True},
                    {'icon': 'fas fa-cog', 'text': 'آموزش تنظیمات'}
                ]
            },
            'contact': {
                'title': 'ارتباط با ما',
                'icon': 'fas fa-envelope',
                'items': []
            }
        }
        
        template = menu_templates.get(page_name, menu_templates['home'])
        self.top_menu.update_menu(template['title'], template['icon'], template['items'])
    
    def resizeEvent(self, event):
        # Reposition toggle button when window is resized
        self.sidebar.toggle_btn.move(self.sidebar.width() - 14, self.height() // 2 - 14)
        super().resizeEvent(event)