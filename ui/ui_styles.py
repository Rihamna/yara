#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class UIStyles:
    """کلاس استایل‌های رابط کاربری مطابق طراحی ارسالی"""
    
    # رنگ‌های اصلی
    COLORS = {
        'bg_primary': '#2A2D3E',           # رنگ زمینه اصلی
        'bg_secondary': '#363A4F',         # رنگ زمینه ثانویه
        'bg_sidebar': '#2A2D3E',           # رنگ sidebar
        'bg_topbar': '#363A4F',            # رنگ منوی بالا
        'text_primary': '#FFFFFF',         # متن اصلی
        'text_secondary': '#8B92A8',       # متن ثانویه
        'text_muted': '#6B7280',           # متن کم‌رنگ
        'accent_blue': '#4F8EF7',          # آبی اکسنت (active)
        'accent_blue_hover': '#5A9BFF',    # آبی hover
        'border_color': '#4A4E5C',         # رنگ border
        'hover_bg': '#4A4E5C',             # رنگ hover background
    }
    
    @staticmethod
    def get_main_window_style():
        """استایل پنجره اصلی"""
        return f"""
            QMainWindow {{
                background-color: {UIStyles.COLORS['bg_primary']};
                color: {UIStyles.COLORS['text_primary']};
                font-family: 'Segoe UI', 'Tahoma', sans-serif;
            }}
        """
    
    @staticmethod
    def get_sidebar_style(collapsed=False):
        """استایل sidebar"""
        width = "60px" if collapsed else "240px"
        return f"""
            QFrame#sidebar {{
                background-color: {UIStyles.COLORS['bg_sidebar']};
                border-right: 1px solid {UIStyles.COLORS['border_color']};
                width: {width};
                min-width: {width};
                max-width: {width};
            }}
        """
    
    @staticmethod
    def get_sidebar_button_style():
        """استایل دکمه‌های sidebar"""
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {UIStyles.COLORS['text_secondary']};
                border: none;
                padding: 12px 16px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
                border-radius: 8px;
                margin: 2px 8px;
            }}
            QPushButton:hover {{
                background-color: {UIStyles.COLORS['hover_bg']};
                color: {UIStyles.COLORS['text_primary']};
            }}
            QPushButton:pressed {{
                background-color: {UIStyles.COLORS['accent_blue']};
                color: white;
            }}
            QPushButton[active="true"] {{
                background-color: {UIStyles.COLORS['accent_blue']};
                color: white;
            }}
        """
    
    @staticmethod
    def get_topbar_style():
        """استایل منوی بالایی"""
        return f"""
            QFrame#topbar {{
                background-color: {UIStyles.COLORS['bg_topbar']};
                border-bottom: 1px solid {UIStyles.COLORS['border_color']};
                padding: 0 20px;
                min-height: 60px;
                max-height: 60px;
            }}
        """
    
    @staticmethod
    def get_topbar_button_style():
        """استایل دکمه‌های منوی بالا"""
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {UIStyles.COLORS['text_secondary']};
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                margin: 0 4px;
            }}
            QPushButton:hover {{
                background-color: {UIStyles.COLORS['hover_bg']};
                color: {UIStyles.COLORS['text_primary']};
            }}
            QPushButton[active="true"] {{
                background-color: {UIStyles.COLORS['accent_blue']};
                color: white;
            }}
        """
    
    @staticmethod
    def get_toggle_button_style():
        """استایل دکمه toggle sidebar"""
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {UIStyles.COLORS['text_secondary']};
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {UIStyles.COLORS['hover_bg']};
                color: {UIStyles.COLORS['text_primary']};
            }}
        """
    
    @staticmethod
    def get_profile_button_style():
        """استایل دکمه پروفایل"""
        return f"""
            QPushButton {{
                background-color: {UIStyles.COLORS['accent_blue']};
                color: white;
                border: none;
                border-radius: 20px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {UIStyles.COLORS['accent_blue_hover']};
            }}
        """
    
    @staticmethod
    def get_content_area_style():
        """استایل ناحیه محتوا"""
        return f"""
            QWidget#contentArea {{
                background-color: {UIStyles.COLORS['bg_primary']};
                padding: 20px;
            }}
        """
    
    @staticmethod
    def get_card_style():
        """استایل کارت‌ها"""
        return f"""
            QFrame {{
                background-color: {UIStyles.COLORS['bg_secondary']};
                border: 1px solid {UIStyles.COLORS['border_color']};
                border-radius: 12px;
                padding: 20px;
            }}
        """
    
    # آیکن‌های متنی ساده (بدون SVG)
    ICONS = {
        'home': '🏠',
        'robot': '🤖', 
        'child': '👶',
        'marriage': '💍',
        'settings': '⚙️',
        'menu': '☰',
        'arrow_left': '◀',
        'user': '👤'
    }