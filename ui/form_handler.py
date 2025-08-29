#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QGroupBox, QScrollArea, QGridLayout, QLineEdit,
                            QComboBox, QSpinBox, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt
from models.applicant import Applicant

class FormHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        
    def create_applicant_form(self, parent_layout):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #334155;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #64748B;
                border-radius: 6px;
                margin: 2px;
            }
        """)
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # اطلاعات پدر
        self.create_father_info_section(form_layout)
        
        # اطلاعات فرزند
        self.create_child_info_section(form_layout)
        
        # اطلاعات بانک
        self.create_bank_info_section(form_layout)
        
        # اعمال استایل به تمام فیلدها
        self.apply_input_styles()
        
        scroll.setWidget(form_widget)
        parent_layout.addWidget(scroll)
        
    def create_father_info_section(self, parent_layout):
        father_group = QGroupBox("اطلاعات پدر")
        father_group.setStyleSheet(self.main_window.get_groupbox_style())
        father_layout = QGridLayout(father_group)
        
        self.main_window.father_first_name = QLineEdit()
        self.main_window.father_last_name = QLineEdit()
        self.main_window.father_national_id = QLineEdit()
        self.main_window.father_mobile = QLineEdit()
        
        self.main_window.father_birth_state = QComboBox()
        self.main_window.father_birth_city = QComboBox()
        self.main_window.father_birth_day = QComboBox()
        self.main_window.father_birth_month = QComboBox()
        self.main_window.father_birth_year = QLineEdit()
        
        # تنظیم placeholder و محدودیت‌ها
        self.main_window.father_first_name.setPlaceholderText("نام پدر")
        self.main_window.father_last_name.setPlaceholderText("نام خانوادگی پدر")
        self.main_window.father_national_id.setPlaceholderText("کد ملی 10 رقمی")
        self.main_window.father_national_id.setMaxLength(10)
        self.main_window.father_mobile.setPlaceholderText("09xxxxxxxxx")
        self.main_window.father_mobile.setMaxLength(11)
        self.main_window.father_birth_year.setPlaceholderText("سال تولد (شمسی)")
        self.main_window.father_birth_year.setMaxLength(4)
        
        # پر کردن کمبوباکس‌ها
        self.setup_location_combos()
        self.setup_date_combos()
        
        # چیدمان فیلدها
        father_layout.addWidget(QLabel("نام:"), 0, 0)
        father_layout.addWidget(self.main_window.father_first_name, 0, 1)
        father_layout.addWidget(QLabel("نام خانوادگی:"), 0, 2)
        father_layout.addWidget(self.main_window.father_last_name, 0, 3)
        
        father_layout.addWidget(QLabel("کد ملی:"), 1, 0)
        father_layout.addWidget(self.main_window.father_national_id, 1, 1)
        father_layout.addWidget(QLabel("موبایل:"), 1, 2)
        father_layout.addWidget(self.main_window.father_mobile, 1, 3)
        
        father_layout.addWidget(QLabel("استان تولد:"), 2, 0)
        father_layout.addWidget(self.main_window.father_birth_state, 2, 1)
        father_layout.addWidget(QLabel("شهر تولد:"), 2, 2)
        father_layout.addWidget(self.main_window.father_birth_city, 2, 3)
        
        father_layout.addWidget(QLabel("سال تولد:"), 3, 0)
        father_layout.addWidget(self.main_window.father_birth_year, 3, 1)
        father_layout.addWidget(QLabel("ماه تولد:"), 3, 2)
        father_layout.addWidget(self.main_window.father_birth_month, 3, 3)
        
        father_layout.addWidget(QLabel("روز تولد:"), 4, 0)
        father_layout.addWidget(self.main_window.father_birth_day, 4, 1)
        
        parent_layout.addWidget(father_group)
        
    def create_child_info_section(self, parent_layout):
        child_group = QGroupBox("اطلاعات فرزند")
        child_group.setStyleSheet(self.main_window.get_groupbox_style())
        child_layout = QGridLayout(child_group)
        
        self.main_window.child_first_name = QLineEdit()
        self.main_window.child_last_name = QLineEdit()
        self.main_window.child_national_id = QLineEdit()
        self.main_window.child_number = QSpinBox()
        
        self.main_window.child_birth_state = QComboBox()
        self.main_window.child_birth_city = QComboBox()
        self.main_window.child_birth_day = QComboBox()
        self.main_window.child_birth_month = QComboBox()
        self.main_window.child_birth_year = QLineEdit()
        
        # تنظیمات فیلدهای فرزند
        self.main_window.child_first_name.setPlaceholderText("نام فرزند")
        self.main_window.child_last_name.setPlaceholderText("نام خانوادگی فرزند")
        self.main_window.child_national_id.setPlaceholderText("کد ملی 10 رقمی")
        self.main_window.child_national_id.setMaxLength(10)
        self.main_window.child_birth_year.setPlaceholderText("سال تولد (شمسی)")
        self.main_window.child_birth_year.setMaxLength(4)
        
        self.main_window.child_number.setMinimum(1)
        self.main_window.child_number.setMaximum(10)
        self.main_window.child_number.setValue(1)
        
        # پر کردن کمبوباکس‌های فرزند
        self.setup_child_combos()
        
        child_layout.addWidget(QLabel("نام:"), 0, 0)
        child_layout.addWidget(self.main_window.child_first_name, 0, 1)
        child_layout.addWidget(QLabel("نام خانوادگی:"), 0, 2)
        child_layout.addWidget(self.main_window.child_last_name, 0, 3)
        
        child_layout.addWidget(QLabel("کد ملی:"), 1, 0)
        child_layout.addWidget(self.main_window.child_national_id, 1, 1)
        child_layout.addWidget(QLabel("تعداد فرزند:"), 1, 2)
        child_layout.addWidget(self.main_window.child_number, 1, 3)
        
        child_layout.addWidget(QLabel("استان تولد:"), 2, 0)
        child_layout.addWidget(self.main_window.child_birth_state, 2, 1)
        child_layout.addWidget(QLabel("شهر تولد:"), 2, 2)
        child_layout.addWidget(self.main_window.child_birth_city, 2, 3)
        
        child_layout.addWidget(QLabel("سال تولد:"), 3, 0)
        child_layout.addWidget(self.main_window.child_birth_year, 3, 1)
        child_layout.addWidget(QLabel("ماه تولد:"), 3, 2)
        child_layout.addWidget(self.main_window.child_birth_month, 3, 3)
        
        child_layout.addWidget(QLabel("روز تولد:"), 4, 0)
        child_layout.addWidget(self.main_window.child_birth_day, 4, 1)
        
        parent_layout.addWidget(child_group)
        
    def create_bank_info_section(self, parent_layout):
        bank_group = QGroupBox("اطلاعات بانک و آدرس")
        bank_group.setStyleSheet(self.main_window.get_groupbox_style())
        bank_layout = QGridLayout(bank_group)
        
        self.main_window.bank_name = QComboBox()
        self.main_window.branch_name = QLineEdit()
        self.main_window.address = QTextEdit()
        self.main_window.postal_code = QLineEdit()
        
        # تنظیمات فیلدهای بانک
        self.main_window.bank_name.addItems(["انتخاب بانک..."] + self.main_window.iran_banks)
        self.main_window.branch_name.setPlaceholderText("نام شعبه")
        self.main_window.address.setPlaceholderText("آدرس کامل")
        self.main_window.address.setMaximumHeight(80)
        self.main_window.postal_code.setPlaceholderText("کد پستی 10 رقمی")
        self.main_window.postal_code.setMaxLength(10)
        
        bank_layout.addWidget(QLabel("بانک:"), 0, 0)
        bank_layout.addWidget(self.main_window.bank_name, 0, 1)
        bank_layout.addWidget(QLabel("شعبه:"), 0, 2)
        bank_layout.addWidget(self.main_window.branch_name, 0, 3)
        
        bank_layout.addWidget(QLabel("آدرس:"), 1, 0)
        bank_layout.addWidget(self.main_window.address, 1, 1, 1, 3)
        
        bank_layout.addWidget(QLabel("کد پستی:"), 2, 0)
        bank_layout.addWidget(self.main_window.postal_code, 2, 1)
        
        parent_layout.addWidget(bank_group)
        
    def setup_location_combos(self):
        # استان‌ها برای پدر
        self.main_window.father_birth_state.addItem("انتخاب استان...")
        self.main_window.father_birth_state.addItems(list(self.main_window.provinces_cities.keys()))
        self.main_window.father_birth_state.currentTextChanged.connect(self.update_father_cities)
        
        # شهرها برای پدر
        self.main_window.father_birth_city.addItem("ابتدا استان را انتخاب کنید")
        
    def setup_child_combos(self):
        # استان‌ها برای فرزند
        self.main_window.child_birth_state.addItem("انتخاب استان...")
        self.main_window.child_birth_state.addItems(list(self.main_window.provinces_cities.keys()))
        self.main_window.child_birth_state.currentTextChanged.connect(self.update_child_cities)
        
        # شهرها برای فرزند
        self.main_window.child_birth_city.addItem("ابتدا استان را انتخاب کنید")
        
    def setup_date_combos(self):
        # ماه‌ها
        self.main_window.father_birth_month.addItem("انتخاب ماه...")
        self.main_window.father_birth_month.addItems(self.main_window.months)
        self.main_window.child_birth_month.addItem("انتخاب ماه...")
        self.main_window.child_birth_month.addItems(self.main_window.months)
        
        # روزها
        for combo in [self.main_window.father_birth_day, self.main_window.child_birth_day]:
            combo.addItem("انتخاب روز...")
            combo.addItems([str(i) for i in range(1, 32)])
            
    def update_father_cities(self, state):
        self.main_window.father_birth_city.clear()
        if state in self.main_window.provinces_cities:
            self.main_window.father_birth_city.addItem("انتخاب شهر...")
            self.main_window.father_birth_city.addItems(self.main_window.provinces_cities[state])
        else:
            self.main_window.father_birth_city.addItem("ابتدا استان را انتخاب کنید")
            
    def update_child_cities(self, state):
        self.main_window.child_birth_city.clear()
        if state in self.main_window.provinces_cities:
            self.main_window.child_birth_city.addItem("انتخاب شهر...")
            self.main_window.child_birth_city.addItems(self.main_window.provinces_cities[state])
        else:
            self.main_window.child_birth_city.addItem("ابتدا استان را انتخاب کنید")
            
    def apply_input_styles(self):
        input_style = """
            QLineEdit, QComboBox, QSpinBox, QTextEdit {
                background-color: #334155;
                border: 1px solid #64748B;
                border-radius: 6px;
                padding: 8px;
                color: #E2E8F0;
                font-size: 13px;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus {
                border-color: #3B82F6;
                background-color: #475569;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
        """
        
        # اعمال استایل به تمام فیلدها
        widgets = [
            self.main_window.father_first_name, self.main_window.father_last_name, 
            self.main_window.father_national_id, self.main_window.father_mobile, 
            self.main_window.father_birth_state, self.main_window.father_birth_city,
            self.main_window.father_birth_day, self.main_window.father_birth_month, 
            self.main_window.father_birth_year, self.main_window.child_first_name, 
            self.main_window.child_last_name, self.main_window.child_national_id,
            self.main_window.child_birth_state, self.main_window.child_birth_city, 
            self.main_window.child_birth_day, self.main_window.child_birth_month, 
            self.main_window.child_birth_year, self.main_window.child_number,
            self.main_window.bank_name, self.main_window.branch_name, 
            self.main_window.address, self.main_window.postal_code
        ]
        
        for widget in widgets:
            widget.setStyleSheet(input_style)
            
    def get_form_data(self):
        """جمع‌آوری داده‌ها از فرم"""
        return Applicant(
            father_first_name=self.main_window.father_first_name.text().strip(),
            father_last_name=self.main_window.father_last_name.text().strip(),
            father_national_id=self.main_window.father_national_id.text().strip(),
            father_mobile=self.main_window.father_mobile.text().strip(),
            father_birth_state=self.main_window.father_birth_state.currentText() if self.main_window.father_birth_state.currentIndex() > 0 else "",
            father_birth_city=self.main_window.father_birth_city.currentText() if self.main_window.father_birth_city.currentIndex() > 0 else "",
            father_birth_day=self.main_window.father_birth_day.currentText() if self.main_window.father_birth_day.currentIndex() > 0 else "",
            father_birth_month=self.main_window.father_birth_month.currentText() if self.main_window.father_birth_month.currentIndex() > 0 else "",
            father_birth_year=self.main_window.father_birth_year.text().strip(),
            child_first_name=self.main_window.child_first_name.text().strip(),
            child_last_name=self.main_window.child_last_name.text().strip(),
            child_national_id=self.main_window.child_national_id.text().strip(),
            child_birth_state=self.main_window.child_birth_state.currentText() if self.main_window.child_birth_state.currentIndex() > 0 else "",
            child_birth_city=self.main_window.child_birth_city.currentText() if self.main_window.child_birth_city.currentIndex() > 0 else "",
            child_birth_day=self.main_window.child_birth_day.currentText() if self.main_window.child_birth_day.currentIndex() > 0 else "",
            child_birth_month=self.main_window.child_birth_month.currentText() if self.main_window.child_birth_month.currentIndex() > 0 else "",
            child_birth_year=self.main_window.child_birth_year.text().strip(),
            child_number=str(self.main_window.child_number.value()),
            bank_name=self.main_window.bank_name.currentText() if self.main_window.bank_name.currentIndex() > 0 else "",
            branch_name=self.main_window.branch_name.text().strip(),
            address=self.main_window.address.toPlainText().strip(),
            postal_code=self.main_window.postal_code.text().strip()
        )
        
    def clear_form(self):
        """پاک کردن تمام فیلدهای فرم"""
        # فیلدهای پدر
        self.main_window.father_first_name.clear()
        self.main_window.father_last_name.clear()
        self.main_window.father_national_id.clear()
        self.main_window.father_mobile.clear()
        self.main_window.father_birth_state.setCurrentIndex(0)
        self.main_window.father_birth_city.clear()
        self.main_window.father_birth_city.addItem("ابتدا استان را انتخاب کنید")
        self.main_window.father_birth_day.setCurrentIndex(0)
        self.main_window.father_birth_month.setCurrentIndex(0)
        self.main_window.father_birth_year.clear()
        
        # فیلدهای فرزند
        self.main_window.child_first_name.clear()
        self.main_window.child_last_name.clear()
        self.main_window.child_national_id.clear()
        self.main_window.child_birth_state.setCurrentIndex(0)
        self.main_window.child_birth_city.clear()
        self.main_window.child_birth_city.addItem("ابتدا استان را انتخاب کنید")
        self.main_window.child_birth_day.setCurrentIndex(0)
        self.main_window.child_birth_month.setCurrentIndex(0)
        self.main_window.child_birth_year.clear()
        self.main_window.child_number.setValue(1)
        
        # فیلدهای بانک
        self.main_window.bank_name.setCurrentIndex(0)
        self.main_window.branch_name.clear()
        self.main_window.address.clear()
        self.main_window.postal_code.clear()
        
    def validate_form(self):
        """اعتبارسنجی فرم"""
        applicant = self.get_form_data()
        return applicant.is_valid(), applicant.get_validation_errors()