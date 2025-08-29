#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QGroupBox, QLineEdit, QMessageBox, QDialog, 
                            QDialogButtonBox, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from models.applicant import ApplicantStatus
import datetime
import time

class RobotThread(QThread):
    status_update = pyqtSignal(str)
    sms_required = pyqtSignal()
    completed = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, applicant_data):
        super().__init__()
        self.applicant_data = applicant_data
        self.sms_code = None
        self.is_running = True
        
    def run(self):
        try:
            self.status_update.emit("شروع فرآیند ثبت نام...")
            time.sleep(1)
            
            if not self.is_running:
                return
                
            self.status_update.emit("در حال پر کردن فرم...")
            time.sleep(2)
            
            if not self.is_running:
                return
                
            self.status_update.emit("ارسال اطلاعات به سرور...")
            time.sleep(1)
            
            if not self.is_running:
                return
            
            # شبیه‌سازی نیاز به کد SMS
            self.status_update.emit("در انتظار کد تأیید SMS...")
            self.sms_required.emit()
            
            # منتظر کد SMS بمانید
            for _ in range(60):  # 60 ثانیه انتظار
                if not self.is_running:
                    return
                if self.sms_code:
                    break
                time.sleep(1)
            
            if not self.is_running:
                return
                
            if self.sms_code and self.sms_code == "123456":  # کد تست
                self.status_update.emit("کد تأیید شده. تکمیل فرآیند...")
                time.sleep(2)
                tracking_code = f"FR{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.completed.emit(True, tracking_code)
            else:
                self.status_update.emit("کد تأیید نامعتبر یا timeout")
                self.completed.emit(False, "کد تأیید نامعتبر")
                
        except Exception as e:
            self.status_update.emit(f"خطا: {str(e)}")
            self.completed.emit(False, str(e))
    
    def submit_sms_code(self, code):
        self.sms_code = code
        
    def stop(self):
        self.is_running = False
        self.quit()

class SMSDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("کد تأیید SMS")
        self.setModal(True)
        self.resize(300, 150)
        self.setStyleSheet("""
            QDialog {
                background-color: #2D3748;
                color: #E2E8F0;
            }
            QLineEdit {
                background-color: #4A5568;
                border: 1px solid #718096;
                border-radius: 5px;
                padding: 8px;
                color: #E2E8F0;
                font-size: 14px;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        label = QLabel("کد تأیید ارسال شده را وارد کنید:")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("کد 6 رقمی")
        self.code_input.setMaxLength(6)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.setStyleSheet("""
            QPushButton {
                background-color: #4299E1;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3182CE;
            }
        """)
        
        layout.addWidget(label)
        layout.addWidget(self.code_input)
        layout.addWidget(buttons)
        
    def get_code(self):
        return self.code_input.text().strip()

class RobotController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.robot_thread = None
        self.sms_dialog = None
        self.current_list_tab = "pending"
        
    def create_robot_controls(self, parent_layout):
        controls_frame = QGroupBox("کنترل ربات")
        controls_frame.setStyleSheet(self.main_window.get_groupbox_style())
        
        controls_layout = QHBoxLayout(controls_frame)
        
        self.start_robot_btn = QPushButton("▶ شروع ربات")
        self.start_robot_btn.setStyleSheet(self.main_window.get_button_style("#10B981", "#059669"))
        self.start_robot_btn.clicked.connect(self.start_robot)
        
        self.stop_robot_btn = QPushButton("⏸ توقف ربات")
        self.stop_robot_btn.setStyleSheet(self.main_window.get_button_style("#EF4444", "#DC2626"))
        self.stop_robot_btn.clicked.connect(self.stop_robot)
        self.stop_robot_btn.setEnabled(False)
        
        controls_layout.addWidget(self.start_robot_btn)
        controls_layout.addWidget(self.stop_robot_btn)
        
        parent_layout.addWidget(controls_frame)
        
    def create_action_buttons(self, parent_layout):
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        
        self.save_btn = QPushButton("💾 ذخیره متقاضی")
        self.save_btn.setStyleSheet(self.main_window.get_button_style("#3B82F6", "#2563EB"))
        self.save_btn.clicked.connect(self.save_applicant)
        
        self.clear_btn = QPushButton("🧹 پاک کردن فرم")
        self.clear_btn.setStyleSheet(self.main_window.get_button_style("#6B7280", "#4B5563"))
        self.clear_btn.clicked.connect(self.clear_form)
        
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.clear_btn)
        
        parent_layout.addWidget(buttons_frame)
        
    def create_sms_panel(self, parent_layout):
        self.sms_frame = QFrame()
        self.sms_frame.setStyleSheet("""
            QFrame {
                background-color: #FEF3C7;
                border: 1px solid #F59E0B;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        self.sms_frame.hide()
        
        sms_layout = QVBoxLayout(self.sms_frame)
        
        sms_title = QLabel("⏰ در انتظار کد تأیید SMS")
        sms_title.setStyleSheet("color: #B45309; font-weight: bold; font-size: 14px;")
        
        sms_desc = QLabel("کد تأیید ارسال شده به شماره موبایل را وارد کنید:")
        sms_desc.setStyleSheet("color: #92400E; font-size: 12px; margin-top: 5px;")
        
        code_layout = QHBoxLayout()
        
        self.sms_input = QLineEdit()
        self.sms_input.setPlaceholderText("کد 6 رقمی")
        self.sms_input.setMaxLength(6)
        self.sms_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #F59E0B;
                color: #92400E;
                font-weight: bold;
                text-align: center;
            }
        """)
        
        self.submit_sms_btn = QPushButton("ارسال کد")
        self.submit_sms_btn.setStyleSheet(self.main_window.get_button_style("#F59E0B", "#D97706"))
        self.submit_sms_btn.clicked.connect(self.submit_sms_code)
        
        code_layout.addWidget(self.sms_input)
        code_layout.addWidget(self.submit_sms_btn)
        
        sms_layout.addWidget(sms_title)
        sms_layout.addWidget(sms_desc)
        sms_layout.addLayout(code_layout)
        
        parent_layout.addWidget(self.sms_frame)
        
    def create_lists_section_widget(self):
        """ایجاد ویجت بخش لیست‌ها"""
        lists_frame = QFrame()
        lists_frame.setStyleSheet("""
            QFrame {
                background-color: #363A4F;
                border-radius: 12px;
                border: 1px solid #4A4E5C;
            }
        """)
        lists_frame.setMinimumWidth(400)
        
        lists_layout = QVBoxLayout(lists_frame)
        lists_layout.setContentsMargins(20, 20, 20, 20)
        lists_layout.setSpacing(16)
        
        # عنوان
        title = QLabel("مدیریت متقاضیان")
        title.setStyleSheet("""
            color: #FFFFFF;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        """)
        lists_layout.addWidget(title)
        
        # تب‌ها
        tabs_frame = QFrame()
        tabs_layout = QHBoxLayout(tabs_frame)
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        tabs_layout.setSpacing(8)
        
        self.pending_tab_btn = QPushButton("در انتظار")
        self.completed_tab_btn = QPushButton("تکمیل شده")
        
        tab_style = """
            QPushButton {
                background-color: #4A4E5C;
                color: #8B92A8;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #5A5E6C;
                color: #FFFFFF;
            }
        """
        
        active_tab_style = """
            QPushButton {
                background-color: #4F8EF7;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: 500;
                font-size: 13px;
            }
        """
        
        self.pending_tab_btn.setStyleSheet(active_tab_style)
        self.completed_tab_btn.setStyleSheet(tab_style)
        
        self.pending_tab_btn.clicked.connect(lambda: self.switch_list_tab("pending"))
        self.completed_tab_btn.clicked.connect(lambda: self.switch_list_tab("completed"))
        
        tabs_layout.addWidget(self.pending_tab_btn)
        tabs_layout.addWidget(self.completed_tab_btn)
        tabs_layout.addStretch()
        
        lists_layout.addWidget(tabs_frame)
        
        # لیست متقاضیان
        self.applicants_list = QListWidget()
        self.applicants_list.setStyleSheet("""
            QListWidget {
                background-color: #2A2D3E;
                border: 1px solid #4A4E5C;
                border-radius: 8px;
                color: #FFFFFF;
                padding: 8px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #4A4E5C;
                border-radius: 6px;
                margin-bottom: 4px;
            }
            QListWidget::item:selected {
                background-color: #4F8EF7;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #4A4E5C;
                color: white;
            }
        """)
        
        lists_layout.addWidget(self.applicants_list)
        
        # دکمه‌های عملیات
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(10)
        
        self.delete_btn = QPushButton("حذف")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected_applicant)
        
        self.refresh_btn = QPushButton("🔄 بروزرسانی")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_lists)
        
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.refresh_btn)
        buttons_layout.addStretch()
        
        lists_layout.addWidget(buttons_frame)
        
        # بارگذاری اولیه
        self.refresh_lists()
        
        return lists_frame
        
    def start_robot(self):
        # بررسی وجود متقاضی در انتظار
        try:
            applicants = self.main_window.data_service.load_applicants()
            pending_applicants = [a for a in applicants if a.status == ApplicantStatus.PENDING]
            
            if not pending_applicants:
                QMessageBox.warning(self.main_window, "هشدار", "هیچ متقاضی در انتظار وجود ندارد!")
                return
                
            # انتخاب اولین متقاضی در انتظار
            self.main_window.current_applicant = pending_applicants[0]
            
            # شروع ربات
            self.robot_thread = RobotThread(self.main_window.current_applicant.to_robot_data())
            self.robot_thread.status_update.connect(self.update_robot_status)
            self.robot_thread.sms_required.connect(self.show_sms_dialog)
            self.robot_thread.completed.connect(self.robot_completed)
            
            self.robot_thread.start()
            
            # تغییر وضعیت دکمه‌ها
            self.start_robot_btn.setEnabled(False)
            self.stop_robot_btn.setEnabled(True)
            
            # بروزرسانی وضعیت متقاضی
            self.main_window.current_applicant.status = ApplicantStatus.PROCESSING
            self.main_window.data_service.save_applicant(self.main_window.current_applicant)
            self.refresh_lists()
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "خطا", f"خطا در شروع ربات: {str(e)}")
            
    def stop_robot(self):
        if self.robot_thread and self.robot_thread.isRunning():
            self.robot_thread.stop()
            self.robot_thread.wait(3000)  # انتظار 3 ثانیه برای توقف
            
        self.start_robot_btn.setEnabled(True)
        self.stop_robot_btn.setEnabled(False)
        self.sms_frame.hide()
        
        if self.main_window.current_applicant:
            self.main_window.current_applicant.status = ApplicantStatus.PENDING
            self.main_window.data_service.save_applicant(self.main_window.current_applicant)
            self.refresh_lists()
            
    def update_robot_status(self, message):
        # نمایش وضعیت ربات در UI
        print(f"Robot Status: {message}")  # برای حالا فقط print کنیم
        
    def show_sms_dialog(self):
        self.sms_frame.show()
        
    def submit_sms_code(self):
        code = self.sms_input.text().strip()
        if code and len(code) == 6:
            if self.robot_thread:
                self.robot_thread.submit_sms_code(code)
            self.sms_frame.hide()
        else:
            QMessageBox.warning(self.main_window, "خطا", "کد SMS باید 6 رقمی باشد!")
            
    def robot_completed(self, success, message):
        self.start_robot_btn.setEnabled(True)
        self.stop_robot_btn.setEnabled(False)
        self.sms_frame.hide()
        
        if self.main_window.current_applicant:
            if success:
                self.main_window.current_applicant.status = ApplicantStatus.COMPLETED
                self.main_window.current_applicant.tracking_code = message
                self.main_window.current_applicant.completion_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                QMessageBox.information(self.main_window, "موفقیت", f"ثبت نام با موفقیت انجام شد!\nکد رهگیری: {message}")
            else:
                self.main_window.current_applicant.status = ApplicantStatus.FAILED
                self.main_window.current_applicant.error_message = message
                QMessageBox.warning(self.main_window, "خطا", f"ثبت نام ناموفق بود:\n{message}")
                
            self.main_window.data_service.save_applicant(self.main_window.current_applicant)
            self.refresh_lists()
            
    def save_applicant(self):
        try:
            # اعتبارسنجی فرم
            is_valid, errors = self.main_window.form_handler.validate_form()
            
            if not is_valid:
                error_message = "لطفا خطاهای زیر را برطرف کنید:\n\n" + "\n".join(errors)
                QMessageBox.warning(self.main_window, "خطای اعتبارسنجی", error_message)
                return
                
            # دریافت داده‌ها از فرم
            applicant = self.main_window.form_handler.get_form_data()
            
            # ذخیره در دیتابیس
            self.main_window.data_service.save_applicant(applicant)
            
            QMessageBox.information(self.main_window, "موفقیت", "متقاضی با موفقیت ذخیره شد!")
            
            # پاک کردن فرم و بروزرسانی لیست
            self.clear_form()
            self.refresh_lists()
            
        except Exception as e:
            QMessageBox.critical(self.main_window, "خطا", f"خطا در ذخیره متقاضی: {str(e)}")
            
    def clear_form(self):
        self.main_window.form_handler.clear_form()
        
    def switch_list_tab(self, tab_name):
        self.current_list_tab = tab_name
        
        tab_style = """
            QPushButton {
                background-color: #334155;
                color: #94A3B8;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #475569;
            }
        """
        
        active_tab_style = """
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
            }
        """
        
        if tab_name == "pending":
            self.pending_tab_btn.setStyleSheet(active_tab_style)
            self.completed_tab_btn.setStyleSheet(tab_style)
        else:
            self.pending_tab_btn.setStyleSheet(tab_style)
            self.completed_tab_btn.setStyleSheet(active_tab_style)
            
        self.refresh_lists()
        
    def refresh_lists(self):
        try:
            self.applicants_list.clear()
            applicants = self.main_window.data_service.load_applicants()
            
            if self.current_list_tab == "pending":
                filtered_applicants = [a for a in applicants if a.status == ApplicantStatus.PENDING]
            else:
                filtered_applicants = [a for a in applicants if a.status in [ApplicantStatus.COMPLETED, ApplicantStatus.FAILED]]
                
            for applicant in filtered_applicants:
                item_text = f"{applicant.display_name} - {applicant.bank_name} - {applicant.status_text}"
                if hasattr(applicant, 'status_emoji'):
                    item_text = f"{applicant.status_emoji} {item_text}"
                    
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, applicant.id)
                self.applicants_list.addItem(item)
                
        except Exception as e:
            QMessageBox.warning(self.main_window, "خطا", f"خطا در بروزرسانی لیست: {str(e)}")
            
    def delete_selected_applicant(self):
        current_item = self.applicants_list.currentItem()
        if not current_item:
            QMessageBox.warning(self.main_window, "هشدار", "لطفا یک متقاضی را انتخاب کنید!")
            return
            
        applicant_id = current_item.data(Qt.UserRole)
        
        reply = QMessageBox.question(
            self.main_window, 
            "تأیید حذف", 
            "آیا از حذف این متقاضی اطمینان دارید؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.main_window.data_service.delete_applicant(applicant_id)
                self.refresh_lists()
                QMessageBox.information(self.main_window, "موفقیت", "متقاضی با موفقیت حذف شد!")
            except Exception as e:
                QMessageBox.critical(self.main_window, "خطا", f"خطا در حذف متقاضی: {str(e)}")