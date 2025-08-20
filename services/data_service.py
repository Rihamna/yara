#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime
from typing import List, Optional
from models.applicant import Applicant, ApplicantStatus

class DataService:
    def __init__(self):
        self.data_dir = "data"
        self.applicants_file = os.path.join(self.data_dir, "applicants.json")
        self.settings_file = os.path.join(self.data_dir, "settings.json")
        self.robot_data_dir = os.path.join(self.data_dir, "robot_data")
        
        self._ensure_directories_exist()
        
    def _ensure_directories_exist(self):
        """ایجاد پوشه‌های مورد نیاز"""
        directories = [
            self.data_dir,
            self.robot_data_dir,
            os.path.join(self.robot_data_dir, "وام_فرزندآوری"),
            os.path.join(self.robot_data_dir, "وام_ازدواج"),
            os.path.join(self.data_dir, "backups")
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                
    def load_applicants(self) -> List[Applicant]:
        """بارگذاری تمام متقاضیان"""
        try:
            if not os.path.exists(self.applicants_file):
                return []
                
            with open(self.applicants_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            applicants = []
            for item in data:
                applicant = Applicant.from_dict(item)
                applicants.append(applicant)
                
            return applicants
            
        except Exception as e:
            raise Exception(f"خطا در بارگذاری متقاضیان: {str(e)}")
            
    def save_applicants(self, applicants: List[Applicant]):
        """ذخیره تمام متقاضیان"""
        try:
            data = []
            for applicant in applicants:
                data.append(applicant.to_dict())
                
            with open(self.applicants_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            raise Exception(f"خطا در ذخیره متقاضیان: {str(e)}")
            
    def save_applicant(self, applicant: Applicant):
        """ذخیره یک متقاضی"""
        try:
            applicants = self.load_applicants()
            
            # بررسی وجود متقاضی
            existing_index = -1
            for i, existing_applicant in enumerate(applicants):
                if existing_applicant.id == applicant.id:
                    existing_index = i
                    break
                    
            if existing_index >= 0:
                # بروزرسانی
                applicants[existing_index] = applicant
            else:
                # اضافه کردن جدید
                applicants.append(applicant)
                
            self.save_applicants(applicants)
            
            # ذخیره جداگانه برای ربات
            self._save_applicant_for_robot(applicant)
            
        except Exception as e:
            raise Exception(f"خطا در ذخیره متقاضی: {str(e)}")
            
    def delete_applicant(self, applicant_id: str):
        """حذف متقاضی"""
        try:
            applicants = self.load_applicants()
            applicants = [a for a in applicants if a.id != applicant_id]
            self.save_applicants(applicants)
            
            # حذف فایل ربات
            self._delete_applicant_robot_file(applicant_id)
            
        except Exception as e:
            raise Exception(f"خطا در حذف متقاضی: {str(e)}")
            
    def update_applicant_status(self, applicant_id: str, new_status: ApplicantStatus):
        """بروزرسانی وضعیت متقاضی"""
        try:
            applicants = self.load_applicants()
            
            for applicant in applicants:
                if applicant.id == applicant_id:
                    applicant.update_status(new_status)
                    break
                    
            self.save_applicants(applicants)
            
        except Exception as e:
            raise Exception(f"خطا در بروزرسانی وضعیت: {str(e)}")
            
    def _save_applicant_for_robot(self, applicant: Applicant):
        """ذخیره فایل جداگانه برای ربات"""
        try:
            robot_path = os.path.join(self.robot_data_dir, "وام_فرزندآوری")
            file_name = f"applicant_{applicant.id}.json"
            file_path = os.path.join(robot_path, file_name)
            
            robot_data = {
                'id': applicant.id,
                'status': applicant.status.value,
                'created_at': applicant.created_at.isoformat(),
                'data': applicant.to_robot_data(),
                'tracking_number': applicant.generate_tracking_number()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(robot_data, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            raise Exception(f"خطا در ذخیره فایل ربات: {str(e)}")
            
    def _delete_applicant_robot_file(self, applicant_id: str):
        """حذف فایل ربات متقاضی"""
        try:
            robot_path = os.path.join(self.robot_data_dir, "وام_فرزندآوری")
            file_name = f"applicant_{applicant_id}.json"
            file_path = os.path.join(robot_path, file_name)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception:
            # در صورت خطا در حذف فایل، نادیده بگیر
            pass
            
    def get_pending_applicant_files(self) -> List[str]:
        """دریافت فایل‌های متقاضیان در انتظار"""
        try:
            robot_path = os.path.join(self.robot_data_dir, "وام_فرزندآوری")
            pending_files = []
            
            if not os.path.exists(robot_path):
                return pending_files
                
            for file_name in os.listdir(robot_path):
                if file_name.startswith("applicant_") and file_name.endswith(".json"):
                    file_path = os.path.join(robot_path, file_name)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                        if data.get('status') == 'pending':
                            pending_files.append(file_path)
                            
                    except Exception:
                        continue
                        
            return pending_files
            
        except Exception as e:
            raise Exception(f"خطا در بارگذاری فایل‌های ربات: {str(e)}")
            
    def load_settings(self) -> dict:
        """بارگذاری تنظیمات"""
        try:
            if not os.path.exists(self.settings_file):
                default_settings = self._get_default_settings()
                self.save_settings(default_settings)
                return default_settings
                
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                
            return settings
            
        except Exception as e:
            raise Exception(f"خطا در بارگذاری تنظیمات: {str(e)}")
            
    def save_settings(self, settings: dict):
        """ذخیره تنظیمات"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            raise Exception(f"خطا در ذخیره تنظیمات: {str(e)}")
            
    def _get_default_settings(self) -> dict:
        """تنظیمات پیش‌فرض"""
        return {
            'auto_start_robot': False,
            'retry_count': 3,
            'delay_between_retries': 5000,
            'show_notifications': True,
            'chrome_driver_path': '',
            'use_headless_browser': False,
            'max_concurrent_robots': 1,
            'auto_backup': True,
            'backup_interval_hours': 24,
            'last_backup': None
        }
        
    def create_backup(self) -> str:
        """ایجاد بکاپ"""
        try:
            backup_dir = os.path.join(self.data_dir, "backups")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"backup_{timestamp}.json")
            
            backup_data = {
                'created_at': datetime.now().isoformat(),
                'applicants': [a.to_dict() for a in self.load_applicants()],
                'settings': self.load_settings(),
                'version': '1.0'
            }
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=4)
                
            return backup_path
            
        except Exception as e:
            raise Exception(f"خطا در ایجاد بکاپ: {str(e)}")
            
    def restore_backup(self, backup_file_path: str):
        """بازیابی بکاپ"""
        try:
            if not os.path.exists(backup_file_path):
                raise FileNotFoundError("فایل بکاپ یافت نشد")
                
            with open(backup_file_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
                
            # بازیابی متقاضیان
            if 'applicants' in backup_data:
                applicants = []
                for item in backup_data['applicants']:
                    applicant = Applicant.from_dict(item)
                    applicants.append(applicant)
                self.save_applicants(applicants)
                
            # بازیابی تنظیمات
            if 'settings' in backup_data:
                self.save_settings(backup_data['settings'])
                
        except Exception as e:
            raise Exception(f"خطا در بازیابی بکاپ: {str(e)}")
            
    def get_stats(self) -> dict:
        """آمار متقاضیان"""
        try:
            applicants = self.load_applicants()
            
            total_count = len(applicants)
            pending_count = len([a for a in applicants if a.status == ApplicantStatus.PENDING])
            processing_count = len([a for a in applicants if a.status == ApplicantStatus.PROCESSING])
            completed_count = len([a for a in applicants if a.status == ApplicantStatus.COMPLETED])
            failed_count = len([a for a in applicants if a.status == ApplicantStatus.FAILED])
            
            today = datetime.now().date()
            today_count = len([a for a in applicants if a.created_at.date() == today])
            
            week_ago = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            week_ago = week_ago.replace(day=week_ago.day - 7)
            week_count = len([a for a in applicants if a.created_at >= week_ago])
            
            month_count = len([a for a in applicants 
                             if a.created_at.month == datetime.now().month and 
                                a.created_at.year == datetime.now().year])
            
            success_rate = (completed_count / total_count * 100) if total_count > 0 else 0
            
            return {
                'total_count': total_count,
                'pending_count': pending_count,
                'processing_count': processing_count,
                'completed_count': completed_count,
                'failed_count': failed_count,
                'today_count': today_count,
                'week_count': week_count,
                'month_count': month_count,
                'success_rate': round(success_rate, 2)
            }
            
        except Exception as e:
            raise Exception(f"خطا در محاسبه آمار: {str(e)}")
            
    def get_current_time(self) -> str:
        """زمان فعلی به صورت متنی"""
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
    def cleanup_old_files(self, days: int = 30):
        """پاکسازی فایل‌های قدیمی"""
        try:
            cutoff_date = datetime.now().replace(day=datetime.now().day - days)
            
            # پاکسازی فایل‌های ربات قدیمی
            robot_path = os.path.join(self.robot_data_dir, "وام_فرزندآوری")
            
            if os.path.exists(robot_path):
                for file_name in os.listdir(robot_path):
                    file_path = os.path.join(robot_path, file_name)
                    
                    if os.path.isfile(file_path):
                        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        if file_time < cutoff_date:
                            os.remove(file_path)
                            
        except Exception as e:
            raise Exception(f"خطا در پاکسازی فایل‌ها: {str(e)}")