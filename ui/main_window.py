#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                            QVBoxLayout, QStackedWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .ui_styles import UIStyles
from .sidebar_component import CollapsibleSidebar
from .top_navigation import TopNavigation

# صفحات مختلف
from .pages.home_page import HomePage
from .pages.other_pages import SettingsPage, NewsPage, EducationPage, ContactPage
from .pages.robots.marriage_loan_robot import MarriageLoanRobot
from .pages.robots.child_loan_robot import ChildLoanRobot

class MainWindow(QMainWindow):
    """پنجره اصلی برنامه YARA"""
    
    def __init__(self):
        super().__init__()
        self.setObjectName("mainWindow")
        
        # تنظیمات پنجره
        self.setWindowTitle("YARA - سامانه مدیریت وام")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # تنظیم استایل کلی
        self.setStyleSheet(UIStyles.get_main_window_style())
        
        # ایجاد رابط کاربری
        self.setup_ui()
        
        # اتصال سیگنال‌ها
        self.connect_signals()
        
        # نمایش صفحه اولیه
        self.show_page("home")
        
    def setup_ui(self):
        """تنظیم رابط کاربری اصلی"""
        # ویجت مرکزی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout اصلی
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = CollapsibleSidebar()
        
        # ناحیه محتوای اصلی
        self.create_content_area()
        
        # اضافه کردن به layout
        main_layout.addWidget(self.content_area)
        main_layout.addWidget(self.sidebar)  # سمت راست
        
    def create_content_area(self):
        """ایجاد ناحیه محتوای اصلی"""
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        self.content_area.setStyleSheet(UIStyles.get_content_area_style())
        
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # منوی بالایی
        self.top_navigation = TopNavigation()
        
        # Stack widget برای صفحات مختلف
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("QStackedWidget { background-color: transparent; }")
        
        # ایجاد صفحات
        self.create_pages()
        
        content_layout.addWidget(self.top_navigation)
        content_layout.addWidget(self.stacked_widget)
        
    def create_pages(self):
        """ایجاد تمام صفحات"""
        # صفحه اصلی
        self.home_page = HomePage()
        self.stacked_widget.addWidget(self.home_page)
        
        # صفحه تنظیمات
        self.settings_page = SettingsPage()
        self.stacked_widget.addWidget(self.settings_page)
        
        # ربات وام ازدواج
        self.marriage_loan_page = MarriageLoanRobot()
        self.stacked_widget.addWidget(self.marriage_loan_page)
        
        # ربات وام فرزند
        self.child_loan_page = ChildLoanRobot()
        self.stacked_widget.addWidget(self.child_loan_page)
        
        # صفحه اخبار
        self.news_page = NewsPage()
        self.stacked_widget.addWidget(self.news_page)
        
        # صفحه آموزش‌ها
        self.education_page = EducationPage()
        self.stacked_widget.addWidget(self.education_page)
        
        # صفحه ارتباط با ما
        self.contact_page = ContactPage()
        self.stacked_widget.addWidget(self.contact_page)
        
        # نقشه صفحات
        self.pages_map = {
            "home": self.home_page,
            "settings": self.settings_page,
            "marriage-loan": self.marriage_loan_page,
            "child-loan": self.child_loan_page,
            "news": self.news_page,
            "education": self.education_page,
            "contact": self.contact_page
        }
        
    def connect_signals(self):
        """اتصال سیگنال‌ها"""
        # سیگنال کلیک منوی sidebar
        self.sidebar.menu_clicked.connect(self.show_page)
        
        # سیگنال منوی بالایی
        self.top_navigation.top_menu_clicked.connect(self.handle_top_menu_click)
        
    def show_page(self, page_id):
        """نمایش صفحه مشخص"""
        if page_id in self.pages_map:
            # تغییر صفحه
            page_widget = self.pages_map[page_id]
            self.stacked_widget.setCurrentWidget(page_widget)
            
            # بروزرسانی منوی بالایی
            self.top_navigation.update_menu(page_id)
            
            # تنظیم منوی فعال در sidebar
            self.sidebar.set_active_menu(page_id)
            
            # فراخوانی متد activate صفحه (اگر موجود باشد)
            if hasattr(page_widget, 'activate'):
                page_widget.activate()
                
    def handle_top_menu_click(self, button_id):
        """مدیریت کلیک روی منوی بالایی"""
        # دریافت صفحه فعلی
        current_page = self.stacked_widget.currentWidget()
        
        # ارسال سیگنال به صفحه فعلی
        if hasattr(current_page, 'handle_top_menu_action'):
            current_page.handle_top_menu_action(button_id)
            
    def resizeEvent(self, event):
        """تنظیم layout هنگام تغییر سایز پنجره"""
        super().resizeEvent(event)
        # می‌توان اینجا تنظیمات responsive اضافه کرد


def main():
    """تابع اصلی برنامه"""
    app = QApplication(sys.argv)
    
    # تنظیم فونت پیش‌فرض
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # ایجاد و نمایش پنجره اصلی
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()