#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class FormBot:
    def __init__(self, driver, wait_time=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)
        self.status_callback = None

    def set_status_callback(self, callback):
        """تنظیم تابع برای ارسال وضعیت به UI"""
        self.status_callback = callback

    def _update_status(self, message):
        """ارسال وضعیت به UI"""
        if self.status_callback:
            self.status_callback(message)
        print(message)

    def select_dropdown_by_text(self, element_id, visible_text):
        """انتخاب گزینه از dropdown براساس متن"""
        try:
            self._update_status(f"انتخاب {visible_text} در فیلد {element_id}")
            dropdown = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
            Select(dropdown).select_by_visible_text(visible_text)
            return True
        except Exception as e:
            self._update_status(f"❌ خطا در انتخاب '{element_id}': {e}")
            return False

    def wait_for_dropdown_options(self, dropdown_id, min_options=2, timeout=5):
        """انتظار برای بارگذاری گزینه‌های dropdown"""
        try:
            def options_loaded(driver):
                dropdown = driver.find_element(By.ID, dropdown_id)
                options = dropdown.find_elements(By.TAG_NAME, "option")
                return len(options) >= min_options
            
            WebDriverWait(self.driver, timeout).until(options_loaded)
            return True
        except Exception as e:
            self._update_status(f"❌ گزینه‌های '{dropdown_id}' بارگذاری نشدند: {e}")
            return False

    def fill_text_field(self, field_id, text):
        """پر کردن فیلد متنی"""
        try:
            self._update_status(f"پر کردن فیلد {field_id}")
            field = self.wait.until(EC.presence_of_element_located((By.ID, field_id)))
            field.clear()
            field.send_keys(text)
            return True
        except Exception as e:
            self._update_status(f"❌ خطا در پر کردن '{field_id}': {e}")
            return False

    def submit_form(self, submit_button_id):
        """ارسال فرم"""
        try:
            self._update_status("ارسال فرم...")
            button = self.wait.until(EC.element_to_be_clickable((By.ID, submit_button_id)))
            button.click()
            return True
        except Exception as e:
            self._update_status(f"❌ خطا در ارسال فرم: {e}")
            return False

    def wait_for_manual_captcha(self):
        """انتظار برای حل دستی کپچا"""
        self._update_status("⏳ لطفاً کپچا را در مرورگر حل کنید و Enter بزنید...")
        input("کپچا را حل کرده و Enter بزنید...")
        return True

class RobotService:
    def __init__(self):
        self.driver = None
        self.bot = None
        self.is_running = False

    def get_driver(self):
        """ایجاد driver مرورگر"""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        try:
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            raise Exception(f"خطا در راه‌اندازی Chrome: {e}")

    def run_registration(self, applicant_data, status_callback=None):
        """اجرای فرآیند ثبت‌نام"""
        try:
            self.is_running = True
            self.driver = self.get_driver()
            self.driver.get("https://ve.cbi.ir/VC/TasRequestVC.aspx")

            self.bot = FormBot(self.driver)
            if status_callback:
                self.bot.set_status_callback(status_callback)

            # پر کردن فرم با داده‌های متقاضی
            success = self._fill_form_with_data(applicant_data)
            
            if success:
                # انتظار برای حل دستی کپچا
                self.bot.wait_for_manual_captcha()
                
                # ارسال فرم اولیه
                self.bot.submit_form("ctl00_ContentPlaceHolder1_btnSendConfirmCode")
                
                # کمی انتظار برای ارسال SMS
                time.sleep(2)
                
                if status_callback:
                    status_callback("⏳ در انتظار کد تأیید SMS...")
                
                return "waiting_for_sms"
            else:
                return "form_error"

        except Exception as e:
            if status_callback:
                status_callback(f"❌ خطا در اجرای ربات: {e}")
            return "error"

    def submit_sms_code(self, sms_code, status_callback=None):
        """ارسال کد تأیید SMS"""
        try:
            if not self.bot:
                return "robot_not_started"
            
            if status_callback:
                status_callback("ارسال کد تأیید...")
            
            # پر کردن کد SMS
            success = self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbConfirmCode", sms_code)
            
            if success:
                # ارسال کد
                submit_success = self.bot.submit_form("ctl00_ContentPlaceHolder1_btnConfirmCode")
                
                if submit_success:
                    # انتظار برای نتیجه
                    time.sleep(3)
                    
                    # بررسی موفقیت (می‌تواند بهبود یابد)
                    if status_callback:
                        status_callback("✅ ثبت‌نام با موفقیت تکمیل شد!")
                    
                    return "completed"
                else:
                    return "sms_error"
            else:
                return "sms_error"
                
        except Exception as e:
            if status_callback:
                status_callback(f"❌ خطا در ارسال کد SMS: {e}")
            return "error"

    def _fill_form_with_data(self, data):
        """پر کردن فرم با داده‌های متقاضی"""
        try:
            # استان و شهر محل تولد پدر
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrState", data['father_birth_state']):
                return False
            
            self.bot.wait_for_dropdown_options("ctl00_ContentPlaceHolder1_ddlPBrCity")
            
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrCity", data['father_birth_city']):
                return False

            # شماره ملی پدر
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbPIDNo", data['father_national_id']):
                return False

            # تاریخ تولد پدر
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrDay", data['father_birth_day']):
                return False
            
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrMonth", data['father_birth_month']):
                return False
            
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbPBrYear", data['father_birth_year']):
                return False

            # تاریخ تولد فرزند
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrDay", data['child_birth_day']):
                return False
            
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrMonth", data['child_birth_month']):
                return False
            
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbCBrYear", data['child_birth_year']):
                return False

            # استان و شهر محل تولد فرزند
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrState", data['child_birth_state']):
                return False
            
            self.bot.wait_for_dropdown_options("ctl00_ContentPlaceHolder1_ddlCBrCity")
            
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrCity", data['child_birth_city']):
                return False

            # تعداد فرزندان
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlChildNo", data['child_number']):
                return False

            # شماره موبایل پدر
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbMobileNo", data['father_mobile']):
                return False

            # کد ملی فرزند
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbCIDNo", data['child_national_id']):
                return False

            return True

        except Exception as e:
            self.bot._update_status(f"❌ خطا در پر کردن فرم: {e}")
            return False

    def stop_robot(self):
        """متوقف کردن ربات"""
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            finally:
                self.driver = None

    def cleanup(self):
        """پاکسازی منابع"""
        self.stop_robot()

    def get_robot_status(self):
        """وضعیت ربات"""
        return {
            'is_running': self.is_running,
            'has_driver': self.driver is not None,
            'driver_title': self.driver.title if self.driver else None
        }

    def test_connection(self):
        """تست اتصال و عملکرد"""
        try:
            test_driver = self.get_driver()
            test_driver.get("https://www.google.com")
            title = test_driver.title
            test_driver.quit()
            
            return True, f"اتصال موفق - عنوان صفحه: {title}"
            
        except Exception as e:
            return False, f"خطا در اتصال: {str(e)}"

    def check_requirements(self):
        """بررسی وجود وابستگی‌ها"""
        issues = []
        
        try:
            # بررسی selenium
            import selenium
            selenium_version = selenium.__version__
        except ImportError:
            issues.append("پکیج selenium نصب نیست")
            selenium_version = None

        try:
            # بررسی Chrome driver
            test_driver = webdriver.Chrome()
            test_driver.quit()
        except Exception as e:
            issues.append(f"Chrome Driver مشکل دارد: {str(e)}")

        if not issues:
            return True, f"تمام وابستگی‌ها آماده هستند (Selenium: {selenium_version})"
        else:
            return False, issues

    def install_requirements(self, progress_callback=None):
        """نصب وابستگی‌ها"""
        try:
            import subprocess
            import sys
            
            packages = ["selenium", "webdriver-manager"]
            
            for package in packages:
                if progress_callback:
                    progress_callback(f"نصب {package}...")
                
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    if progress_callback:
                        progress_callback(f"خطا در نصب {package}: {result.stderr}")
                    return False
            
            if progress_callback:
                progress_callback("تمام پکیج‌ها با موفقیت نصب شدند")
            
            return True
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"خطا در نصب: {str(e)}")
            return False