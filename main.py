#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فایل اصلی اجرای برنامه YARA - سیستم مدیریت ربات‌های خودکار
این فایل نقطه ورودی برنامه است و مسئول راه‌اندازی رابط کاربری می‌باشد

نویسنده: سیستم خودکار YARA
تاریخ ایجاد: 2024
نسخه: 2.0

ویژگی‌های اصلی:
- مدیریت ربات‌های خودکار
- ثبت‌نام وام‌های بانکی
- رابط کاربری فارسی
- پشتیبانی از چندین بانک
"""

import os
print("Current directory:", os.getcwd())
print("Files in current directory:", os.listdir("."))
import sys
import os

# اضافه کردن مسیر پروژه به path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QFont, QFontDatabase
import traceback

from ui.main_window import MainWindow   

def setup_rtl_layout(app):
    """
    تنظیم Layout راست به چپ برای فارسی
    """
    try:
        app.setLayoutDirection(Qt.RightToLeft)
        return True
    except Exception as e:
        print(f"خطا در تنظیم RTL: {e}")
        return False


def setup_fonts(app):
    """
    تنظیم فونت‌های فارسی
    """
    try:
        # تنظیم فونت پیش‌فرض
        font = QFont("Tahoma", 10)
        font.setStyleHint(QFont.SansSerif)
        app.setFont(font)
        
        return True
    except Exception as e:
        print(f"خطا در تنظیم فونت: {e}")
        return False


def check_dependencies():
    """
    بررسی وجود وابستگی‌های مورد نیاز
    """
    missing_deps = []
    
    try:
        import PyQt5
    except ImportError:
        missing_deps.append("PyQt5")
        
    try:
        import selenium
    except ImportError:
        missing_deps.append("selenium")
        
    return missing_deps


def show_error_dialog(title, message):
    """
    نمایش پیام خطا
    """
    try:
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()
    except:
        print(f"{title}: {message}")


def main():
    """
    تابع اصلی برای اجرای برنامه
    """
    try:
        # بررسی وابستگی‌ها
        missing_deps = check_dependencies()
        if missing_deps:
            error_msg = f"پکیج‌های زیر نصب نیستند:\n{', '.join(missing_deps)}\n\nبرای نصب اجرا کنید:\npip install {' '.join(missing_deps)}"
            print(error_msg)
            return 1
        
        # ایجاد اپلیکیشن
        app = QApplication(sys.argv)
        app.setApplicationName("YARA")
        app.setApplicationDisplayName("YARA - سیستم مدیریت ربات‌های خودکار")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("YARA Systems")
        
        # تنظیمات زبان و فونت
        setup_rtl_layout(app)
        setup_fonts(app)
        
        # ایجاد پنجره اصلی
        try:
            window = MainWindow()
            window.show()
        except Exception as e:
            error_msg = f"خطا در راه‌اندازی پنجره اصلی:\n{str(e)}\n\nجزئیات:\n{traceback.format_exc()}"
            show_error_dialog("خطای راه‌اندازی", error_msg)
            return 1
        
        # شروع حلقه اصلی برنامه
        try:
            exit_code = app.exec_()
            return exit_code
        except KeyboardInterrupt:
            print("برنامه توسط کاربر متوقف شد")
            return 0
        except Exception as e:
            error_msg = f"خطای غیرمنتظره:\n{str(e)}\n\nجزئیات:\n{traceback.format_exc()}"
            show_error_dialog("خطای اجرا", error_msg)
            return 1
            
    except Exception as e:
        print(f"خطای کلی در برنامه: {str(e)}")
        print(f"جزئیات: {traceback.format_exc()}")
        return 1


if __name__ == "__main__":
    """
    اجرای برنامه در صورت فراخوانی مستقیم
    """
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"خطای نهایی: {str(e)}")
        sys.exit(1)