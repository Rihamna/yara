#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QFrame, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from .ui_styles import UIStyles

class TopNavigationButton(QPushButton):
    """دکمه‌های منوی بالایی"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.is_active = False
        self.setMinimumHeight(36)
        self.setup_style()
        
    def setup_style(self):
        """تنظیم استایل دکمه"""
        self.setStyleSheet(UIStyles.get_topbar_button_style())
        
    def set_active(self, active):
        """تنظیم وضعیت فعال"""
        self.is_active = active
        self.setProperty("active", active)
        self.style().polish(self)

class TopNavigation(QFrame):
    """منوی بالایی برنامه"""
    
    menu_clicked = pyqtSignal(str)  # سیگنال کلیک منو
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topbar")
        self.setup_ui()
        
    def setup_ui(self):
        """تنظیم رابط کاربری"""
        self.setStyleSheet(UIStyles.get_topbar_style())
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(0)
        
        # سمت چپ - منوها
        self.create_left_menu(layout)
        
        # فاصله
        layout.addStretch()
        
        # سمت راست - پروفایل
        self.create_right_section(layout)
        
    def create_left_menu(self, parent_layout):
        """ایجاد منوهای سمت چپ"""
        menu_frame = QFrame()
        menu_layout = QHBoxLayout(menu_frame)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(8)
        
        # منوهای اصلی
        menu_items = [
            ("صفحه اصلی", "home"),
            ("ربات ها", "robots")
        ]
        
        self.menu_buttons = {}
        for text, menu_id in menu_items:
            btn = TopNavigationButton(text)
            btn.clicked.connect(lambda checked, mid=menu_id: self.menu_clicked.emit(mid))
            menu_layout.addWidget(btn)
            self.menu_buttons[menu_id] = btn
        
        parent_layout.addWidget(menu_frame)
        
    def create_right_section(self, parent_layout):
        """ایجاد بخش راست - پروفایل و اطلاعات"""
        right_frame = QFrame()
        right_layout = QHBoxLayout(right_frame)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)
        
        # دکمه‌های اطلاعاتی
        info_buttons = [
            "اطلاع‌رسانی",
            "متقاضیان",
            "آموزش استفاده"
        ]
        
        for btn_text in info_buttons:
            btn = TopNavigationButton(btn_text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {UIStyles.COLORS['text_secondary']};
                    border: none;
                    padding: 6px 12px;
                    font-size: 13px;
                    font-weight: 400;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    color: {UIStyles.COLORS['text_primary']};
                    background-color: {UIStyles.COLORS['hover_bg']};
                }}
            """)
            right_layout.addWidget(btn)
        
        # دکمه تطبیقات وام (active)
        loan_app_btn = TopNavigationButton("تطبیقات وام")
        loan_app_btn.set_active(True)
        right_layout.addWidget(loan_app_btn)
        
        # دکمه پروفایل YARA
        profile_btn = QPushButton("U    YARA")
        profile_btn.setStyleSheet(UIStyles.get_profile_button_style())
        right_layout.addWidget(profile_btn)
        
        parent_layout.addWidget(right_frame)
        
    def set_active_menu(self, menu_id):
        """تنظیم منوی فعال"""
        for btn_id, button in self.menu_buttons.items():
            button.set_active(btn_id == menu_id)

class ModernTopBar(QFrame):
    """منوی بالایی مدرن مطابق طراحی"""
    
    menu_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernTopBar")
        self.current_page = "home"
        self.setup_ui()
        
    def setup_ui(self):
        """تنظیم UI مطابق تصاویر"""
        self.setFixedHeight(64)
        self.setStyleSheet(f"""
            QFrame#modernTopBar {{
                background-color: {UIStyles.COLORS['bg_topbar']};
                border-bottom: 1px solid {UIStyles.COLORS['border_color']};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        
        # عنوان صفحه فعلی (سمت چپ)
        self.page_title = QLabel("ربات وام ازدواج")
        self.page_title.setStyleSheet(f"""
            color: {UIStyles.COLORS['accent_blue']};
            font-size: 18px;
            font-weight: 600;
        """)
        
        self.page_subtitle = QLabel("این بخش مربوط به مدیریت وام ازدواج می‌باشد")
        self.page_subtitle.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_secondary']};
            font-size: 14px;
            margin-top: 2px;
        """)
        
        left_section = QFrame()
        left_layout = QVBoxLayout(left_section)
        left_layout.setContentsMargins(0, 8, 0, 8)
        left_layout.setSpacing(2)
        left_layout.addWidget(self.page_title)
        left_layout.addWidget(self.page_subtitle)
        
        layout.addWidget(left_section)
        layout.addStretch()
        
        # منوهای سمت راست
        right_section = QFrame()
        right_layout = QHBoxLayout(right_section)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(6)
        
        # دکمه‌های اطلاعاتی
        info_items = [
            ("اطلاع‌رسانی", "notifications"),
            ("متقاضیان", "applicants"),
            ("آموزش استفاده", "tutorial")
        ]
        
        self.info_buttons = {}
        for text, btn_id in info_items:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {UIStyles.COLORS['text_secondary']};
                    border: none;
                    padding: 8px 14px;
                    font-size: 13px;
                    font-weight: 400;
                    border-radius: 6px;
                }}
                QPushButton:hover {{
                    color: {UIStyles.COLORS['text_primary']};
                    background-color: {UIStyles.COLORS['hover_bg']};
                }}
            """)
            right_layout.addWidget(btn)
            self.info_buttons[btn_id] = btn
        
        # دکمه تطبیقات وام (فعال)
        self.active_btn = QPushButton("تطبیقات وام")
        self.active_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {UIStyles.COLORS['accent_blue']};
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {UIStyles.COLORS['accent_blue_hover']};
            }}
        """)
        right_layout.addWidget(self.active_btn)
        
        # فاصله
        right_layout.addSpacing(16)
        
        # پروفایل YARA
        profile_container = QFrame()
        profile_layout = QHBoxLayout(profile_container)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(8)
        
        # آیکن کاربر
        user_icon = QLabel("U")
        user_icon.setFixedSize(32, 32)
        user_icon.setAlignment(Qt.AlignCenter)
        user_icon.setStyleSheet(f"""
            QLabel {{
                background-color: {UIStyles.COLORS['accent_blue']};
                color: white;
                border-radius: 16px;
                font-weight: bold;
                font-size: 14px;
            }}
        """)
        
        # نام کاربر
        username = QLabel("YARA")
        username.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_primary']};
            font-size: 14px;
            font-weight: 500;
        """)
        
        profile_layout.addWidget(user_icon)
        profile_layout.addWidget(username)
        
        right_layout.addWidget(profile_container)
        layout.addWidget(right_section)
        
    def update_page_info(self, page_id, title, subtitle):
        """بروزرسانی اطلاعات صفحه"""
        self.current_page = page_id
        self.page_title.setText(title)
        self.page_subtitle.setText(subtitle)
        
        # تغییر رنگ عنوان بر اساس صفحه
        if page_id == "home":
            self.page_title.setStyleSheet(f"""
                color: {UIStyles.COLORS['text_primary']};
                font-size: 18px;
                font-weight: 600;
            """)
        else:
            self.page_title.setStyleSheet(f"""
                color: {UIStyles.COLORS['accent_blue']};
                font-size: 18px;
                font-weight: 600;
            """)