#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
from datetime import datetime
from enum import Enum

class ApplicantStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Applicant:
    def __init__(self, father_national_id="", father_birth_state="", father_birth_city="",
                 father_birth_day="", father_birth_month="", father_birth_year="", 
                 father_mobile="", child_national_id="", child_birth_state="", 
                 child_birth_city="", child_birth_day="", child_birth_month="", 
                 child_birth_year="", child_number="", applicant_id=None):
        
        self.id = applicant_id if applicant_id else str(uuid.uuid4())
        
        # اطلاعات پدر
        self.father_national_id = father_national_id
        self.father_birth_state = father_birth_state
        self.father_birth_city = father_birth_city
        self.father_birth_day = father_birth_day
        self.father_birth_month = father_birth_month
        self.father_birth_year = father_birth_year
        self.father_mobile = father_mobile
        
        # اطلاعات فرزند
        self.child_national_id = child_national_id
        self.child_birth_state = child_birth_state
        self.child_birth_city = child_birth_city
        self.child_birth_day = child_birth_day
        self.child_birth_month = child_birth_month
        self.child_birth_year = child_birth_year
        self.child_number = child_number
        
        # اطلاعات وضعیت
        self.status = ApplicantStatus.PENDING
        self.created_at = datetime.now()
        self.completion_time = None
        self.error_message = None
        
    @property
    def display_name(self):
        """نام نمایشی برای UI"""
        father_part = self.father_national_id[-4:] if len(self.father_national_id) >= 4 else "****"
        child_part = self.child_national_id[-4:] if len(self.child_national_id) >= 4 else "****"
        return f"پدر: {father_part} - فرزند: {child_part}"
        
    @property
    def status_text(self):
        """متن وضعیت"""
        status_map = {
            ApplicantStatus.PENDING: "در انتظار",
            ApplicantStatus.PROCESSING: "در حال پردازش",
            ApplicantStatus.COMPLETED: "تکمیل شده",
            ApplicantStatus.FAILED: "ناموفق"
        }
        return status_map.get(self.status, "نامشخص")
        
    @property
    def status_emoji(self):
        """آیکون وضعیت"""
        emoji_map = {
            ApplicantStatus.PENDING: "⏳",
            ApplicantStatus.PROCESSING: "🔄",
            ApplicantStatus.COMPLETED: "✅",
            ApplicantStatus.FAILED: "❌"
        }
        return emoji_map.get(self.status, "❓")
        
    def is_valid(self):
        """اعتبارسنجی اطلاعات"""
        errors = self.get_validation_errors()
        return len(errors) == 0
        
    def get_validation_errors(self):
        """لیست خطاهای اعتبارسنجی"""
        errors = []
        
        # بررسی کد ملی پدر
        if not self.father_national_id:
            errors.append("شماره ملی پدر الزامی است")
        elif len(self.father_national_id) != 10 or not self._is_valid_national_id(self.father_national_id):
            errors.append("شماره ملی پدر معتبر نیست")
            
        # بررسی کد ملی فرزند
        if not self.child_national_id:
            errors.append("کد ملی فرزند الزامی است")
        elif len(self.child_national_id) != 10 or not self._is_valid_national_id(self.child_national_id):
            errors.append("کد ملی فرزند معتبر نیست")
            
        # بررسی شماره موبایل
        if not self.father_mobile:
            errors.append("شماره موبایل پدر الزامی است")
        elif len(self.father_mobile) != 11 or not self.father_mobile.startswith("09"):
            errors.append("شماره موبایل پدر معتبر نیست")
            
        # بررسی تاریخ تولد پدر
        if not all([self.father_birth_year, self.father_birth_month, self.father_birth_day]):
            errors.append("تاریخ تولد پدر الزامی است")
            
        # بررسی تاریخ تولد فرزند
        if not all([self.child_birth_year, self.child_birth_month, self.child_birth_day]):
            errors.append("تاریخ تولد فرزند الزامی است")
            
        # بررسی استان و شهر
        if not self.father_birth_state or not self.father_birth_city:
            errors.append("محل تولد پدر الزامی است")
            
        if not self.child_birth_state or not self.child_birth_city:
            errors.append("محل تولد فرزند الزامی است")
            
        return errors
        
    def to_robot_data(self):
        """تبدیل به فرمت مورد نیاز ربات"""
        return {
            'father_national_id': self.father_national_id,
            'father_birth_state': self.father_birth_state,
            'father_birth_city': self.father_birth_city,
            'father_birth_day': self.father_birth_day,
            'father_birth_month': self.father_birth_month,
            'father_birth_year': self.father_birth_year,
            'father_mobile': self.father_mobile,
            'child_national_id': self.child_national_id,
            'child_birth_state': self.child_birth_state,
            'child_birth_city': self.child_birth_city,
            'child_birth_day': self.child_birth_day,
            'child_birth_month': self.child_birth_month,
            'child_birth_year': self.child_birth_year,
            'child_number': self.child_number
        }
        
    def to_dict(self):
        """تبدیل به دیکشنری برای ذخیره JSON"""
        return {
            'id': self.id,
            'father_national_id': self.father_national_id,
            'father_birth_state': self.father_birth_state,
            'father_birth_city': self.father_birth_city,
            'father_birth_day': self.father_birth_day,
            'father_birth_month': self.father_birth_month,
            'father_birth_year': self.father_birth_year,
            'father_mobile': self.father_mobile,
            'child_national_id': self.child_national_id,
            'child_birth_state': self.child_birth_state,
            'child_birth_city': self.child_birth_city,
            'child_birth_day': self.child_birth_day,
            'child_birth_month': self.child_birth_month,
            'child_birth_year': self.child_birth_year,
            'child_number': self.child_number,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'completion_time': self.completion_time,
            'error_message': self.error_message
        }
        
    @classmethod
    def from_dict(cls, data):
        """ایجاد از دیکشنری"""
        applicant = cls(
            applicant_id=data.get('id'),
            father_national_id=data.get('father_national_id', ''),
            father_birth_state=data.get('father_birth_state', ''),
            father_birth_city=data.get('father_birth_city', ''),
            father_birth_day=data.get('father_birth_day', ''),
            father_birth_month=data.get('father_birth_month', ''),
            father_birth_year=data.get('father_birth_year', ''),
            father_mobile=data.get('father_mobile', ''),
            child_national_id=data.get('child_national_id', ''),
            child_birth_state=data.get('child_birth_state', ''),
            child_birth_city=data.get('child_birth_city', ''),
            child_birth_day=data.get('child_birth_day', ''),
            child_birth_month=data.get('child_birth_month', ''),
            child_birth_year=data.get('child_birth_year', ''),
            child_number=data.get('child_number', '')
        )
        
        # تنظیم وضعیت
        status_str = data.get('status', 'pending')
        for status in ApplicantStatus:
            if status.value == status_str:
                applicant.status = status
                break
                
        # تنظیم تاریخ‌ها
        if data.get('created_at'):
            applicant.created_at = datetime.fromisoformat(data['created_at'])
            
        applicant.completion_time = data.get('completion_time')
        applicant.error_message = data.get('error_message')
        
        return applicant
        
    def clone(self):
        """ایجاد کپی"""
        cloned = Applicant(
            father_national_id=self.father_national_id,
            father_birth_state=self.father_birth_state,
            father_birth_city=self.father_birth_city,
            father_birth_day=self.father_birth_day,
            father_birth_month=self.father_birth_month,
            father_birth_year=self.father_birth_year,
            father_mobile=self.father_mobile,
            child_national_id=self.child_national_id,
            child_birth_state=self.child_birth_state,
            child_birth_city=self.child_birth_city,
            child_birth_day=self.child_birth_day,
            child_birth_month=self.child_birth_month,
            child_birth_year=self.child_birth_year,
            child_number=self.child_number
        )
        
        cloned.status = ApplicantStatus.PENDING
        cloned.created_at = datetime.now()
        
        return cloned
        
    def _is_valid_national_id(self, national_id):
        """اعتبارسنجی کد ملی ایرانی"""
        if not national_id or len(national_id) != 10:
            return False
            
        # بررسی تکراری نبودن ارقام
        if national_id == national_id[0] * 10:
            return False
            
        try:
            total = 0
            for i in range(9):
                total += int(national_id[i]) * (10 - i)
                
            remainder = total % 11
            check_digit = int(national_id[9])
            
            return (remainder < 2 and check_digit == remainder) or \
                   (remainder >= 2 and check_digit == 11 - remainder)
                   
        except (ValueError, IndexError):
            return False
            
    def generate_tracking_number(self):
        """تولید شماره پیگیری"""
        date_str = self.created_at.strftime("%Y%m%d")
        id_str = self.id.replace("-", "")[:8].upper()
        return f"FR{date_str}{id_str}"
        
    def update_status(self, new_status, message=None):
        """بروزرسانی وضعیت"""
        self.status = new_status
        
        if new_status == ApplicantStatus.COMPLETED:
            self.completion_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            
        if message:
            self.error_message = message
            
    def __str__(self):
        return f"Applicant: {self.display_name} - Status: {self.status_text} - Created: {self.created_at.strftime('%Y/%m/%d')}"
        
    def __eq__(self, other):
        if isinstance(other, Applicant):
            return self.id == other.id
        return False
        
    def __hash__(self):
        return hash(self.id)