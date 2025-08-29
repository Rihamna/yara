#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QFrame, QLabel, QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QEasingCurve, QPropertyAnimation, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from .ui_styles import UIStyles

class SidebarButton(QPushButton):
    """دکمه‌های منوی کناری با آیکن متنی"""
    
    def __init__(self, text, icon_text, parent=None, is_submenu=False):
        super().__init__(parent)
        self.text = text
        self.icon_text = icon_text  # متن آیکن به جای SVG
        self.is_submenu = is_submenu
        self.is_active = False
        
        self.setMinimumHeight(44)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16 if not self.is_submenu else 32, 8, 16, 8)
        layout.setSpacing(12)
        
        # آیکن متنی (emoji یا نماد)
        self.icon_label = QLabel(self.icon_text)
        self.icon_label.setFixedSize(20, 20)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet(f"color: {UIStyles.COLORS['text_secondary']}; font-size: 16px;")
        
        # متن
        self.text_label = QLabel(self.text)
        self.text_label.setStyleSheet(f"color: {UIStyles.COLORS['text_secondary']}; font-weight: 500;")
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addStretch()
        
        self.setStyleSheet(UIStyles.get_sidebar_button_style())
        
    def set_active(self, active):
        """تنظیم وضعیت فعال/غیرفعال"""
        self.is_active = active
        self.setProperty("active", active)
        
        icon_color = "white" if active else UIStyles.COLORS['text_secondary']
        text_color = "white" if active else UIStyles.COLORS['text_secondary']
        
        self.icon_label.setStyleSheet(f"color: {icon_color}; font-size: 16px;")
        self.text_label.setStyleSheet(f"color: {text_color}; font-weight: 500;")
        self.style().polish(self)
        
    def enterEvent(self, event):
        """رویداد hover"""
        if not self.is_active:
            self.icon_label.setStyleSheet("color: white; font-size: 16px;")
            self.text_label.setStyleSheet("color: white; font-weight: 500;")
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """رویداد خروج از hover"""
        if not self.is_active:
            color = UIStyles.COLORS['text_secondary']
            self.icon_label.setStyleSheet(f"color: {color}; font-size: 16px;")
            self.text_label.setStyleSheet(f"color: {color}; font-weight: 500;")
        super().leaveEvent(event)

class CollapsibleSidebar(QFrame):
    """منوی کناری جمع‌شونده"""
    
    menu_clicked = pyqtSignal(str)  # سیگنال کلیک روی منو
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.collapsed = False
        self.animation_duration = 350
        
        self.setFixedWidth(240)
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        """تنظیم رابط کاربری"""
        self.setStyleSheet(UIStyles.get_sidebar_style(self.collapsed))
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # هدر با لوگو و دکمه toggle
        self.create_header(main_layout)
        
        # منوهای اصلی
        self.create_main_menu(main_layout)
        
        main_layout.addStretch()
        
    def create_header(self, parent_layout):
        """ایجاد هدر sidebar"""
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 20, 16, 20)
        
        # لوگو YARA
        self.logo_label = QLabel("YARA")
        self.logo_label.setStyleSheet("""
            color: white; 
            font-size: 20px; 
            font-weight: bold;
            font-family: 'Segoe UI', sans-serif;
        """)
        
        header_layout.addWidget(self.logo_label)
        header_layout.addStretch()
        
        # دکمه toggle
        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setFixedSize(32, 32)
        self.toggle_btn.setStyleSheet(UIStyles.get_toggle_button_style())
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        
        header_layout.addWidget(self.toggle_btn)
        parent_layout.addWidget(header_frame)
        
    def create_main_menu(self, parent_layout):
        """ایجاد منوهای اصلی"""
        menu_frame = QFrame()
        self.menu_layout = QVBoxLayout(menu_frame)
        self.menu_layout.setContentsMargins(0, 10, 0, 10)
        self.menu_layout.setSpacing(4)
        
        # منو صفحه اصلی
        self.home_btn = SidebarButton("صفحه اصلی", "🏠")
        self.home_btn.clicked.connect(lambda: self.menu_clicked.emit("home"))
        self.menu_layout.addWidget(self.home_btn)
        
        # منو ربات‌ها (با زیرمنو)
        self.robots_btn = SidebarButton("ربات ها", "🤖")
        self.robots_btn.clicked.connect(self.toggle_robots_submenu)
        self.menu_layout.addWidget(self.robots_btn)
        
        # زیرمنوی ربات‌ها
        self.submenu_frame = QFrame()
        self.submenu_layout = QVBoxLayout(self.submenu_frame)
        self.submenu_layout.setContentsMargins(0, 0, 0, 0)
        self.submenu_layout.setSpacing(2)
        
        # ربات وام فرزند
        self.child_loan_btn = SidebarButton("ربات وام فرزند", "👶", is_submenu=True)
        self.child_loan_btn.clicked.connect(lambda: self.menu_clicked.emit("child-loan"))
        self.submenu_layout.addWidget(self.child_loan_btn)
        
        # ربات وام ازدواج
        self.marriage_loan_btn = SidebarButton("ربات وام ازدواج", "💍", is_submenu=True)
        self.marriage_loan_btn.clicked.connect(lambda: self.menu_clicked.emit("marriage-loan"))
        self.submenu_layout.addWidget(self.marriage_loan_btn)
        
        self.submenu_frame.hide()  # ابتدا مخفی
        self.menu_layout.addWidget(self.submenu_frame)
        
        # ذخیره دکمه‌ها برای مدیریت active state
        self.menu_buttons = {
            "home": self.home_btn,
            "robots": self.robots_btn,
            "child-loan": self.child_loan_btn,
            "marriage-loan": self.marriage_loan_btn
        }
        
        parent_layout.addWidget(menu_frame)
        
    def setup_animation(self):
        """تنظیم انیمیشن‌ها"""
        self.width_animation = QPropertyAnimation(self, b"maximumWidth")
        self.width_animation.setDuration(self.animation_duration)
        self.width_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def toggle_sidebar(self):
        """تغییر وضعیت باز/بسته sidebar"""
        self.collapsed = not self.collapsed
        
        target_width = 60 if self.collapsed else 240
        
        self.width_animation.setStartValue(self.width())
        self.width_animation.setEndValue(target_width)
        self.width_animation.start()
        
        # بروزرسانی دکمه toggle
        self.update_toggle_button()
        self.update_collapsed_state()
        
    def update_toggle_button(self):
        """بروزرسانی دکمه toggle"""
        icon_text = "◀" if not self.collapsed else "☰"
        self.toggle_btn.setText(icon_text)
        
    def update_collapsed_state(self):
        """بروزرسانی وضعیت collapsed"""
        if self.collapsed:
            self.logo_label.hide()
            # مخفی کردن متن دکمه‌ها
            for button in self.menu_buttons.values():
                button.text_label.hide()
            self.submenu_frame.hide()
        else:
            self.logo_label.show()
            # نمایش متن دکمه‌ها
            for button in self.menu_buttons.values():
                button.text_label.show()
                
    def toggle_robots_submenu(self):
        """تغییر وضعیت زیرمنوی ربات‌ها"""
        if self.collapsed:
            return
            
        if self.submenu_frame.isVisible():
            self.submenu_frame.hide()
        else:
            self.submenu_frame.show()
            
    def set_active_menu(self, menu_id):
        """تنظیم منوی فعال"""
        for btn_id, button in self.menu_buttons.items():
            button.set_active(btn_id == menu_id)
            
        # مدیریت زیرمنو
        if menu_id in ["child-loan", "marriage-loan"]:
            self.submenu_frame.show()
            self.robots_btn.set_active(True)