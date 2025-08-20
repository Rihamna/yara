#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.main_window import MainWindow

def setup_app():
    """تنظیمات اولیه برنامه"""
    app = QApplication(sys.argv)
    
    # تنظیم فونت فارسی
    font = QFont("Tahoma", 10)
    app.setFont(font)
    
    # تنظیم راست به چپ
    app.setLayoutDirection(Qt.RightToLeft)
    
    # تنظیم encoding برای فارسی
    app.setProperty("encoding", "utf-8")
    
    return app

def create_data_directories():
    """ایجاد پوشه‌های مورد نیاز"""
    directories = [
        'data',
        'data/robot_data',
        'data/robot_data/وام_فرزندآوری',
        'data/robot_data/وام_ازدواج',
        'data/backups',
        'logs'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def main():
    """تابع اصلی برنامه"""
    try:
        # ایجاد پوشه‌ها
        create_data_directories()
        
        # راه‌اندازی برنامه
        app = setup_app()
        
        # ایجاد پنجره اصلی
        main_window = MainWindow()
        main_window.show()
        
        # اجرای برنامه
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"خطا در اجرای برنامه: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()