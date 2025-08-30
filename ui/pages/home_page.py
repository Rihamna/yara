#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from .base_page import BasePage
from ..styles.colors import AppColors

class HomePage(BasePage):
    """صفحه اصلی برنامه"""
    
    def __init__(self, parent=None):
        super().__init__("home", "صفحه اصلی", parent)
        
    def create_content(self):
        """ایجاد محتوای صفحه اصلی"""
        # متن خوشامدگویی
        welcome_text = QLabel("به سامانه YARA خوش آمدید. از منوی سمت راست بخش مورد نظر خود را انتخاب کنید.")
        welcome_text.setStyleSheet(f"""
            QLabel {{
                color: {AppColors.DARK_TEXT};
                font-size: 16px;
                line-height: 1.6;
                padding: 20px;
                background-color: rgba(59, 130, 246, 0.1);
                border-radius: 8px;
                border: 1px solid {AppColors.PRIMARY};
            }}
        """)
        welcome_text.setWordWrap(True)
        self.content_layout.addWidget(welcome_text)
        
        # کارت‌های معرفی
        self.create_info_cards()
        
        self.content_layout.addStretch()
        
    def create_info_cards(self):
        """ایجاد کارت‌های اطلاعاتی"""
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        # کارت ربات وام ازدواج
        marriage_card = self.create_info_card(
            "💍", 
            "ربات وام ازدواج", 
            "اتوماسیون فرآیند ثبت نام وام ازدواج در بانک‌های مختلف"
        )
        cards_layout.addWidget(marriage_card)
        
        # کارت ربات وام فرزند  
        child_card = self.create_info_card(
            "👶",
            "ربات وام فرزند",
            "اتوماسیون فرآیند ثبت نام وام فرزندآوری در بانک‌های مختلف"
        )
        cards_layout.addWidget(child_card)
        
        # کارت تنظیمات
        settings_card = self.create_info_card(
            "⚙️",
            "تنظیمات سیستم", 
            "مدیریت و پیکربندی تنظیمات کلی سیستم و ربات‌ها"
        )
        cards_layout.addWidget(settings_card)
        
        self.content_layout.addLayout(cards_layout)
        
    def create_info_card(self, icon, title, description):
        """ایجاد کارت اطلاعاتی"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {AppColors.DARK_BG};
                border: 1px solid {AppColors.DARK_BORDER};
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame:hover {{
                border-color: {AppColors.PRIMARY};
                background-color: {AppColors.DARK_HOVER};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        # آیکون
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                margin-bottom: 10px;
            }
        """)
        
        # عنوان
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {AppColors.LIGHT_TEXT};
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
        """)
        
        # توضیحات
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {AppColors.MUTED_TEXT};
                font-size: 14px;
                line-height: 1.4;
            }}
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        
        return card