#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سرویس Backend ربات وام فرزندآوری
این فایل مسئول منطق اجرای ربات و تعامل با سایت بانک مرکزی می‌باشد

نویسنده: سیستم خودکار YARA
تاریخ ایجاد: 2024
نسخه: 2.0 - جداسازی UI و Backend

ویژگی‌های Backend:
- مدیریت Selenium WebDriver
- پر کردن خودکار فرم‌ها
- مدیریت کپچا
- ارسال SMS و تأیید
"""

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
    """کلاس مدیریت فرم‌های وب"""
    
    def __init__(self, driver, wait_time=15):
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
        print(f"Bot Status: {message}")

    def select_dropdown_by_text(self, element_id, visible_text):
        """انتخاب گزینه از dropdown براساس متن"""
        try:
            self._update_status(f"انتخاب '{visible_text}' در فیلد {element_id}")
            dropdown = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
            
            # انتظار برای بارگذاری گزینه‌ها
            time.sleep(1)
            
            select_element = Select(dropdown)
            
            # جستجوی دقیق متن
            found = False
            for option in select_element.options:
                if option.text.strip() == visible_text.strip():
                    select_element.select_by_visible_text(visible_text)
                    found = True
                    break
                    
            if not found:
                # تلاش برای انتخاب براساس شامل بودن متن
                for option in select_element.options:
                    if visible_text.strip() in option.text.strip():
                        select_element.select_by_visible_text(option.text)
                        found = True
                        break
                        
            if not found:
                self._update_status(f"⚠️ گزینه '{visible_text}' یافت نشد در {element_id}")
                return False
                
            self._update_status(f"✅ انتخاب شد: {visible_text}")
            return True
            
        except Exception as e:
            self._update_status(f"❌ خطا در انتخاب '{element_id}': {str(e)}")
            return False

    def wait_for_dropdown_options(self, dropdown_id, min_options=2, timeout=10):
        """انتظار برای بارگذاری گزینه‌های dropdown"""
        try:
            self._update_status(f"انتظار برای بارگذاری گزینه‌های {dropdown_id}...")
            
            def options_loaded(driver):
                dropdown = driver.find_element(By.ID, dropdown_id)
                options = dropdown.find_elements(By.TAG_NAME, "option")
                return len(options) >= min_options
            
            WebDriverWait(self.driver, timeout).until(options_loaded)
            time.sleep(0.5)  # کمی انتظار اضافی
            return True
            
        except Exception as e:
            self._update_status(f"❌ گزینه‌های '{dropdown_id}' بارگذاری نشدند: {str(e)}")
            return False

    def fill_text_field(self, field_id, text):
        """پر کردن فیلد متنی"""
        try:
            self._update_status(f"پر کردن فیلد {field_id} با: {text}")
            field = self.wait.until(EC.presence_of_element_located((By.ID, field_id)))
            
            # پاک کردن محتوای قبلی
            field.clear()
            time.sleep(0.2)
            
            # وارد کردن متن جدید
            field.send_keys(text)
            
            # تأیید وارد شدن متن
            if field.get_attribute("value") == text:
                self._update_status(f"✅ فیلد {field_id} پر شد")
                return True
            else:
                self._update_status(f"⚠️ محتوای فیلد {field_id} تأیید نشد")
                return False
                
        except Exception as e:
            self._update_status(f"❌ خطا در پر کردن '{field_id}': {str(e)}")
            return False

    def click_button(self, button_id):
        """کلیک روی دکمه"""
        try:
            self._update_status(f"کلیک روی دکمه {button_id}")
            button = self.wait.until(EC.element_to_be_clickable((By.ID, button_id)))
            
            # اسکرول به دکمه
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(0.5)
            
            # کلیک
            button.click()
            self._update_status(f"✅ کلیک شد: {button_id}")
            return True
            
        except Exception as e:
            self._update_status(f"❌ خطا در کلیک '{button_id}': {str(e)}")
            return False

    def wait_for_manual_captcha(self, timeout=300):
        """انتظار برای حل دستی کپچا"""
        self._update_status("⏳ لطفاً کپچا را در مرورگر حل کنید...")
        
        # نمایش alert برای کاربر
        self.driver.execute_script("""
            alert('لطفاً کپچا را حل کنید و سپس OK بزنید');
        """)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # بررسی وجود alert
                alert = self.driver.switch_to.alert
                alert.accept()
                self._update_status("✅ کپچا حل شد")
                return True
            except:
                time.sleep(1)
                continue
                
        self._update_status("❌ زمان حل کپچا تمام شد")
        return False

    def check_for_errors(self):
        """بررسی وجود پیام‌های خطا در صفحه"""
        try:
            # جستجوی عناصر خطا معمول
            error_selectors = [
                "span[style*='color:red']",
                ".error",
                ".alert-danger",
                "[id*='error']",
                "[class*='error']"
            ]
            
            for selector in error_selectors:
                try:
                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in error_elements:
                        if element.is_displayed() and element.text.strip():
                            return element.text.strip()
                except:
                    continue
                    
            return None
            
        except Exception:
            return None


class ChildLoanRobotService:
    """سرویس اصلی ربات وام فرزند"""
    
    def __init__(self):
        self.driver = None
        self.bot = None
        self.is_running = False
        self.target_url = "https://ve.cbi.ir/VC/TasRequestVC.aspx"

    def get_driver(self):
        """ایجاد driver مرورگر Chrome"""
        options = Options()
        
        # تنظیمات بهینه‌سازی
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        # تنظیمات زبان فارسی
        options.add_experimental_option('prefs', {
            'intl.accept_languages': 'fa-IR,fa,en-US,en'
        })
        
        # User Agent
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(10)
            return driver
            
        except Exception as e:
            raise Exception(f"خطا در راه‌اندازی Chrome: {str(e)}")

    def run_registration(self, applicant_data, status_callback=None):
        """اجرای فرآیند ثبت‌نام"""
        try:
            self.is_running = True
            
            # راه‌اندازی درایور
            if status_callback:
                status_callback("راه‌اندازی مرورگر...")
                
            self.driver = self.get_driver()
            
            # رفتن به صفحه هدف
            if status_callback:
                status_callback("بارگذاری صفحه...")
                
            self.driver.get(self.target_url)
            
            # انتظار برای بارگذاری کامل صفحه
            time.sleep(3)
            
            # ایجاد bot
            self.bot = FormBot(self.driver)
            if status_callback:
                self.bot.set_status_callback(status_callback)

            # پر کردن فرم با داده‌های متقاضی
            success = self._fill_form_with_data(applicant_data)
            
            if not success:
                return "form_error"

            # حل کپچا
            if status_callback:
                status_callback("منتظر حل کپچا...")
                
            captcha_result = self.bot.wait_for_manual_captcha()
            if not captcha_result:
                return "captcha_error"

            # ارسال فرم اولیه
            if status_callback:
                status_callback("ارسال درخواست...")
                
            submit_success = self.bot.click_button("ctl00_ContentPlaceHolder1_btnSendConfirmCode")
            
            if not submit_success:
                return "submit_error"

            # انتظار برای ارسال SMS
            time.sleep(3)
            
            # بررسی خطاها
            error_message = self.bot.check_for_errors()
            if error_message:
                if status_callback:
                    status_callback(f"خطا: {error_message}")
                return "server_error"
            
            if status_callback:
                status_callback("⏳ در انتظار کد تأیید SMS...")
            
            return "waiting_for_sms"

        except Exception as e:
            if status_callback:
                status_callback(f"❌ خطا در اجرای ربات: {str(e)}")
            return "error"

    def submit_sms_code(self, sms_code, status_callback=None):
        """ارسال کد تأیید SMS"""
        try:
            if not self.bot or not self.driver:
                return "robot_not_started"
            
            if status_callback:
                status_callback("در حال ارسال کد تأیید...")
            
            # پر کردن کد SMS
            success = self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbConfirmCode", sms_code)
            
            if not success:
                return "sms_input_error"

            # ارسال کد
            submit_success = self.bot.click_button("ctl00_ContentPlaceHolder1_btnConfirmCode")
            
            if not submit_success:
                return "sms_submit_error"

            # انتظار برای پردازش
            time.sleep(5)
            
            # بررسی نتیجه
            current_url = self.driver.current_url
            page_source = self.driver.page_source
            
            # بررسی پیام‌های موفقیت یا خطا
            if "موفق" in page_source or "تکمیل" in page_source or "success" in page_source.lower():
                if status_callback:
                    status_callback("✅ ثبت‌نام با موفقیت تکمیل شد!")
                return "completed"
                
            # بررسی خطاها
            error_message = self.bot.check_for_errors()
            if error_message:
                if status_callback:
                    status_callback(f"خطا: {error_message}")
                return "sms_error"
            
            # بررسی تغییر URL (نشان‌دهنده موفقیت)
            if current_url != self.target_url:
                if status_callback:
                    status_callback("✅ ثبت‌نام با موفقیت تکمیل شد!")
                return "completed"
            
            # در غیر این صورت، ناموفق
            if status_callback:
                status_callback("❌ کد تأیید نادرست است")
            return "sms_error"
                
        except Exception as e:
            if status_callback:
                status_callback(f"❌ خطا در ارسال کد SMS: {str(e)}")
            return "error"

    def _fill_form_with_data(self, data):
        """پر کردن فرم با داده‌های متقاضی"""
        try:
            self.bot._update_status("شروع پر کردن فرم...")

            # استان محل تولد پدر
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrState", data['father_birth_state']):
                return False
            
            # انتظار برای بارگذاری شهرها
            if not self.bot.wait_for_dropdown_options("ctl00_ContentPlaceHolder1_ddlPBrCity"):
                return False
            
            # شهر محل تولد پدر
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrCity", data['father_birth_city']):
                return False

            # شماره ملی پدر
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbPIDNo", data['father_national_id']):
                return False

            # تاریخ تولد پدر - روز
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrDay", data['father_birth_day']):
                return False
            
            # تاریخ تولد پدر - ماه
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrMonth", data['father_birth_month']):
                return False
            
            # تاریخ تولد پدر - سال
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbPBrYear", data['father_birth_year']):
                return False

            # تاریخ تولد فرزند - روز
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrDay", data['child_birth_day']):
                return False
            
            # تاریخ تولد فرزند - ماه
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrMonth", data['child_birth_month']):
                return False
            
            # تاریخ تولد فرزند - سال
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbCBrYear", data['child_birth_year']):
                return False

            # استان محل تولد فرزند
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrState", data['child_birth_state']):
                return False
            
            # انتظار برای بارگذاری شهرهای فرزند
            if not self.bot.wait_for_dropdown_options("ctl00_ContentPlaceHolder1_ddlCBrCity"):
                return False
            
            # شهر محل تولد فرزند
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrCity", data['child_birth_city']):
                return False

            # تعداد فرزندان
            child_number_mapping = {
                "اول": "1",
                "دوم": "2", 
                "سوم": "3",
                "چهارم": "4",
                "پنجم": "5"
            }
            
            child_number_value = child_number_mapping.get(data['child_number'], data['child_number'])
            if not self.bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlChildNo", child_number_value):
                return False

            # شماره موبایل پدر
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbMobileNo", data['father_mobile']):
                return False

            # کد ملی فرزند
            if not self.bot.fill_text_field("ctl00_ContentPlaceHolder1_tbCIDNo", data['child_national_id']):
                return False

            self.bot._update_status("✅ فرم با موفقیت پر شد")
            return True

        except Exception as e:
            self.bot._update_status(f"❌ خطا در پر کردن فرم: {str(e)}")
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
                self.bot = None

    def cleanup(self):
        """پاکسازی منابع"""
        self.stop_robot()

    def get_robot_status(self):
        """وضعیت ربات"""
        return {
            'is_running': self.is_running,
            'has_driver': self.driver is not None,
            'driver_title': self.driver.title if self.driver else None,
            'current_url': self.driver.current_url if self.driver else None
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

        # بررسی دسترسی به سایت
        try:
            test_driver = self.get_driver()
            test_driver.get(self.target_url)
            if "تسهیلات ضروری" not in test_driver.title:
                issues.append("دسترسی به سایت بانک مرکزی مشکل دارد")
            test_driver.quit()
        except Exception as e:
            issues.append(f"خطا در اتصال به سایت: {str(e)}")

        if not issues:
            return True, f"تمام وابستگی‌ها آماده هستند (Selenium: {selenium_version})"
        else:
            return False, issues

    def save_screenshot(self, filename=None):
        """ذخیره تصویر صفحه"""
        try:
            if not self.driver:
                return False
                
            if not filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                
            screenshot_path = os.path.join("data", "screenshots", filename)
            
            # اطمینان از وجود پوشه
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            
            self.driver.save_screenshot(screenshot_path)
            return screenshot_path
            
        except Exception as e:
            print(f"خطا در ذخیره تصویر: {str(e)}")
            return False

    def get_page_source(self):
        """دریافت سورس کد صفحه"""
        try:
            if self.driver:
                return self.driver.page_source
            return None
        except Exception:
            return None

    def restart_driver(self):
        """راه‌اندازی مجدد درایور"""
        try:
            self.stop_robot()
            time.sleep(2)
            self.driver = self.get_driver()
            self.bot = FormBot(self.driver)
            return True
        except Exception as e:
            print(f"خطا در راه‌اندازی مجدد: {str(e)}")
            return False