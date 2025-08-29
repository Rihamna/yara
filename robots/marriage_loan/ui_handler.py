#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
رابط کاربری ربات وام ازدواج
این فایل مسئول UI مربوط به ربات وام ازدواج می‌باشد

نویسنده: سیستم خودکار YARA
تاریخ ایجاد: 2024
نسخه: 2.0 - در حال توسعه

وضعیت: این ربات در حال توسعه است و به زودی آماده خواهد شد
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MarriageLoanUIHandler:
    """کلاس مدیریت UI ربات وام ازدواج - در حال توسعه"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        
    def create_interface(self):
        """ایجاد رابط کاربری - صفحه به زودی"""
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)
        
        # فریم اصلی
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 20px;
                padding: 40px;
            }
        """)
        
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setAlignment(Qt.AlignCenter)
        frame_layout.setSpacing(25)
        
        # آیکن
        icon_label = QLabel("💍")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            font-size: 72px; 
            margin-bottom: 20px;
        """)
        
        # عنوان اصلی
        title_label = QLabel("ربات وام ازدواج")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: white; 
            font-size: 36px; 
            font-weight: bold;
            font-family: 'Tahoma', sans-serif;
            margin-bottom: 15px;
        """)
        
        # متن اصلی
        main_text = QLabel("به زودی در دسترس خواهد بود")
        main_text.setAlignment(Qt.AlignCenter)
        main_text.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9); 
            font-size: 22px;
            font-weight: 500;
            font-family: 'Tahoma', sans-serif;
            margin-bottom: 20px;
        """)
        
        # متن توضیحی
        description_text = QLabel("تیم توسعه YARA در حال کار بر روی این ربات می‌باشد\nلطفاً تا تکمیل این بخش صبر کنید")
        description_text.setAlignment(Qt.AlignCenter)
        description_text.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8); 
            font-size: 16px;
            font-family: 'Tahoma', sans-serif;
            line-height: 1.6;
            margin-bottom: 30px;
        """)
        
        # دکمه بازگشت
        back_button = QPushButton("بازگشت به صفحه اصلی")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                padding: 12px 30px;
                border-radius: 25px;
                font-weight: 500;
                font-size: 14px;
                font-family: 'Tahoma', sans-serif;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border-color: rgba(255, 255, 255, 0.5);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                transform: translateY(0px);
            }
        """)
        back_button.clicked.connect(lambda: self.main_window.switch_page("home"))
        
        # اضافه کردن عناصر به layout
        frame_layout.addWidget(icon_label)
        frame_layout.addWidget(title_label)
        frame_layout.addWidget(main_text)
        frame_layout.addWidget(description_text)
        frame_layout.addWidget(back_button)
        
        layout.addWidget(main_frame)
        
        # متدهای خالی برای سازگاری
        return main_widget
        
    def update_status(self, message):
        """بروزرسانی وضعیت - خالی"""
        pass
        
    def show_sms_panel(self):
        """نمایش پنل SMS - خالی"""
        pass
        
    def on_robot_completed(self, success):
        """تکمیل ربات - خالی"""
        pass#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
رابط کاربری ربات وام ازدواج
این فایل مسئول UI مربوط به ربات وام ازدواج می‌باشد

نویسنده: سیستم خودکار YARA
تاریخ ایجاد: 2024
نسخه: 2.0 - جداسازی UI و Backend

ویژگی‌های UI:
- فرم اطلاعات زوج
- مدیریت لیست متقاضیان
- کنترل ربات
- نمایش وضعیت
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from models.applicant import Applicant, ApplicantStatus
from data.database_manager import DatabaseManager


class MarriageLoanUIHandler:
    """کلاس مدیریت UI ربات وام ازدواج"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.data_service = main_window.data_service
        self.db_manager = DatabaseManager()
        
        # متغیرهای UI
        self.pending_applicants = []
        self.completed_applicants = []
        self.current_applicant = None
        
        # ویجت‌های فرم
        self.form_widgets = {}
        self.status_label = None
        self.sms_frame = None
        
    def create_interface(self):
        """ایجاد رابط کاربری کامل"""
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # بخش فرم (سمت چپ)
        form_section = self.create_form_section()
        main_layout.addWidget(form_section, 3)
        
        # بخش لیست‌ها (سمت راست)
        lists_section = self.create_lists_section()
        main_layout.addWidget(lists_section, 2)
        
        # بارگذاری داده‌های اولیه
        self.load_initial_data()
        
        return main_widget
        
    def create_form_section(self):
        """ایجاد بخش فرم"""
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(20)
        
        # عنوان
        title_label = QLabel("ربات وام ازدواج")
        title_label.setStyleSheet("""
            color: #2d3748; 
            font-size: 22px; 
            font-weight: bold;
            font-family: 'Tahoma', sans-serif;
            margin-bottom: 10px;
        """)
        form_layout.addWidget(title_label)
        
        # کنترل ربات
        robot_control = self.create_robot_control_section()
        form_layout.addWidget(robot_control)
        
        # فرم اطلاعات
        applicant_form = self.create_applicant_form()
        form_layout.addWidget(applicant_form)
        
        # دکمه‌های عملیات
        action_buttons = self.create_action_buttons()
        form_layout.addWidget(action_buttons)
        
        # پنل SMS (مخفی در ابتدا)
        self.sms_frame = self.create_sms_panel()
        form_layout.addWidget(self.sms_frame)
        
        return form_frame
        
    def create_robot_control_section(self):
        """ایجاد بخش کنترل ربات"""
        control_frame = QGroupBox("کنترل ربات")
        control_frame.setStyleSheet(self.get_groupbox_style())
        
        control_layout = QVBoxLayout(control_frame)
        
        # دکمه‌های کنترل
        buttons_layout = QHBoxLayout()
        
        self.start_robot_btn = QPushButton("▶️ شروع ربات")
        self.start_robot_btn.setStyleSheet(self.get_button_style("#10b981", "#059669"))
        self.start_robot_btn.clicked.connect(self.start_robot)
        
        self.stop_robot_btn = QPushButton("⏸️ توقف ربات")
        self.stop_robot_btn.setStyleSheet(self.get_button_style("#ef4444", "#dc2626"))
        self.stop_robot_btn.clicked.connect(self.stop_robot)
        self.stop_robot_btn.setEnabled(False)
        
        buttons_layout.addWidget(self.start_robot_btn)
        buttons_layout.addWidget(self.stop_robot_btn)
        
        # نمایشگر وضعیت
        self.status_label = QLabel("آماده برای شروع")
        self.status_label.setStyleSheet("""
            background-color: #f0fdf4;
            color: #166534;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #bbf7d0;
            font-family: 'Tahoma', sans-serif;
        """)
        
        control_layout.addLayout(buttons_layout)
        control_layout.addWidget(self.status_label)
        
        return control_frame
        
    def create_applicant_form(self):
        """ایجاد فرم اطلاعات متقاضی - مخصوص وام ازدواج"""
        form_frame = QGroupBox("اطلاعات متقاضی")
        form_frame.setStyleSheet(self.get_groupbox_style())
        
        # Scroll area برای فرم
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(400)  
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        scroll_widget = QWidget()
        form_layout = QGridLayout(scroll_widget)
        form_layout.setSpacing(8)
        
        row = 0
        
        # اطلاعات داماد
        form_layout.addWidget(QLabel("اطلاعات داماد"), row, 0, 1, 4)
        form_layout.itemAt(form_layout.count()-1).widget().setStyleSheet("font-weight: bold; color: #374151; margin: 10px 0px 5px 0px;")
        row += 1
        
        # نام داماد
        form_layout.addWidget(QLabel("نام:"), row, 0)
        self.form_widgets['groom_first_name'] = QLineEdit()
        form_layout.addWidget(self.form_widgets['groom_first_name'], row, 1)
        
        form_layout.addWidget(QLabel("نام خانوادگی:"), row, 2)
        self.form_widgets['groom_last_name'] = QLineEdit()
        form_layout.addWidget(self.form_widgets['groom_last_name'], row, 3)
        row += 1
        
        # کد ملی و موبایل داماد
        form_layout.addWidget(QLabel("کد ملی:"), row, 0)
        self.form_widgets['groom_national_id'] = QLineEdit()
        self.form_widgets['groom_national_id'].setMaxLength(10)
        form_layout.addWidget(self.form_widgets['groom_national_id'], row, 1)
        
        form_layout.addWidget(QLabel("موبایل:"), row, 2)
        self.form_widgets['groom_mobile'] = QLineEdit()
        self.form_widgets['groom_mobile'].setMaxLength(11)
        form_layout.addWidget(self.form_widgets['groom_mobile'], row, 3)
        row += 1
        
        # استان و شهر داماد
        form_layout.addWidget(QLabel("استان تولد:"), row, 0)
        self.form_widgets['groom_state'] = QComboBox()
        self.form_widgets['groom_state'].currentTextChanged.connect(self.on_groom_state_changed)
        form_layout.addWidget(self.form_widgets['groom_state'], row, 1)
        
        form_layout.addWidget(QLabel("شهر تولد:"), row, 2)
        self.form_widgets['groom_city'] = QComboBox()
        form_layout.addWidget(self.form_widgets['groom_city'], row, 3)
        row += 1
        
        # تاریخ تولد داماد
        form_layout.addWidget(QLabel("تاریخ تولد:"), row, 0)
        
        groom_date_frame = QFrame()
        groom_date_layout = QHBoxLayout(groom_date_frame)
        groom_date_layout.setContentsMargins(0, 0, 0, 0)
        
        self.form_widgets['groom_birth_day'] = QComboBox()
        self.form_widgets['groom_birth_month'] = QComboBox()
        self.form_widgets['groom_birth_year'] = QLineEdit()
        self.form_widgets['groom_birth_year'].setMaxLength(4)
        self.form_widgets['groom_birth_year'].setPlaceholderText("1370")
        
        groom_date_layout.addWidget(self.form_widgets['groom_birth_day'])
        groom_date_layout.addWidget(self.form_widgets['groom_birth_month'])
        groom_date_layout.addWidget(self.form_widgets['groom_birth_year'])
        
        form_layout.addWidget(groom_date_frame, row, 1, 1, 3)
        row += 1
        
        # جداکننده
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #e5e7eb; margin: 10px 0px;")
        form_layout.addWidget(separator, row, 0, 1, 4)
        row += 1
        
        # اطلاعات عروس
        form_layout.addWidget(QLabel("اطلاعات عروس"), row, 0, 1, 4)
        form_layout.itemAt(form_layout.count()-1).widget().setStyleSheet("font-weight: bold; color: #374151; margin: 10px 0px 5px 0px;")
        row += 1
        
        # نام عروس
        form_layout.addWidget(QLabel("نام:"), row, 0)
        self.form_widgets['bride_first_name'] = QLineEdit()
        form_layout.addWidget(self.form_widgets['bride_first_name'], row, 1)
        
        form_layout.addWidget(QLabel("نام خانوادگی:"), row, 2)
        self.form_widgets['bride_last_name'] = QLineEdit()
        form_layout.addWidget(self.form_widgets['bride_last_name'], row, 3)
        row += 1
        
        # کد ملی عروس
        form_layout.addWidget(QLabel("کد ملی:"), row, 0)
        self.form_widgets['bride_national_id'] = QLineEdit()
        self.form_widgets['bride_national_id'].setMaxLength(10)
        form_layout.addWidget(self.form_widgets['bride_national_id'], row, 1)
        
        # تاریخ ازدواج
        form_layout.addWidget(QLabel("تاریخ ازدواج:"), row, 2)
        self.form_widgets['marriage_date'] = QLineEdit()
        self.form_widgets['marriage_date'].setPlaceholderText("1402/01/01")
        form_layout.addWidget(self.form_widgets['marriage_date'], row, 3)
        row += 1
        
        # استان و شهر عروس
        form_layout.addWidget(QLabel("استان تولد:"), row, 0)
        self.form_widgets['bride_state'] = QComboBox()
        self.form_widgets['bride_state'].currentTextChanged.connect(self.on_bride_state_changed)
        form_layout.addWidget(self.form_widgets['bride_state'], row, 1)
        
        form_layout.addWidget(QLabel("شهر تولد:"), row, 2)
        self.form_widgets['bride_city'] = QComboBox()
        form_layout.addWidget(self.form_widgets['bride_city'], row, 3)
        row += 1
        
        # تاریخ تولد عروس
        form_layout.addWidget(QLabel("تاریخ تولد:"), row, 0)
        
        bride_date_frame = QFrame()
        bride_date_layout = QHBoxLayout(bride_date_frame)
        bride_date_layout.setContentsMargins(0, 0, 0, 0)
        
        self.form_widgets['bride_birth_day'] = QComboBox()
        self.form_widgets['bride_birth_month'] = QComboBox()
        self.form_widgets['bride_birth_year'] = QLineEdit()
        self.form_widgets['bride_birth_year'].setMaxLength(4)
        self.form_widgets['bride_birth_year'].setPlaceholderText("1375")
        
        bride_date_layout.addWidget(self.form_widgets['bride_birth_day'])
        bride_date_layout.addWidget(self.form_widgets['bride_birth_month'])
        bride_date_layout.addWidget(self.form_widgets['bride_birth_year'])
        
        form_layout.addWidget(bride_date_frame, row, 1, 1, 3)
        row += 1
        
        # جداکننده
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setStyleSheet("color: #e5e7eb; margin: 10px 0px;")
        form_layout.addWidget(separator2, row, 0, 1, 4)
        row += 1
        
        # اطلاعات بانکی
        form_layout.addWidget(QLabel("اطلاعات بانکی"), row, 0, 1, 4)
        form_layout.itemAt(form_layout.count()-1).widget().setStyleSheet("font-weight: bold; color: #374151; margin: 10px 0px 5px 0px;")
        row += 1
        
        # بانک و شعبه
        form_layout.addWidget(QLabel("بانک:"), row, 0)
        self.form_widgets['bank_name'] = QComboBox()
        form_layout.addWidget(self.form_widgets['bank_name'], row, 1)
        
        form_layout.addWidget(QLabel("شعبه:"), row, 2)
        self.form_widgets['branch_name'] = QLineEdit()
        form_layout.addWidget(self.form_widgets['branch_name'], row, 3)
        row += 1
        
        # آدرس
        form_layout.addWidget(QLabel("آدرس:"), row, 0)
        self.form_widgets['address'] = QLineEdit()
        form_layout.addWidget(self.form_widgets['address'], row, 1, 1, 3)
        row += 1
        
        # کد پستی
        form_layout.addWidget(QLabel("کد پستی:"), row, 0)
        self.form_widgets['postal_code'] = QLineEdit()
        self.form_widgets['postal_code'].setMaxLength(10)
        form_layout.addWidget(self.form_widgets['postal_code'], row, 1)
        
        # اعمال استایل به تمام ویجت‌های فرم
        for widget in self.form_widgets.values():
            if isinstance(widget, QLineEdit):
                widget.setStyleSheet(self.get_input_style())
            elif isinstance(widget, QComboBox):
                widget.setStyleSheet(self.get_combo_style())
        
        scroll_area.setWidget(scroll_widget)
        
        form_frame_layout = QVBoxLayout(form_frame)
        form_frame_layout.addWidget(scroll_area)
        
        return form_frame
        
    def create_action_buttons(self):
        """ایجاد دکمه‌های عملیات"""
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        
        self.save_btn = QPushButton("💾 ذخیره")
        self.save_btn.setStyleSheet(self.get_button_style("#3b82f6", "#2563eb"))
        self.save_btn.clicked.connect(self.save_applicant)
        
        self.clear_btn = QPushButton("🔄 پاک کردن")
        self.clear_btn.setStyleSheet(self.get_button_style("#6b7280", "#4b5563"))
        self.clear_btn.clicked.connect(self.clear_form)
        
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.clear_btn)
        
        return buttons_frame
        
    def create_sms_panel(self):
        """ایجاد پنل SMS"""
        sms_frame = QGroupBox("کد تأیید SMS")
        sms_frame.setStyleSheet(self.get_groupbox_style())
        sms_frame.hide()
        
        sms_layout = QVBoxLayout(sms_frame)
        
        info_label = QLabel("لطفاً کد 6 رقمی ارسال شده به موبایل را وارد کنید:")
        info_label.setStyleSheet("color: #374151; font-size: 13px; margin-bottom: 10px;")
        
        sms_input_layout = QHBoxLayout()
        
        self.sms_code_input = QLineEdit()
        self.sms_code_input.setMaxLength(6)
        self.sms_code_input.setPlaceholderText("کد 6 رقمی")
        self.sms_code_input.setStyleSheet(self.get_input_style())
        
        self.submit_sms_btn = QPushButton("✅ ارسال کد")
        self.submit_sms_btn.setStyleSheet(self.get_button_style("#10b981", "#059669"))
        self.submit_sms_btn.clicked.connect(self.submit_sms_code)
        
        sms_input_layout.addWidget(self.sms_code_input)
        sms_input_layout.addWidget(self.submit_sms_btn)
        
        sms_layout.addWidget(info_label)
        sms_layout.addLayout(sms_input_layout)
        
        return sms_frame
        
    def create_lists_section(self):
        """ایجاد بخش لیست‌ها"""
        lists_frame = QFrame()
        lists_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        lists_layout = QVBoxLayout(lists_frame)
        lists_layout.setContentsMargins(20, 20, 20, 20)
        lists_layout.setSpacing(15)
        
        # عنوان
        title_label = QLabel("مدیریت متقاضیان")
        title_label.setStyleSheet("""
            color: #2d3748; 
            font-size: 18px; 
            font-weight: bold;
            font-family: 'Tahoma', sans-serif;
            margin-bottom: 10px;
        """)
        lists_layout.addWidget(title_label)
        
        # لیست در انتظار
        pending_frame = QGroupBox("در انتظار")
        pending_frame.setStyleSheet(self.get_groupbox_style())
        
        pending_layout = QVBoxLayout(pending_frame)
        
        self.pending_count_label = QLabel("0 متقاضی")
        self.pending_count_label.setStyleSheet("color: #6b7280; font-size: 12px; font-weight: bold;")
        
        self.pending_list = QListWidget()
        self.pending_list.setStyleSheet(self.get_list_style())
        self.pending_list.itemClicked.connect(self.on_pending_item_clicked)
        self.pending_list.setMaximumHeight(150)
        
        pending_layout.addWidget(self.pending_count_label)
        pending_layout.addWidget(self.pending_list)
        
        # لیست تکمیل شده
        completed_frame = QGroupBox("تکمیل شده")
        completed_frame.setStyleSheet(self.get_groupbox_style())
        
        completed_layout = QVBoxLayout(completed_frame)
        
        self.completed_count_label = QLabel("0 متقاضی")
        self.completed_count_label.setStyleSheet("color: #6b7280; font-size: 12px; font-weight: bold;")
        
        self.completed_list = QListWidget()
        self.completed_list.setStyleSheet(self.get_list_style())
        self.completed_list.setMaximumHeight(150)
        
        completed_layout.addWidget(self.completed_count_label)
        completed_layout.addWidget(self.completed_list)
        
        lists_layout.addWidget(pending_frame)
        lists_layout.addWidget(completed_frame)
        
        return lists_frame
        
    def load_initial_data(self):
        """بارگذاری داده‌های اولیه"""
        try:
            # بارگذاری کمبوبکس‌ها
            self.load_combo_data()
            
            # بارگذاری متقاضیان
            self.load_applicants()
            
        except Exception as e:
            self.main_window.show_error(f"خطا در بارگذاری داده‌ها: {str(e)}")
            
    def load_combo_data(self):
        """بارگذاری داده‌های کمبوبکس‌ها"""
        try:
            # استان‌ها از دیتابیس
            states = self.db_manager.get_states()
            
            self.form_widgets['groom_state'].addItems(states)
            self.form_widgets['bride_state'].addItems(states)
            
            # روزها
            days = [str(i) for i in range(1, 32)]
            self.form_widgets['groom_birth_day'].addItems(days)
            self.form_widgets['bride_birth_day'].addItems(days)
            
            # ماه‌های شمسی
            months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                     "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
            
            self.form_widgets['groom_birth_month'].addItems(months)
            self.form_widgets['bride_birth_month'].addItems(months)
            
            # بانک‌های ایران از دیتابیس
            banks = self.db_manager.get_banks()
            self.form_widgets['bank_name'].addItems(banks)
            
        except Exception as e:
            # در صورت عدم دسترسی به دیتابیس، از داده‌های پیش‌فرض استفاده کن
            self.load_default_combo_data()
            
    def load_default_combo_data(self):
        """بارگذاری داده‌های پیش‌فرض کمبوبکس‌ها"""
        states = ["تهران", "اصفهان", "خوزستان", "فارس", "خراسان رضوی", "آذربایجان شرقی", 
                 "مازندران", "کرمان", "سیستان و بلوچستان", "گیلان"]
        
        self.form_widgets['groom_state'].addItems(states)
        self.form_widgets['bride_state'].addItems(states)
        
        days = [str(i) for i in range(1, 32)]
        self.form_widgets['groom_birth_day'].addItems(days)
        self.form_widgets['bride_birth_day'].addItems(days)
        
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                 "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        
        self.form_widgets['groom_birth_month'].addItems(months)
        self.form_widgets['bride_birth_month'].addItems(months)
        
        banks = ["بانک ملی ایران", "بانک صادرات ایران", "بانک تجارت", "بانک ملت", 
                "بانک پاسارگاد", "بانک پارسیان", "بانک سامان", "بانک کشاورزی"]
        self.form_widgets['bank_name'].addItems(banks)
        
    def on_groom_state_changed(self, state):
        """تغییر استان داماد"""
        try:
            cities = self.db_manager.get_cities_by_state(state)
            if not cities:
                cities = self.get_default_cities(state)
                
            self.form_widgets['groom_city'].clear()
            self.form_widgets['groom_city'].addItems(cities)
        except Exception:
            self.form_widgets['groom_city'].clear()
            self.form_widgets['groom_city'].addItems(self.get_default_cities(state))
            
    def on_bride_state_changed(self, state):
        """تغییر استان عروس"""
        try:
            cities = self.db_manager.get_cities_by_state(state)
            if not cities:
                cities = self.get_default_cities(state)
                
            self.form_widgets['bride_city'].clear()
            self.form_widgets['bride_city'].addItems(cities)
        except Exception:
            self.form_widgets['bride_city'].clear()
            self.form_widgets['bride_city'].addItems(self.get_default_cities(state))
            
    def get_default_cities(self, state):
        """شهرهای پیش‌فرض برای استان"""
        cities_map = {
            "تهران": ["تهران", "شهریار", "ورامین", "رباط کریم"],
            "اصفهان": ["اصفهان", "کاشان", "نجف آباد", "خمینی شهر"],
            "خوزستان": ["اهواز", "آبادان", "خرمشهر", "دزفول"],
            "فارس": ["شیراز", "مرودشت", "کازرون", "جهرم"],
            "خراسان رضوی": ["مشهد", "نیشابور", "سبزوار", "قوچان"]
        }
        
        return cities_map.get(state, [state])
        
    def load_applicants(self):
        """بارگذاری متقاضیان"""
        try:
            # برای ربات وام ازدواج، متقاضیان جداگانه‌ای داریم
            applicants = self.data_service.load_applicants()
            
            # فیلتر متقاضیان مربوط به وام ازدواج
            marriage_applicants = [a for a in applicants if hasattr(a, 'loan_type') and a.loan_type == 'marriage']
            
            self.pending_applicants = [a for a in marriage_applicants if a.status == ApplicantStatus.PENDING]
            self.completed_applicants = [a for a in marriage_applicants if a.status == ApplicantStatus.COMPLETED]
            
            self.update_lists()
            
        except Exception as e:
            print(f"خطا در بارگذاری متقاضیان: {str(e)}")
            
    def update_lists(self):
        """بروزرسانی لیست‌ها"""
        # لیست در انتظار
        self.pending_list.clear()
        for applicant in self.pending_applicants:
            item_text = f"{applicant.father_first_name} {applicant.father_last_name}"
            if applicant.bank_name:
                item_text += f" - {applicant.bank_name}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, applicant)
            self.pending_list.addItem(item)
            
        # لیست تکمیل شده
        self.completed_list.clear()
        for applicant in self.completed_applicants:
            item