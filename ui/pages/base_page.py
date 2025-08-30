#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from ..styles.colors import AppStyles

class BasePage(QWidget):
    """کلاس پایه برای تمام صفحات"""
    
    page_changed = pyqtSignal(str)  # سیگنال تغییر صفحه
    
    def __init__(self, page_id, title, parent=None):
        super().__init__(parent)
        self.page_id = page_id
        self.page_title = title
        
        self.setup_ui()
        
    def setup_ui(self):
        """تنظیم رابط کاربری پایه"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # فریم محتوا
        self.content_frame = QFrame()
        self.content_frame.setObjectName("pageContent")
        self.content_frame.setStyleSheet(AppStyles.get_page_content_style())
        
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)
        
        # عنوان صفحه
        self.title_label = QLabel(self.page_title)
        self.title_label.setStyleSheet(AppStyles.get_page_title_style())
        self.content_layout.addWidget(self.title_label)
        
        # ناحیه محتوای سفارشی
        self.create_content()
        
        layout.addWidget(self.content_frame)
        
    def create_content(self):
        """ایجاد محتوای صفحه - باید در کلاس‌های فرزند override شود"""
        pass
        
    def show_page(self):
        """نمایش صفحه"""
        self.show()
        
    def hide_page(self):
        """مخفی کردن صفحه"""
        self.hide()
        
    def refresh_page(self):
        """بروزرسانی محتوای صفحه"""
        pass

class SimpleContentPage(BasePage):
    """صفحه ساده با متن"""
    
    def __init__(self, page_id, title, content_text, parent=None):
        self.content_text = content_text
        super().__init__(page_id, title, parent)
        
    def create_content(self):
        """ایجاد محتوای ساده"""
        content_label = QLabel(self.content_text)
        content_label.setStyleSheet(f"""
            QLabel {{
                color: #E0E0E0;
                font-size: 16px;
                line-height: 1.6;
                padding: 20px;
            }}
        """)
        content_label.setWordWrap(True)
        self.content_layout.addWidget(content_label)
        self.content_layout.addStretch()