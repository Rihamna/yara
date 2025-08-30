#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class UIStyles:
    """استایل‌های رابط کاربری مطابق طراحی HTML ارسالی"""
    
    # رنگ‌های دقیق مطابق HTML
    COLORS = {
        'primary': '#2563eb',              # آبی اصلی
        'primary_light': '#3b82f6',        # آبی روشن
        'primary_dark': '#1e40af',         # آبی تیره
        'dark_bg': '#1E1E2D',              # زمینه sidebar
        'dark_secondary': '#2A2A3D',       # زمینه ثانویه
        'dark_text': '#E0E0E0',            # متن اصلی
        'dark_hover': '#3A3A4D',           # hover
        'dark_active': '#1d4ed8',          # active
        'dark_border': '#3D3D50',          # border
        'body_bg': '#0F0F1A',              # زمینه کل برنامه
        'glow_color': 'rgba(37, 99, 235, 0.5)',  # افکت glow
    }
    
    @staticmethod
    def get_main_window_style():
        """استایل پنجره اصلی"""
        return f"""
            QMainWindow, QWidget {{
                background-color: {UIStyles.COLORS['body_bg']};
                color: {UIStyles.COLORS['dark_text']};
                font-family: 'Segoe UI', 'Tahoma', sans-serif;
                font-size: 14px;
            }}
        """
    
    @staticmethod
    def get_sidebar_style():
        """استایل sidebar"""
        return f"""
            QFrame#sidebar {{
                background-color: {UIStyles.COLORS['dark_bg']};
                border-left: 1px solid {UIStyles.COLORS['dark_border']};
                border-right: none;
                border-top: none;
                border-bottom: none;
            }}
        """
    
    @staticmethod
    def get_sidebar_header_style():
        """استایل هدر sidebar"""
        return f"""
            QFrame#sidebarHeader {{
                background-color: {UIStyles.COLORS['dark_bg']};
                border-bottom: 1px solid {UIStyles.COLORS['dark_border']};
                padding: 17px 13px;
                min-height: 60px;
                max-height: 60px;
            }}
        """
    
    @staticmethod
    def get_logo_style():
        """استایل لوگو YARA"""
        return f"""
            QLabel#logo {{
                color: white;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }}
        """
    
    @staticmethod
    def get_profile_button_style():
        """استایل دکمه پروفایل"""
        return f"""
            QPushButton#profileBtn {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {UIStyles.COLORS['primary']}, 
                    stop:1 {UIStyles.COLORS['primary_light']});
                color: white;
                border: none;
                border-radius: 18px;
                font-weight: bold;
                font-size: 14px;
                min-width: 36px;
                max-width: 36px;
                min-height: 36px;
                max-height: 36px;
            }}
            QPushButton#profileBtn:hover {{
                transform: scale(1.05);
            }}
        """
    
    @staticmethod
    def get_toggle_button_style():
        """استایل دکمه toggle"""
        return f"""
            QPushButton#toggleBtn {{
                background-color: {UIStyles.COLORS['dark_bg']};
                color: {UIStyles.COLORS['dark_text']};
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 14px;
                font-size: 12px;
                min-width: 28px;
                max-width: 28px;
                min-height: 28px;
                max-height: 28px;
            }}
            QPushButton#toggleBtn:hover {{
                background-color: {UIStyles.COLORS['dark_hover']};
            }}
        """
    
    @staticmethod
    def get_menu_item_style():
        """استایل آیتم‌های منو"""
        return f"""
            QFrame.menuItem {{
                background-color: {UIStyles.COLORS['dark_secondary']};
                border-radius: 8px;
                margin: 4px 10px;
            }}
        """
    
    @staticmethod
    def get_menu_button_style():
        """استایل دکمه‌های منو"""
        return f"""
            QPushButton.menuBtn {{
                background-color: transparent;
                color: {UIStyles.COLORS['dark_text']};
                border: none;
                padding: 10px 15px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
                border-radius: 8px;
            }}
            QPushButton.menuBtn:hover {{
                background-color: {UIStyles.COLORS['dark_hover']};
                padding-right: 18px;
            }}
            QPushButton.menuBtn:pressed {{
                background-color: {UIStyles.COLORS['dark_active']};
                color: white;
            }}
            QPushButton.menuBtn[active="true"] {{
                background-color: {UIStyles.COLORS['dark_active']};
                color: white;
            }}
        """
    
    @staticmethod
    def get_submenu_style():
        """استایل زیرمنو"""
        return f"""
            QFrame.submenu {{
                background-color: rgba(42, 42, 61, 0.7);
                margin-left: 15px;
                border-radius: 6px;
            }}
        """
    
    @staticmethod
    def get_submenu_button_style():
        """استایل دکمه‌های زیرمنو"""
        return f"""
            QPushButton.submenuBtn {{
                background-color: transparent;
                color: {UIStyles.COLORS['dark_text']};
                border: none;
                padding: 8px 15px 8px 12px;
                text-align: left;
                font-size: 13px;
                border-radius: 6px;
                opacity: 0.9;
            }}
            QPushButton.submenuBtn:hover {{
                background-color: {UIStyles.COLORS['dark_hover']};
                padding-right: 18px;
                opacity: 1;
            }}
            QPushButton.submenuBtn[active="true"] {{
                background-color: {UIStyles.COLORS['primary_dark']};
                color: white;
                font-weight: bold;
            }}
        """
    
    @staticmethod
    def get_top_menu_style():
        """استایل منوی بالایی"""
        return f"""
            QFrame#topMenu {{
                background-color: {UIStyles.COLORS['dark_secondary']};
                border-bottom: 1px solid {UIStyles.COLORS['dark_border']};
                min-height: 60px;
                max-height: 60px;
                padding: 0 20px;
            }}
        """
    
    @staticmethod
    def get_top_menu_title_style():
        """استایل عنوان منوی بالا"""
        return f"""
            QLabel#topMenuTitle {{
                color: {UIStyles.COLORS['dark_text']};
                font-size: 18px;
                font-weight: bold;
            }}
        """
    
    @staticmethod
    def get_top_menu_button_style():
        """استایل دکمه‌های منوی بالا"""
        return f"""
            QPushButton.topMenuBtn {{
                background-color: rgba(42, 42, 61, 0.7);
                color: {UIStyles.COLORS['dark_text']};
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 6px;
                padding: 8px 15px;
                font-size: 14px;
                margin: 0 5px;
            }}
            QPushButton.topMenuBtn:hover {{
                background-color: {UIStyles.COLORS['dark_hover']};
            }}
            QPushButton.topMenuBtn[active="true"] {{
                background-color: {UIStyles.COLORS['dark_active']};
                color: white;
                border-color: {UIStyles.COLORS['primary']};
            }}
        """
    
    @staticmethod
    def get_content_area_style():
        """استایل ناحیه محتوا"""
        return f"""
            QWidget#contentArea {{
                background-color: {UIStyles.COLORS['body_bg']};
                padding: 20px;
            }}
        """
    
    @staticmethod
    def get_page_content_style():
        """استایل محتوای صفحات"""
        return f"""
            QFrame.pageContent {{
                background-color: {UIStyles.COLORS['dark_secondary']};
                border: 1px solid {UIStyles.COLORS['dark_border']};
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
            }}
        """
    
    @staticmethod
    def get_page_title_style():
        """استایل عنوان صفحات"""
        return f"""
            QLabel.pageTitle {{
                color: {UIStyles.COLORS['primary_light']};
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid {UIStyles.COLORS['dark_border']};
            }}
        """

    # آیکن‌های متنی (Font Awesome Unicode)
    ICONS = {
        'home': '🏠',
        'robot': '🤖',
        'child': '👶',
        'marriage': '💕',
        'settings': '⚙️',
        'news': '📰',
        'education': '🎓',
        'contact': '✉️',
        'user': 'U',
        'toggle_open': '◀',
        'toggle_close': '☰',
        'arrow_left': '◀',
        'arrow_right': '▶',
    }