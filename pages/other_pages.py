#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QPushButton, QLineEdit, QTextEdit,
                            QCheckBox, QComboBox, QSpinBox, QTabWidget)
from PyQt5.QtCore import Qt
from ..ui_styles import UIStyles

class BasePage(QWidget):
    """کلاس پایه برای صفحات"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.page_title = title
        self.setup_base_ui()
        
    def setup_base_ui(self):
        """تنظیم UI پایه"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # عنوان صفحه
        title = QLabel(self.page_title)
        title.setProperty("class", "pageTitle")
        title.setStyleSheet(UIStyles.get_page_title_style())
        self.main_layout.addWidget(title)
        
        # محتوای اصلی
        self.content_frame = QFrame()
        self.content_frame.setProperty("class", "pageContent")
        self.content_frame.setStyleSheet(UIStyles.get_page_content_style())
        
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setSpacing(15)
        
        self.main_layout.addWidget(self.content_frame)
        self.main_layout.addStretch()

class SettingsPage(BasePage):
    """صفحه تنظیمات"""
    
    def __init__(self, parent=None):
        super().__init__("تنظیمات سیستم", parent)
        self.setup_settings_ui()
        
    def setup_settings_ui(self):
        """تنظیم UI تنظیمات"""
        # تب‌های تنظیمات
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 4px;
                background-color: transparent;
            }}
            QTabBar::tab {{
                background-color: {UIStyles.COLORS['dark_hover']};
                color: {UIStyles.COLORS['dark_text']};
                padding: 8px 16px;
                margin-right: 2px;
                border-radius: 4px 4px 0 0;
            }}
            QTabBar::tab:selected {{
                background-color: {UIStyles.COLORS['primary']};
                color: white;
            }}
        """)
        
        # تب تنظیمات عمومی
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # تنظیمات اتصال به بانک
        bank_group = self.create_settings_group("تنظیمات اتصال به بانک", [
            ("آدرس سرور:", QLineEdit("192.168.1.100")),
            ("پورت:", QSpinBox()),
            ("نام کاربری:", QLineEdit("admin")),
            ("رمز عبور:", QLineEdit()),
        ])
        general_layout.addWidget(bank_group)
        
        # تنظیمات اطلاع‌رسانی
        notif_group = self.create_settings_group("تنظیمات اطلاع‌رسانی", [
            ("ارسال SMS:", QCheckBox("فعال")),
            ("ارسال ایمیل:", QCheckBox("فعال")),
            ("اطلاع‌رسانی تلگرام:", QCheckBox("فعال")),
        ])
        general_layout.addWidget(notif_group)
        
        general_layout.addStretch()
        tabs.addTab(general_tab, "عمومی")
        
        # تب تنظیمات امنیتی
        security_tab = QWidget()
        security_layout = QVBoxLayout(security_tab)
        
        security_group = self.create_settings_group("تنظیمات امنیتی", [
            ("مدت انقضای جلسه (دقیقه):", QSpinBox()),
            ("حداکثر تلاش ورود:", QSpinBox()),
            ("رمزگذاری داده‌ها:", QCheckBox("فعال")),
        ])
        security_layout.addWidget(security_group)
        security_layout.addStretch()
        
        tabs.addTab(security_tab, "امنیت")
        
        self.content_layout.addWidget(tabs)
        
    def create_settings_group(self, title, items):
        """ایجاد گروه تنظیمات"""
        group_frame = QFrame()
        group_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(42, 42, 61, 0.3);
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(group_frame)
        
        # عنوان گروه
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # آیتم‌های تنظیمات
        for label_text, widget in items:
            item_layout = QHBoxLayout()
            
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {UIStyles.COLORS['dark_text']}; min-width: 150px;")
            
            if isinstance(widget, QLineEdit):
                widget.setStyleSheet(f"""
                    QLineEdit {{
                        background-color: {UIStyles.COLORS['dark_hover']};
                        color: white;
                        border: 1px solid {UIStyles.COLORS['dark_border']};
                        border-radius: 4px;
                        padding: 8px;
                    }}
                """)
            elif isinstance(widget, QSpinBox):
                widget.setRange(1, 9999)
                widget.setValue(30)
                widget.setStyleSheet(f"""
                    QSpinBox {{
                        background-color: {UIStyles.COLORS['dark_hover']};
                        color: white;
                        border: 1px solid {UIStyles.COLORS['dark_border']};
                        border-radius: 4px;
                        padding: 8px;
                    }}
                """)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(True)
                widget.setStyleSheet(f"color: {UIStyles.COLORS['dark_text']};")
            
            item_layout.addWidget(label)
            item_layout.addWidget(widget)
            item_layout.addStretch()
            
            layout.addLayout(item_layout)
            
        return group_frame

class NewsPage(BasePage):
    """صفحه اخبار"""
    
    def __init__(self, parent=None):
        super().__init__("اخبار و اطلاعیه‌ها", parent)
        self.setup_news_ui()
        
    def setup_news_ui(self):
        """تنظیم UI اخبار"""
        # لیست اخبار
        news_items = [
            {
                'title': 'بروزرسانی سیستم ربات وام ازدواج',
                'date': '1403/05/15',
                'content': 'سیستم ربات وام ازدواج با ویژگی‌های جدید بروزرسانی شد...',
                'type': 'update'
            },
            {
                'title': 'تمدید مهلت ثبت‌نام وام فرزند',
                'date': '1403/05/10',
                'content': 'مهلت ثبت‌نام برای وام فرزند تا پایان ماه جاری تمدید شد...',
                'type': 'info'
            },
            {
                'title': 'تغییرات فرآیند تایید وام‌ها',
                'date': '1403/05/05',
                'content': 'فرآیند تایید وام‌ها با هدف تسریع در پردازش تغییر یافت...',
                'type': 'warning'
            }
        ]
        
        for item in news_items:
            news_card = self.create_news_card(item)
            self.content_layout.addWidget(news_card)
            
    def create_news_card(self, news_item):
        """ایجاد کارت خبر"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(42, 42, 61, 0.5);
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 8px;
                padding: 15px;
                margin: 5px 0;
            }}
            QFrame:hover {{
                border-color: {UIStyles.COLORS['primary']};
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # هدر خبر
        header_layout = QHBoxLayout()
        
        title_label = QLabel(news_item['title'])
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        
        date_label = QLabel(news_item['date'])
        date_label.setStyleSheet(f"color: {UIStyles.COLORS['dark_text']}; font-size: 12px;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(date_label)
        
        # محتوای خبر
        content_label = QLabel(news_item['content'])
        content_label.setStyleSheet(f"color: {UIStyles.COLORS['dark_text']}; font-size: 14px; margin-top: 8px;")
        content_label.setWordWrap(True)
        
        layout.addLayout(header_layout)
        layout.addWidget(content_label)
        
        return card

class EducationPage(BasePage):
    """صفحه آموزش‌ها"""
    
    def __init__(self, parent=None):
        super().__init__("آموزش‌های سیستم", parent)
        self.setup_education_ui()
        
    def setup_education_ui(self):
        """تنظیم UI آموزش‌ها"""
        # دسته‌بندی آموزش‌ها
        categories = [
            {
                'title': 'آموزش کار با ربات وام ازدواج',
                'icon': '💕',
                'lessons': [
                    'راه‌اندازی و پیکربندی اولیه',
                    'ثبت اطلاعات متقاضیان',
                    'فرآیند بررسی و تایید درخواست‌ها',
                    'تنظیمات اطلاع‌رسانی'
                ]
            },
            {
                'title': 'آموزش کار با ربات وام فرزند',
                'icon': '👶',
                'lessons': [
                    'تنظیمات اولیه سیستم',
                    'مدیریت اطلاعات متقاضیان',
                    'نحوه محاسبه و تایید وام',
                    'گزارش‌گیری از سیستم'
                ]
            },
            {
                'title': 'آموزش تنظیمات سیستم',
                'icon': '⚙️',
                'lessons': [
                    'تنظیمات اتصال به بانک',
                    'مدیریت کاربران',
                    'تنظیمات امنیتی',
                    'پشتیبان‌گیری و بازیابی'
                ]
            }
        ]
        
        for category in categories:
            category_card = self.create_education_category(category)
            self.content_layout.addWidget(category_card)
            
    def create_education_category(self, category):
        """ایجاد دسته آموزشی"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(42, 42, 61, 0.5);
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 8px;
                padding: 15px;
                margin: 5px 0;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # عنوان دسته
        title_layout = QHBoxLayout()
        
        icon_label = QLabel(category['icon'])
        icon_label.setStyleSheet("font-size: 24px;")
        
        title_label = QLabel(category['title'])
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # لیست درس‌ها
        for lesson in category['lessons']:
            lesson_btn = QPushButton(f"▶ {lesson}")
            lesson_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {UIStyles.COLORS['dark_text']};
                    border: none;
                    padding: 8px 0;
                    text-align: left;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    color: {UIStyles.COLORS['primary_light']};
                    text-decoration: underline;
                }}
            """)
            layout.addWidget(lesson_btn)
            
        layout.insertLayout(0, title_layout)
        return card
        
    def handle_top_menu_action(self, action_id):
        """مدیریت عملیات منوی بالا"""
        if action_id == "marriage-tutorial":
            # نمایش آموزش وام ازدواج
            pass
        elif action_id == "child-tutorial":
            # نمایش آموزش وام فرزند
            pass
        elif action_id == "settings-tutorial":
            # نمایش آموزش تنظیمات
            pass

class ContactPage(BasePage):
    """صفحه ارتباط با ما"""
    
    def __init__(self, parent=None):
        super().__init__("ارتباط با ما", parent)
        self.setup_contact_ui()
        
    def setup_contact_ui(self):
        """تنظیم UI ارتباط با ما"""
        # اطلاعات تماس
        contact_info = QFrame()
        contact_info.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(42, 42, 61, 0.5);
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        
        contact_layout = QVBoxLayout(contact_info)
        
        info_items = [
            ("📞 تلفن پشتیبانی:", "021-12345678"),
            ("📧 ایمیل:", "support@yara-system.com"),
            ("🌐 وب‌سایت:", "www.yara-system.com"),
            ("📱 تلگرام:", "@yara_support"),
            ("⏰ ساعات کاری:", "شنبه تا چهارشنبه 8 تا 16")
        ]
        
        for label, value in info_items:
            item_layout = QHBoxLayout()
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"color: {UIStyles.COLORS['dark_text']}; font-weight: bold; min-width: 150px;")
            
            value_widget = QLabel(value)
            value_widget.setStyleSheet("color: white; font-size: 14px;")
            
            item_layout.addWidget(label_widget)
            item_layout.addWidget(value_widget)
            item_layout.addStretch()
            
            contact_layout.addLayout(item_layout)
            
        self.content_layout.addWidget(contact_info)
        
        # فرم ارسال پیام
        message_form = QFrame()
        message_form.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(42, 42, 61, 0.5);
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 8px;
                padding: 20px;
                margin-top: 15px;
            }}
        """)
        
        form_layout = QVBoxLayout(message_form)
        
        form_title = QLabel("ارسال پیام به پشتیبانی")
        form_title.setStyleSheet("font-size: 16px; font-weight: bold; color: white; margin-bottom: 15px;")
        form_layout.addWidget(form_title)
        
        # فیلدهای فرم
        subject_input = QLineEdit()
        subject_input.setPlaceholderText("موضوع پیام...")
        subject_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {UIStyles.COLORS['dark_hover']};
                color: white;
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }}
        """)
        
        message_input = QTextEdit()
        message_input.setPlaceholderText("متن پیام...")
        message_input.setMaximumHeight(120)
        message_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {UIStyles.COLORS['dark_hover']};
                color: white;
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }}
        """)
        
        send_btn = QPushButton("ارسال پیام")
        send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {UIStyles.COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {UIStyles.COLORS['primary_light']};
            }}
        """)
        
        form_layout.addWidget(subject_input)
        form_layout.addWidget(message_input)
        form_layout.addWidget(send_btn)
        
        self.content_layout.addWidget(message_form)