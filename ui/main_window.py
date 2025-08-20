#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLabel, QPushButton, QLineEdit, 
                             QComboBox, QListWidget, QListWidgetItem, QFrame,
                             QScrollArea, QMessageBox, QSplitter, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
from models.applicant import Applicant, ApplicantStatus
from services.data_service import DataService
from services.robot_service import RobotService
import asyncio

class RobotThread(QThread):
    status_update = pyqtSignal(str)
    sms_required = pyqtSignal()
    completed = pyqtSignal(bool)
    
    def __init__(self, applicant_data):
        super().__init__()
        self.applicant_data = applicant_data
        self.robot_service = RobotService()
        self.sms_code = None
        
    def run(self):
        try:
            # شروع ربات
            result = self.robot_service.run_registration(self.applicant_data, self.status_update.emit)
            
            if result == "waiting_for_sms":
                self.sms_required.emit()
                
                # انتظار برای کد SMS
                while self.sms_code is None:
                    self.msleep(100)
                
                # ارسال کد SMS
                sms_result = self.robot_service.submit_sms_code(self.sms_code, self.status_update.emit)
                self.completed.emit(sms_result == "completed")
            else:
                self.completed.emit(False)
                
        except Exception as e:
            self.status_update.emit(f"خطا: {str(e)}")
            self.completed.emit(False)
    
    def submit_sms_code(self, code):
        self.sms_code = code

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_service = DataService()
        self.pending_applicants = []
        self.completed_applicants = []
        self.current_applicant = None
        self.robot_thread = None
        
        self.init_ui()
        self.load_data()
        self.setup_styles()
        
    def init_ui(self):
        """ایجاد رابط کاربری"""
        self.setWindowTitle("🤖 سیستم مدیریت ربات وام فرزندآوری")
        self.setGeometry(100, 100, 1200, 800)
        
        # ویجت اصلی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout اصلی
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        self.create_header(main_layout)
        
        # محتوای اصلی
        content_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter)
        
        # فرم سمت چپ
        self.create_form_panel(content_splitter)
        
        # لیست‌ها سمت راست
        self.create_lists_panel(content_splitter)
        
        # وضعیت پایین
        self.create_status_bar(main_layout)
        
    def create_header(self, parent_layout):
        """ایجاد هدر"""
        header_frame = QFrame()
        header_frame.setFixedHeight(100)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                margin: 10px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # عنوان اصلی
        title_layout = QVBoxLayout()
        
        title_label = QLabel("🤖 ربات وام فرزندآوری")
        title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("سیستم خودکار ثبت‌نام وام فرزندآوری بانک مرکزی")
        subtitle_label.setStyleSheet("color: white; font-size: 14px; opacity: 0.9;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        # وضعیت ربات
        status_layout = QVBoxLayout()
        status_layout.addWidget(QLabel("وضعیت ربات:", styleSheet="color: white; font-weight: bold;"))
        self.robot_status_label = QLabel("⚫ غیرفعال")
        self.robot_status_label.setStyleSheet("color: white; font-size: 14px;")
        status_layout.addWidget(self.robot_status_label)
        
        header_layout.addLayout(status_layout)
        header_layout.addStretch()
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        parent_layout.addWidget(header_frame)
        
    def create_form_panel(self, parent_splitter):
        """ایجاد پنل فرم"""
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }
        """)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(form_frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        form_layout = QVBoxLayout(form_frame)
        
        # عنوان فرم
        form_title = QLabel("📝 ثبت‌نام جدید")
        form_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; margin-bottom: 20px;")
        form_layout.addWidget(form_title)
        
        # اطلاعات پدر
        self.create_father_section(form_layout)
        
        # اطلاعات فرزند
        self.create_child_section(form_layout)
        
        # دکمه‌ها
        self.create_buttons(form_layout)
        
        # پنل SMS
        self.create_sms_panel(form_layout)
        
        parent_splitter.addWidget(scroll_area)
        
    def create_father_section(self, parent_layout):
        """بخش اطلاعات پدر"""
        father_label = QLabel("👨 اطلاعات پدر")
        father_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #667eea; margin: 20px 0 10px 0;")
        parent_layout.addWidget(father_label)
        
        # استان پدر
        parent_layout.addWidget(QLabel("استان محل تولد پدر:"))
        self.father_state_combo = QComboBox()
        self.father_state_combo.currentTextChanged.connect(self.on_father_state_changed)
        parent_layout.addWidget(self.father_state_combo)
        
        # شهر پدر
        parent_layout.addWidget(QLabel("شهر محل تولد پدر:"))
        self.father_city_combo = QComboBox()
        parent_layout.addWidget(self.father_city_combo)
        
        # شماره ملی پدر
        parent_layout.addWidget(QLabel("شماره ملی پدر:"))
        self.father_national_id = QLineEdit()
        self.father_national_id.setMaxLength(10)
        parent_layout.addWidget(self.father_national_id)
        
        # تاریخ تولد پدر
        parent_layout.addWidget(QLabel("تاریخ تولد پدر:"))
        father_date_layout = QHBoxLayout()
        
        self.father_birth_day = QComboBox()
        self.father_birth_month = QComboBox()
        self.father_birth_year = QLineEdit()
        self.father_birth_year.setMaxLength(4)
        
        father_date_layout.addWidget(self.father_birth_day)
        father_date_layout.addWidget(self.father_birth_month)
        father_date_layout.addWidget(self.father_birth_year)
        
        parent_layout.addLayout(father_date_layout)
        
        # موبایل پدر
        parent_layout.addWidget(QLabel("شماره موبایل پدر:"))
        self.father_mobile = QLineEdit()
        self.father_mobile.setMaxLength(11)
        parent_layout.addWidget(self.father_mobile)
        
    def create_child_section(self, parent_layout):
        """بخش اطلاعات فرزند"""
        child_label = QLabel("👶 اطلاعات فرزند")
        child_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #667eea; margin: 20px 0 10px 0;")
        parent_layout.addWidget(child_label)
        
        # کد ملی فرزند
        parent_layout.addWidget(QLabel("کد ملی فرزند:"))
        self.child_national_id = QLineEdit()
        self.child_national_id.setMaxLength(10)
        parent_layout.addWidget(self.child_national_id)
        
        # تاریخ تولد فرزند
        parent_layout.addWidget(QLabel("تاریخ تولد فرزند:"))
        child_date_layout = QHBoxLayout()
        
        self.child_birth_day = QComboBox()
        self.child_birth_month = QComboBox()
        self.child_birth_year = QLineEdit()
        self.child_birth_year.setMaxLength(4)
        
        child_date_layout.addWidget(self.child_birth_day)
        child_date_layout.addWidget(self.child_birth_month)
        child_date_layout.addWidget(self.child_birth_year)
        
        parent_layout.addLayout(child_date_layout)
        
        # استان فرزند
        parent_layout.addWidget(QLabel("استان محل تولد فرزند:"))
        self.child_state_combo = QComboBox()
        self.child_state_combo.currentTextChanged.connect(self.on_child_state_changed)
        parent_layout.addWidget(self.child_state_combo)
        
        # شهر فرزند
        parent_layout.addWidget(QLabel("شهر محل تولد فرزند:"))
        self.child_city_combo = QComboBox()
        parent_layout.addWidget(self.child_city_combo)
        
        # تعداد فرزند
        parent_layout.addWidget(QLabel("تعداد فرزند:"))
        self.child_number_combo = QComboBox()
        parent_layout.addWidget(self.child_number_combo)
        
    def create_buttons(self, parent_layout):
        """ایجاد دکمه‌ها"""
        buttons_layout = QHBoxLayout()
        
        self.save_button = QPushButton("💾 ذخیره")
        self.save_button.clicked.connect(self.save_applicant)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #48bb78;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
        """)
        
        self.start_robot_button = QPushButton("🚀 شروع ربات")
        self.start_robot_button.clicked.connect(self.start_robot)
        self.start_robot_button.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a67d8;
            }
        """)
        
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.start_robot_button)
        
        parent_layout.addLayout(buttons_layout)
        
    def create_sms_panel(self, parent_layout):
        """پنل کد SMS"""
        self.sms_frame = QFrame()
        self.sms_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                margin-top: 20px;
            }
        """)
        self.sms_frame.hide()
        
        sms_layout = QVBoxLayout(self.sms_frame)
        
        sms_label = QLabel("📱 کد تأیید SMS")
        sms_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        sms_layout.addWidget(sms_label)
        
        self.sms_code_input = QLineEdit()
        self.sms_code_input.setMaxLength(6)
        self.sms_code_input.setPlaceholderText("کد 6 رقمی را وارد کنید")
        sms_layout.addWidget(self.sms_code_input)
        
        self.submit_sms_button = QPushButton("✅ تأیید کد")
        self.submit_sms_button.clicked.connect(self.submit_sms_code)
        self.submit_sms_button.setStyleSheet("""
            QPushButton {
                background-color: #48bb78;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
        """)
        sms_layout.addWidget(self.submit_sms_button)
        
        parent_layout.addWidget(self.sms_frame)
        
    def create_lists_panel(self, parent_splitter):
        """ایجاد پنل لیست‌ها"""
        lists_widget = QWidget()
        lists_layout = QVBoxLayout(lists_widget)
        
        # لیست در انتظار
        pending_frame = QFrame()
        pending_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }
        """)
        
        pending_layout = QVBoxLayout(pending_frame)
        
        self.pending_count_label = QLabel("⏳ در انتظار (0)")
        self.pending_count_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ed8936; margin-bottom: 15px;")
        pending_layout.addWidget(self.pending_count_label)
        
        self.pending_list = QListWidget()
        self.pending_list.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
            }
            QListWidget::item {
                background: #fff5f5;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }
            QListWidget::item:hover {
                background: #fed7d7;
            }
        """)
        pending_layout.addWidget(self.pending_list)
        
        # لیست تکمیل شده
        completed_frame = QFrame()
        completed_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }
        """)
        
        completed_layout = QVBoxLayout(completed_frame)
        
        self.completed_count_label = QLabel("✅ تکمیل شده (0)")
        self.completed_count_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #48bb78; margin-bottom: 15px;")
        completed_layout.addWidget(self.completed_count_label)
        
        self.completed_list = QListWidget()
        self.completed_list.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
            }
            QListWidget::item {
                background: #f0fff4;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
            }
            QListWidget::item:hover {
                background: #c6f6d5;
            }
        """)
        completed_layout.addWidget(self.completed_list)
        
        lists_layout.addWidget(pending_frame)
        lists_layout.addWidget(completed_frame)
        
        parent_splitter.addWidget(lists_widget)
        
    def create_status_bar(self, parent_layout):
        """نوار وضعیت"""
        status_frame = QFrame()
        status_frame.setFixedHeight(40)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #2d3748;
                margin: 0;
            }
        """)
        
        status_layout = QHBoxLayout(status_frame)
        
        self.status_text = QLabel("آماده")
        self.status_text.setStyleSheet("color: white;")
        
        self.last_update_text = QLabel("آخرین بروزرسانی: -")
        self.last_update_text.setStyleSheet("color: #a0aec0;")
        
        status_layout.addWidget(self.status_text)
        status_layout.addStretch()
        status_layout.addWidget(self.last_update_text)
        
        parent_layout.addWidget(status_frame)
        
    def setup_styles(self):
        """تنظیم استایل‌ها"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLineEdit, QComboBox {
                padding: 10px;
                margin: 5px;
                font-size: 14px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #667eea;
            }
            QLabel {
                margin: 5px 0;
                color: #333;
            }
        """)
        
    def load_combo_data(self):
        """بارگذاری داده‌های کمبوباکس"""
        # استان‌ها
        states = ["تهران", "اصفهان", "خوزستان", "فارس", "خراسان رضوی", 
                 "البرز", "آذربایجان شرقی", "کرمان", "مازندران", "گیلان"]
        
        self.father_state_combo.addItems(states)
        self.child_state_combo.addItems(states)
        
        # روزها
        days = [str(i) for i in range(1, 32)]
        self.father_birth_day.addItems(days)
        self.child_birth_day.addItems(days)
        
        # ماه‌ها
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                 "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        
        self.father_birth_month.addItems(months)
        self.child_birth_month.addItems(months)
        
        # تعداد فرزند
        child_numbers = ["اول", "دوم", "سوم", "چهارم", "پنجم"]
        self.child_number_combo.addItems(child_numbers)
        
    def on_father_state_changed(self, state):
        """تغییر استان پدر"""
        self.load_cities_for_state(state, self.father_city_combo)
        
    def on_child_state_changed(self, state):
        """تغییر استان فرزند"""
        self.load_cities_for_state(state, self.child_city_combo)
        
    def load_cities_for_state(self, state, city_combo):
        """بارگذاری شهرها براساس استان"""
        city_combo.clear()
        
        cities = {
            "تهران": ["تهران", "شهریار", "ورامین", "دماوند", "پاکدشت"],
            "اصفهان": ["اصفهان", "کاشان", "نجف‌آباد", "خمینی‌شهر", "لنجان"],
            "خوزستان": ["اهواز", "آبادان", "خرمشهر", "دزفول", "مسجدسلیمان"]
        }
        
        city_list = cities.get(state, [state])
        city_combo.addItems(city_list)
        
    def load_data(self):
        """بارگذاری داده‌ها"""
        self.load_combo_data()
        self.load_applicants()
        
    def load_applicants(self):
        """بارگذاری متقاضیان"""
        try:
            applicants = self.data_service.load_applicants()
            
            self.pending_applicants = [a for a in applicants if a.status == ApplicantStatus.PENDING]
            self.completed_applicants = [a for a in applicants if a.status == ApplicantStatus.COMPLETED]
            
            self.update_lists()
            
        except Exception as e:
            self.update_status(f"خطا در بارگذاری: {str(e)}")
            
    def update_lists(self):
        """بروزرسانی لیست‌ها"""
        # لیست انتظار
        self.pending_list.clear()
        for applicant in self.pending_applicants:
            item = QListWidgetItem(applicant.display_name)
            item.setData(Qt.UserRole, applicant)
            self.pending_list.addItem(item)
            
        # لیست تکمیل شده
        self.completed_list.clear()
        for applicant in self.completed_applicants:
            item = QListWidgetItem(f"{applicant.display_name}\n{applicant.completion_time}")
            item.setData(Qt.UserRole, applicant)
            self.completed_list.addItem(item)
            
        # بروزرسانی تعداد
        self.pending_count_label.setText(f"⏳ در انتظار ({len(self.pending_applicants)})")
        self.completed_count_label.setText(f"✅ تکمیل شده ({len(self.completed_applicants)})")
        
    def validate_form(self):
        """اعتبارسنجی فرم"""
        if not self.father_national_id.text() or len(self.father_national_id.text()) != 10:
            QMessageBox.warning(self, "خطا", "شماره ملی پدر باید 10 رقم باشد.")
            return False
            
        if not self.child_national_id.text() or len(self.child_national_id.text()) != 10:
            QMessageBox.warning(self, "خطا", "کد ملی فرزند باید 10 رقم باشد.")
            return False
            
        if not self.father_mobile.text() or len(self.father_mobile.text()) != 11:
            QMessageBox.warning(self, "خطا", "شماره موبایل پدر باید 11 رقم باشد.")
            return False
            
        return True
        
    def create_applicant_from_form(self):
        """ایجاد متقاضی از فرم"""
        return Applicant(
            father_national_id=self.father_national_id.text().strip(),
            father_birth_state=self.father_state_combo.currentText(),
            father_birth_city=self.father_city_combo.currentText(),
            father_birth_day=self.father_birth_day.currentText(),
            father_birth_month=self.father_birth_month.currentText(),
            father_birth_year=self.father_birth_year.text().strip(),
            father_mobile=self.father_mobile.text().strip(),
            child_national_id=self.child_national_id.text().strip(),
            child_birth_state=self.child_state_combo.currentText(),
            child_birth_city=self.child_city_combo.currentText(),
            child_birth_day=self.child_birth_day.currentText(),
            child_birth_month=self.child_birth_month.currentText(),
            child_birth_year=self.child_birth_year.text().strip(),
            child_number=self.child_number_combo.currentText()
        )
        
    def clear_form(self):
        """پاک کردن فرم"""
        self.father_national_id.clear()
        self.father_state_combo.setCurrentIndex(0)
        self.father_city_combo.setCurrentIndex(0)
        self.father_birth_day.setCurrentIndex(0)
        self.father_birth_month.setCurrentIndex(0)
        self.father_birth_year.clear()
        self.father_mobile.clear()
        
        self.child_national_id.clear()
        self.child_state_combo.setCurrentIndex(0)
        self.child_city_combo.setCurrentIndex(0)
        self.child_birth_day.setCurrentIndex(0)
        self.child_birth_month.setCurrentIndex(0)
        self.child_birth_year.clear()
        self.child_number_combo.setCurrentIndex(0)
        
    def save_applicant(self):
        """ذخیره متقاضی"""
        try:
            if not self.validate_form():
                return
                
            applicant = self.create_applicant_from_form()
            self.data_service.save_applicant(applicant)
            
            self.pending_applicants.append(applicant)
            self.update_lists()
            self.clear_form()
            
            self.update_status("متقاضی جدید با موفقیت ذخیره شد")
            QMessageBox.information(self, "موفقیت", "اطلاعات با موفقیت ذخیره شد!")
            
        except Exception as e:
            self.update_status(f"خطا در ذخیره: {str(e)}")
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره اطلاعات:\n{str(e)}")
            
    def start_robot(self):
        """شروع ربات"""
        try:
            if not self.pending_applicants:
                QMessageBox.warning(self, "هشدار", "لیست انتظار خالی است. ابتدا متقاضی اضافه کنید.")
                return
                
            self.current_applicant = self.pending_applicants[0]
            
            # غیرفعال کردن دکمه
            self.start_robot_button.setEnabled(False)
            self.start_robot_button.setText("⏳ در حال اجرا...")
            
            # بروزرسانی وضعیت
            self.update_robot_status("🔄 فعال", "در حال اجرای ربات...")
            
            # شروع thread ربات
            self.robot_thread = RobotThread(self.current_applicant.to_robot_data())
            self.robot_thread.status_update.connect(self.update_status)
            self.robot_thread.sms_required.connect(self.show_sms_panel)
            self.robot_thread.completed.connect(self.on_robot_completed)
            self.robot_thread.start()
            
        except Exception as e:
            self.reset_robot_ui()
            self.update_status(f"خطا: {str(e)}")
            QMessageBox.critical(self, "خطا", f"خطا در اجرای ربات:\n{str(e)}")
            
    def show_sms_panel(self):
        """نمایش پنل کد SMS"""
        self.sms_frame.show()
        self.update_status("⏳ در انتظار کد تأیید SMS...")
        
    def submit_sms_code(self):
        """ارسال کد SMS"""
        try:
            if not self.sms_code_input.text():
                QMessageBox.warning(self, "هشدار", "کد تأیید را وارد کنید.")
                return
                
            if self.robot_thread:
                self.submit_sms_button.setEnabled(False)
                self.submit_sms_button.setText("⏳ در حال ارسال...")
                self.robot_thread.submit_sms_code(self.sms_code_input.text())
                
        except Exception as e:
            self.update_status(f"خطا: {str(e)}")
            QMessageBox.critical(self, "خطا", f"خطا در ارسال کد:\n{str(e)}")
            
    def on_robot_completed(self, success):
        """اتمام کار ربات"""
        try:
            if success and self.current_applicant:
                # انتقال به لیست تکمیل شده
                self.current_applicant.status = ApplicantStatus.COMPLETED
                self.current_applicant.completion_time = self.data_service.get_current_time()
                
                self.pending_applicants.remove(self.current_applicant)
                self.completed_applicants.append(self.current_applicant)
                
                self.data_service.update_applicant_status(self.current_applicant.id, ApplicantStatus.COMPLETED)
                self.update_lists()
                
                # پنهان کردن پنل SMS
                self.sms_frame.hide()
                self.sms_code_input.clear()
                
                if self.pending_applicants:
                    QMessageBox.information(self, "موفقیت", 
                                          "ثبت‌نام با موفقیت تکمیل شد!\n\nربات آماده اجرای متقاضی بعدی است.")
                else:
                    QMessageBox.information(self, "تمام", 
                                          "ثبت‌نام با موفقیت تکمیل شد!\n\nتمام متقاضیان پردازش شدند.")
            else:
                QMessageBox.critical(self, "خطا", "ثبت‌نام ناموفق بود!")
                
            self.reset_robot_ui()
            self.current_applicant = None
            
        except Exception as e:
            self.update_status(f"خطا: {str(e)}")
            
    def reset_robot_ui(self):
        """بازنشانی UI ربات"""
        self.start_robot_button.setEnabled(True)
        self.start_robot_button.setText("🚀 شروع ربات")
        self.submit_sms_button.setEnabled(True)
        self.submit_sms_button.setText("✅ تأیید کد")
        self.update_robot_status("⚫ غیرفعال", "آماده")
        
    def update_robot_status(self, status, message):
        """بروزرسانی وضعیت ربات"""
        self.robot_status_label.setText(status)
        self.update_status(message)
        
    def update_status(self, message):
        """بروزرسانی نوار وضعیت"""
        self.status_text.setText(message)
        from datetime import datetime
        self.last_update_text.setText(f"آخرین بروزرسانی: {datetime.now().strftime('%H:%M:%S')}")
        
    def closeEvent(self, event):
        """بستن برنامه"""
        if self.robot_thread and self.robot_thread.isRunning():
            self.robot_thread.terminate()
            self.robot_thread.wait()
        event.accept()