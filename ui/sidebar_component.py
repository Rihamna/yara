#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QFrame, QLabel, QScrollArea)
from PyQt5.QtCore import Qt, QEasingCurve, QPropertyAnimation, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from .ui_styles import UIStyles

class MenuButton(QPushButton):
    """دکمه منوی اصلی"""
    
    def __init__(self, text, icon_text, parent=None):
        super().__init__(parent)
        self.text_content = text
        self.icon_content = icon_text
        self.is_active = False
        
        self.setObjectName("menuBtn")
        self.setProperty("class", "menuBtn")
        self.setup_ui()
        
    def setup_ui(self):
        """تنظیم رابط کاربری دکمه"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(8)
        
        # آیکن
        self.icon_label = QLabel(self.icon_content)
        self.icon_label.setFixedSize(22, 22)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 16px;")
        
        # متن
        self.text_label = QLabel(self.text_content)
        self.text_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addStretch()
        
        self.setStyleSheet(UIStyles.get_menu_button_style())
        
    def set_active(self, active):
        """تنظیم حالت فعال"""
        self.is_active = active
        self.setProperty("active", active)
        self.style().polish(self)
        
    def hide_text(self):
        """مخفی کردن متن برای حالت collapsed"""
        self.text_label.hide()
        
    def show_text(self):
        """نمایش متن"""
        self.text_label.show()

class SubMenuButton(QPushButton):
    """دکمه زیرمنو"""
    
    def __init__(self, text, icon_text, parent=None):
        super().__init__(parent)
        self.text_content = text
        self.icon_content = icon_text
        self.is_active = False
        
        self.setObjectName("submenuBtn")
        self.setProperty("class", "submenuBtn")
        self.setup_ui()
        
    def setup_ui(self):
        """تنظیم رابط کاربری زیرمنو"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 15, 8)
        layout.setSpacing(7)
        
        # آیکن
        self.icon_label = QLabel(self.icon_content)
        self.icon_label.setFixedSize(16, 16)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 13px;")
        
        # متن
        self.text_label = QLabel(self.text_content)
        self.text_label.setStyleSheet("font-size: 13px;")
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addStretch()
        
        self.setStyleSheet(UIStyles.get_submenu_button_style())
        
    def set_active(self, active):
        """تنظیم حالت فعال"""
        self.is_active = active
        self.setProperty("active", active)
        self.style().polish(self)
        
    def hide_text(self):
        """مخفی کردن متن"""
        self.text_label.hide()
        
    def show_text(self):
        """نمایش متن"""
        self.text_label.show()

class CollapsibleSidebar(QFrame):
    """Sidebar جمع‌شونده مطابق طراحی HTML"""
    
    # سیگنال‌ها
    menu_clicked = pyqtSignal(str)  # سیگنال کلیک منو
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        
        # حالت sidebar
        self.collapsed = False
        self.expanded_width = 220
        self.collapsed_width = 80
        
        # تنظیم اولیه
        self.setFixedWidth(self.expanded_width)
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """تنظیم رابط کاربری sidebar"""
        self.setStyleSheet(UIStyles.get_sidebar_style())
        
        # Layout اصلی
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # هدر
        self.create_header(main_layout)
        
        # منوی اصلی
        self.create_menu_area(main_layout)
        
    def create_header(self, parent_layout):
        """ایجاد هدر sidebar"""
        self.header_frame = QFrame()
        self.header_frame.setObjectName("sidebarHeader")
        self.header_frame.setStyleSheet(UIStyles.get_sidebar_header_style())
        
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(13, 17, 13, 17)
        header_layout.setSpacing(15)
        
        # کانتینر لوگو و پروفایل
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(15)
        
        # لوگو YARA
        self.logo_label = QLabel("YARA")
        self.logo_label.setObjectName("logo")
        self.logo_label.setStyleSheet(UIStyles.get_logo_style())
        
        # دکمه پروفایل
        self.profile_btn = QPushButton("U")
        self.profile_btn.setObjectName("profileBtn")
        self.profile_btn.setStyleSheet(UIStyles.get_profile_button_style())
        
        logo_layout.addStretch()
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.profile_btn)
        
        header_layout.addWidget(logo_container)
        
        # دکمه toggle (خارج از layout اصلی)
        self.toggle_btn = QPushButton(UIStyles.ICONS['toggle_open'])
        self.toggle_btn.setObjectName("toggleBtn")
        self.toggle_btn.setStyleSheet(UIStyles.get_toggle_button_style())
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
        parent_layout.addWidget(self.header_frame)
        
    def create_menu_area(self, parent_layout):
        """ایجاد ناحیه منو"""
        # ScrollArea برای منو
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        # ویجت محتوای منو
        menu_widget = QWidget()
        self.menu_layout = QVBoxLayout(menu_widget)
        self.menu_layout.setContentsMargins(0, 13, 0, 13)
        self.menu_layout.setSpacing(4)
        
        # ایجاد منوها
        self.create_menu_items()
        
        # فضای خالی در انتها
        self.menu_layout.addStretch()
        
        scroll_area.setWidget(menu_widget)
        parent_layout.addWidget(scroll_area)
        
    def create_menu_items(self):
        """ایجاد آیتم‌های منو"""
        # ذخیره منوها برای مدیریت
        self.menu_buttons = {}
        self.submenu_buttons = {}
        
        # منو صفحه اصلی
        home_frame = QFrame()
        home_frame.setProperty("class", "menuItem")
        home_frame.setStyleSheet(UIStyles.get_menu_item_style())
        home_layout = QVBoxLayout(home_frame)
        home_layout.setContentsMargins(0, 0, 0, 0)
        
        self.home_btn = MenuButton("صفحه اصلی", UIStyles.ICONS['home'])
        self.home_btn.clicked.connect(lambda: self.menu_clicked.emit("home"))
        home_layout.addWidget(self.home_btn)
        
        self.menu_buttons["home"] = self.home_btn
        self.menu_layout.addWidget(home_frame)
        
        # منو تنظیمات
        settings_frame = QFrame()
        settings_frame.setProperty("class", "menuItem")
        settings_frame.setStyleSheet(UIStyles.get_menu_item_style())
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        
        self.settings_btn = MenuButton("تنظیمات", UIStyles.ICONS['settings'])
        self.settings_btn.clicked.connect(lambda: self.menu_clicked.emit("settings"))
        settings_layout.addWidget(self.settings_btn)
        
        self.menu_buttons["settings"] = self.settings_btn
        self.menu_layout.addWidget(settings_frame)
        
        # منو ربات‌ها (با زیرمنو)
        self.create_robots_menu()
        
        # منو اخبار
        news_frame = QFrame()
        news_frame.setProperty("class", "menuItem")
        news_frame.setStyleSheet(UIStyles.get_menu_item_style())
        news_layout = QVBoxLayout(news_frame)
        news_layout.setContentsMargins(0, 0, 0, 0)
        
        self.news_btn = MenuButton("اخبار", UIStyles.ICONS['news'])
        self.news_btn.clicked.connect(lambda: self.menu_clicked.emit("news"))
        news_layout.addWidget(self.news_btn)
        
        self.menu_buttons["news"] = self.news_btn
        self.menu_layout.addWidget(news_frame)
        
        # منو آموزش‌ها
        education_frame = QFrame()
        education_frame.setProperty("class", "menuItem")
        education_frame.setStyleSheet(UIStyles.get_menu_item_style())
        education_layout = QVBoxLayout(education_frame)
        education_layout.setContentsMargins(0, 0, 0, 0)
        
        self.education_btn = MenuButton("آموزش ها", UIStyles.ICONS['education'])
        self.education_btn.clicked.connect(lambda: self.menu_clicked.emit("education"))
        education_layout.addWidget(self.education_btn)
        
        self.menu_buttons["education"] = self.education_btn
        self.menu_layout.addWidget(education_frame)
        
        # منو ارتباط با ما
        contact_frame = QFrame()
        contact_frame.setProperty("class", "menuItem")
        contact_frame.setStyleSheet(UIStyles.get_menu_item_style())
        contact_layout = QVBoxLayout(contact_frame)
        contact_layout.setContentsMargins(0, 0, 0, 0)
        
        self.contact_btn = MenuButton("ارتباط با ما", UIStyles.ICONS['contact'])
        self.contact_btn.clicked.connect(lambda: self.menu_clicked.emit("contact"))
        contact_layout.addWidget(self.contact_btn)
        
        self.menu_buttons["contact"] = self.contact_btn
        self.menu_layout.addWidget(contact_frame)
        
    def create_robots_menu(self):
        """ایجاد منوی ربات‌ها با زیرمنو"""
        robots_frame = QFrame()
        robots_frame.setProperty("class", "menuItem")
        robots_frame.setStyleSheet(UIStyles.get_menu_item_style())
        robots_layout = QVBoxLayout(robots_frame)
        robots_layout.setContentsMargins(0, 0, 0, 0)
        robots_layout.setSpacing(0)
        
        # منوی اصلی ربات‌ها
        self.robots_btn = MenuButton("ربات ها", UIStyles.ICONS['robot'])
        self.robots_btn.clicked.connect(self.toggle_robots_submenu)
        robots_layout.addWidget(self.robots_btn)
        
        # زیرمنو
        self.submenu_frame = QFrame()
        self.submenu_frame.setProperty("class", "submenu")
        self.submenu_frame.setStyleSheet(UIStyles.get_submenu_style())
        
        submenu_layout = QVBoxLayout(self.submenu_frame)
        submenu_layout.setContentsMargins(0, 0, 0, 0)
        submenu_layout.setSpacing(2)
        
        # ربات وام ازدواج
        self.marriage_loan_btn = SubMenuButton("ربات وام ازدواج", UIStyles.ICONS['marriage'])
        self.marriage_loan_btn.clicked.connect(lambda: self.handle_submenu_click("marriage-loan"))
        submenu_layout.addWidget(self.marriage_loan_btn)
        
        # ربات وام فرزند
        self.child_loan_btn = SubMenuButton("ربات وام فرزند", UIStyles.ICONS['child'])
        self.child_loan_btn.clicked.connect(lambda: self.handle_submenu_click("child-loan"))
        submenu_layout.addWidget(self.child_loan_btn)
        
        # ذخیره زیرمنوها
        self.submenu_buttons["marriage-loan"] = self.marriage_loan_btn
        self.submenu_buttons["child-loan"] = self.child_loan_btn
        
        # مخفی کردن زیرمنو در ابتدا
        self.submenu_frame.hide()
        
        robots_layout.addWidget(self.submenu_frame)
        self.menu_buttons["robots"] = self.robots_btn
        self.menu_layout.addWidget(robots_frame)
        
    def setup_animations(self):
        """تنظیم انیمیشن‌ها"""
        self.width_animation = QPropertyAnimation(self, b"maximumWidth")
        self.width_animation.setDuration(300)
        self.width_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # انیمیشن برای زیرمنو
        self.submenu_animation = QPropertyAnimation(self.submenu_frame, b"maximumHeight")
        self.submenu_animation.setDuration(300)
        self.submenu_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def toggle_sidebar(self):
        """تغییر وضعیت باز/بسته sidebar"""
        self.collapsed = not self.collapsed
        
        # تنظیم عرض جدید
        target_width = self.collapsed_width if self.collapsed else self.expanded_width
        
        self.width_animation.setStartValue(self.width())
        self.width_animation.setEndValue(target_width)
        self.width_animation.finished.connect(self.on_animation_finished)
        self.width_animation.start()
        
        # تغییر آیکن toggle
        icon = UIStyles.ICONS['toggle_close'] if self.collapsed else UIStyles.ICONS['toggle_open']
        self.toggle_btn.setText(icon)
        
    def on_animation_finished(self):
        """اتمام انیمیشن تغییر عرض"""
        if self.collapsed:
            # مخفی کردن متن‌ها
            self.logo_label.hide()
            for button in self.menu_buttons.values():
                button.hide_text()
            for button in self.submenu_buttons.values():
                button.hide_text()
            # بستن زیرمنو
            self.submenu_frame.hide()
        else:
            # نمایش متن‌ها
            self.logo_label.show()
            for button in self.menu_buttons.values():
                button.show_text()
            for button in self.submenu_buttons.values():
                button.show_text()
                
    def toggle_robots_submenu(self):
        """تغییر وضعیت زیرمنوی ربات‌ها"""
        if self.collapsed:
            return
            
        if self.submenu_frame.isVisible():
            # بستن زیرمنو
            self.submenu_frame.hide()
        else:
            # بازکردن زیرمنو
            self.submenu_frame.show()
            
    def handle_submenu_click(self, page_id):
        """مدیریت کلیک روی زیرمنو"""
        # فعال کردن منوی اصلی ربات‌ها
        self.set_active_menu("robots")
        
        # فعال کردن زیرمنوی انتخاب شده
        for sub_id, button in self.submenu_buttons.items():
            button.set_active(sub_id == page_id)
            
        # ارسال سیگنال
        self.menu_clicked.emit(page_id)
        
    def set_active_menu(self, menu_id):
        """تنظیم منوی فعال"""
        # غیرفعال کردن همه منوها
        for btn_id, button in self.menu_buttons.items():
            button.set_active(btn_id == menu_id)
            
        # مدیریت زیرمنو
        if menu_id in ["marriage-loan", "child-loan"]:
            self.robots_btn.set_active(True)
            if not self.collapsed:
                self.submenu_frame.show()
        elif menu_id != "robots":
            for button in self.submenu_buttons.values():
                button.set_active(False)
                
    def resizeEvent(self, event):
        """تنظیم موقعیت دکمه toggle هنگام تغییر سایز"""
        super().resizeEvent(event)
        # تنظیم موقعیت دکمه toggle
        toggle_x = -14
        toggle_y = 30  # وسط هدر
        self.toggle_btn.move(toggle_x, toggle_y)
        self.toggle_btn.raise_()  # آوردن به جلو