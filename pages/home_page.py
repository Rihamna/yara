#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QPushButton, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ..ui_styles import UIStyles

class StatsCard(QFrame):
    """کارت آمار"""
    
    def __init__(self, title, value, icon="📊", parent=None):
        super().__init__(parent)
        self.setProperty("class", "pageContent")
        self.setStyleSheet(UIStyles.get_card_style())
        self.setup_ui(title, value, icon)
        
    def setup_ui(self, title, value, icon):
        """تنظیم UI کارت"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # آیکن
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 32px; color: #3b82f6;")
        
        # مقدار
        value_label = QLabel(str(value))
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        
        # عنوان
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {UIStyles.COLORS['dark_text']}; font-size: 14px;")
        
        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(title_label)

class QuickActionButton(QPushButton):
    """دکمه عمل سریع"""
    
    def __init__(self, text, icon="▶", parent=None):
        super().__init__(parent)
        self.setText(f"{icon} {text}")
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {UIStyles.COLORS['dark_secondary']};
                color: {UIStyles.COLORS['dark_text']};
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 500;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {UIStyles.COLORS['dark_hover']};
                border-color: {UIStyles.COLORS['primary']};
            }}
            QPushButton:pressed {{
                background-color: {UIStyles.COLORS['primary']};
                color: white;
            }}
        """)

class HomePage(QWidget):
    """صفحه اصلی برنامه"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """تنظیم رابط کاربری"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # عنوان صفحه
        title = QLabel("داشبورد اصلی")
        title.setProperty("class", "pageTitle")
        title.setStyleSheet(UIStyles.get_page_title_style())
        main_layout.addWidget(title)
        
        # کارت‌های آمار
        self.create_stats_section(main_layout)
        
        # بخش عملیات سریع
        self.create_quick_actions_section(main_layout)
        
        # بخش اخبار و اطلاعیه‌ها
        self.create_news_section(main_layout)
        
        main_layout.addStretch()
        
    def create_stats_section(self, parent_layout):
        """ایجاد بخش آمار"""
        stats_frame = QFrame()
        stats_layout = QGridLayout(stats_frame)
        stats_layout.setSpacing(15)
        
        # کارت‌های آمار
        cards_data = [
            ("کل متقاضیان", "1,247", "👥"),
            ("وام‌های تایید شده", "856", "✅"),
            ("وام‌های در انتظار", "123", "⏳"),
            ("مبلغ کل پرداختی", "2.4 میلیارد", "💰")
        ]
        
        for i, (title, value, icon) in enumerate(cards_data):
            card = StatsCard(title, value, icon)
            row = i // 2
            col = i % 2
            stats_layout.addWidget(card, row, col)
            
        parent_layout.addWidget(stats_frame)
        
    def create_quick_actions_section(self, parent_layout):
        """ایجاد بخش عملیات سریع"""
        actions_frame = QFrame()
        actions_frame.setProperty("class", "pageContent")
        actions_frame.setStyleSheet(UIStyles.get_page_content_style())
        
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setSpacing(15)
        
        # عنوان بخش
        section_title = QLabel("عملیات سریع")
        section_title.setStyleSheet("font-size: 16px; font-weight: bold; color: white; margin-bottom: 10px;")
        actions_layout.addWidget(section_title)
        
        # دکمه‌های عملیات
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        actions_data = [
            ("مدیریت ربات وام ازدواج", "💕"),
            ("مدیریت ربات وام فرزند", "👶"),
            ("مشاهده گزارشات", "📊"),
            ("تنظیمات سیستم", "⚙️")
        ]
        
        for text, icon in actions_data:
            btn = QuickActionButton(text, icon)
            buttons_layout.addWidget(btn)
            
        actions_layout.addLayout(buttons_layout)
        parent_layout.addWidget(actions_frame)
        
    def create_news_section(self, parent_layout):
        """ایجاد بخش اخبار"""
        news_frame = QFrame()
        news_frame.setProperty("class", "pageContent")
        news_frame.setStyleSheet(UIStyles.get_page_content_style())
        
        news_layout = QVBoxLayout(news_frame)
        news_layout.setSpacing(15)
        
        # عنوان بخش
        section_title = QLabel("آخرین اخبار و اطلاعیه‌ها")
        section_title.setStyleSheet("font-size: 16px; font-weight: bold; color: white; margin-bottom: 10px;")
        news_layout.addWidget(section_title)
        
        # لیست اخبار
        news_items = [
            "🔔 بروزرسانی سیستم ربات وام ازدواج انجام شد",
            "📢 مهلت ثبت‌نام وام فرزند تا پایان ماه تمدید شد",
            "⚠️ توجه: تغییرات جدید در فرآیند تایید وام‌ها",
            "💡 راهنمای جدید استفاده از سیستم منتشر شد"
        ]
        
        for item in news_items:
            news_label = QLabel(item)
            news_label.setStyleSheet(f"""
                color: {UIStyles.COLORS['dark_text']};
                padding: 8px 0;
                border-bottom: 1px solid {UIStyles.COLORS['dark_border']};
                font-size: 14px;
            """)
            news_layout.addWidget(news_label)
            
        parent_layout.addWidget(news_frame)
        
    def activate(self):
        """فراخوانی هنگام فعال شدن صفحه"""
        # می‌توان اینجا داده‌ها را بروزرسانی کرد
        pass