#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QMessageBox, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from models.applicant import Applicant, ApplicantStatus
from services.data_service import DataService

# Import کامپوننت‌های جدید
try:
    from ui.sidebar_component import CollapsibleSidebar
    from ui.top_navigation import ModernTopBar
    from ui.ui_styles import UIStyles
    from ui.form_handler import FormHandler
    from ui.robot_controller import RobotController
    from ui.page_manager import PageManager
except ImportError as e:
    print(f"خطا در import: {e}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.data_service = DataService()
        self.current_page = "home"
        self.current_applicant = None
        self.main_content = None
        
        # کامپوننت‌های UI - با کنترل خطا
        try:
            self.form_handler = FormHandler(self)
            self.robot_controller = RobotController(self)
            self.page_manager = PageManager(self)
        except Exception as e:
            QMessageBox.critical(None, "خطای ایمپورت", 
                f"خطا در بارگذاری ماژول‌های UI:\n{str(e)}")
            QApplication.instance().quit()
            return
        
        # داده‌های استاتیک
        self.iran_banks = [
            "بانک ملی ایران", "بانک صادرات ایران", "بانک تجارت", 
            "بانک رفاه کارگران", "بانک کشاورزی", "بانک مسکن",
            "بانک صنعت و معدن", "بانک سپه", "بانک پست بانک ایران",
            "بانک دی", "بانک پارسیان", "بانک پاسارگاد", "بانک کارآفرین",
            "بانک سامان", "بانک سینا", "بانک شهر", "بانک توسعه تعاون",
            "بانک اقتصاد نوین", "بانک آینده", "بانک انصار", "بانک ایران زمین"
        ]
        
        self.provinces_cities = {
            "آذربایجان شرقی": ["تبریز", "مراغه", "میانه", "مرند", "اهر"],
            "آذربایجان غربی": ["ارومیه", "خوی", "مهاباد", "نقده", "سلماس"],
            "اردبیل": ["اردبیل", "مشگین شهر", "پارس آباد", "خلخال"],
            "اصفهان": ["اصفهان", "کاشان", "خمینی شهر", "نجف آباد"],
            "تهران": ["تهران", "ورامین", "شهریار", "اسلامشهر"],
            "خراسان رضوی": ["مشهد", "نیشابور", "سبزوار", "کاشمر"],
            "فارس": ["شیراز", "کازرون", "فسا", "داراب"],
            "گیلان": ["رشت", "انزلی", "لاهیجان", "لنگرود"]
        }
        
        self.months = [
            "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
            "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
        ]
        
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        """تنظیم رابط کاربری اصلی"""
        self.setWindowTitle("YARA - سیستم مدیریت ربات‌های خودکار")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)
        
        # استایل کلی پنجره
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {UIStyles.COLORS['bg_primary']};
                color: {UIStyles.COLORS['text_primary']};
                font-family: 'Segoe UI', 'Tahoma', sans-serif;
                font-size: 13px;
            }}
        """)
        
        # Layout اصلی
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # منوی بالایی
        self.create_top_navigation(main_layout)
        
        # بخش اصلی (sidebar + محتوا)
        self.create_main_section(main_layout)
        
        # نمایش صفحه پیش‌فرض
        self.switch_page("home")
        
    def create_top_navigation(self, parent_layout):
        """ایجاد منوی بالایی"""
        self.top_bar = ModernTopBar()
        parent_layout.addWidget(self.top_bar)
        
    def create_main_section(self, parent_layout):
        """ایجاد بخش اصلی شامل sidebar و محتوا"""
        main_container = QFrame()
        main_container_layout = QHBoxLayout(main_container)
        main_container_layout.setContentsMargins(0, 0, 0, 0)
        main_container_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = CollapsibleSidebar()
        self.sidebar.menu_clicked.connect(self.switch_page)
        main_container_layout.addWidget(self.sidebar)
        
        # ناحیه محتوا
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        self.content_area.setStyleSheet(UIStyles.get_content_area_style())
        
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        main_container_layout.addWidget(self.content_area)
        parent_layout.addWidget(main_container)
        
    def switch_page(self, page_id):
        """تغییر صفحه"""
        self.current_page = page_id
        
        # بروزرسانی منوی کناری
        self.sidebar.set_active_menu(page_id)
        
        # بروزرسانی محتوا بر اساس صفحه
        if page_id == "home":
            self.show_home_page()
            self.top_bar.update_page_info("home", "صفحه اصلی", "خوش آمدید به سیستم مدیریت ربات‌های YARA")
            
        elif page_id == "child-loan":
            self.show_child_loan_page()
            self.top_bar.update_page_info("child-loan", "ربات وام فرزند", "این بخش مربوط به مدیریت وام فرزندآوری می‌باشد")
            
        elif page_id == "marriage-loan":
            self.show_marriage_loan_page()
            self.top_bar.update_page_info("marriage-loan", "ربات وام ازدواج", "این بخش مربوط به مدیریت وام ازدواج می‌باشد")
            
    def clear_content(self):
        """پاک کردن محتوای فعلی"""
        if self.main_content:
            self.main_content.setParent(None)
            self.main_content = None
            
    def show_home_page(self):
        """نمایش صفحه خانگی"""
        self.clear_content()
        self.main_content = self.page_manager.create_home_page()
        self.content_layout.addWidget(self.main_content)
        
    def show_child_loan_page(self):
        """نمایش صفحه ربات وام فرزند"""
        self.clear_content()
        self.main_content = self.page_manager.create_child_loan_page()
        self.content_layout.addWidget(self.main_content)
        
    def show_marriage_loan_page(self):
        """نمایش صفحه ربات وام ازدواج"""
        self.clear_content()
        self.main_content = self.page_manager.create_marriage_loan_page()
        self.content_layout.addWidget(self.main_content)
        
    def load_data(self):
        """بارگذاری داده‌های اولیه"""
        try:
            self.applicants = self.data_service.load_applicants()
        except Exception as e:
            QMessageBox.warning(self, "خطا", f"خطا در بارگذاری داده‌ها: {str(e)}")
            self.applicants = []
            
    def get_button_style(self, bg_color, hover_color):
        """استایل دکمه‌ها"""
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 500;
                font-size: 13px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {hover_color};
                transform: translateY(1px);
            }}
            QPushButton:disabled {{
                background-color: #64748B;
                color: #94A3B8;
            }}
        """
        
    def get_groupbox_style(self):
        """استایل GroupBox"""
        return f"""
            QGroupBox {{
                font-weight: 600;
                border: 1px solid {UIStyles.COLORS['border_color']};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                color: {UIStyles.COLORS['text_primary']};
                background-color: {UIStyles.COLORS['bg_secondary']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                color: {UIStyles.COLORS['accent_blue']};
                background-color: {UIStyles.COLORS['bg_secondary']};
            }}
        """
        
    def closeEvent(self, event):
        """رویداد بسته شدن برنامه"""
        reply = QMessageBox.question(self, "خروج", "آیا مطمئن هستید که می‌خواهید خارج شوید؟",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # ذخیره تنظیمات قبل از خروج
            try:
                # اینجا می‌تونیم تنظیمات را ذخیره کنیم
                pass
            except Exception as e:
                print(f"خطا در ذخیره تنظیمات: {e}")
            
            event.accept()
        else:
            event.ignore()
            
    def resizeEvent(self, event):
        """رویداد تغییر سایز پنجره"""
        super().resizeEvent(event)
        
        # بررسی وجود sidebar قبل از استفاده
        if not hasattr(self, 'sidebar'):
            return
            
        # تنظیم responsive layout
        width = self.width()
        if width < 1024:
            # سایز کوچک - sidebar جمع شود
            if not self.sidebar.collapsed:
                self.sidebar.toggle_sidebar()
        elif width > 1200 and self.sidebar.collapsed:
            # سایز بزرگ - sidebar باز شود
            self.sidebar.toggle_sidebar()