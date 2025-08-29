#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QGroupBox, QScrollArea)
from PyQt5.QtCore import Qt
from .ui_styles import UIStyles

class PageManager:
    def __init__(self, main_window):
        self.main_window = main_window
        
    def create_home_page(self):
        """ایجاد صفحه خانگی مطابق طراحی جدید"""
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # هدر خوشامدگویی
        welcome_frame = self.create_welcome_header()
        layout.addWidget(welcome_frame)
        
        # ردیف اول - کارت‌های اطلاعات
        info_row = QHBoxLayout()
        info_row.setSpacing(20)
        
        # کارت وضعیت ربات‌ها
        robot_status_card = self.create_robot_status_card()
        info_row.addWidget(robot_status_card, 2)
        
        # کارت وضعیت API ها
        api_status_card = self.create_api_status_card()
        info_row.addWidget(api_status_card, 1)
        
        layout.addLayout(info_row)
        
        # ردیف دوم - آمار تفصیلی
        stats_card = self.create_detailed_stats_card()
        layout.addWidget(stats_card)
        
        layout.addStretch()
        return home_widget
        
    def create_welcome_header(self):
        """ایجاد هدر خوشامدگویی"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {UIStyles.COLORS['accent_blue']}, 
                    stop:1 #667eea);
                border-radius: 12px;
                padding: 24px;
            }}
        """)
        frame.setMaximumHeight(120)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(8)
        
        title = QLabel("خوش آمدید به YARA")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        
        subtitle = QLabel("سیستم مدیریت ربات‌های خودکار ثبت‌نام وام")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            font-weight: 400;
        """)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        return frame
        
    def create_robot_status_card(self):
        """کارت وضعیت ربات‌ها"""
        card = QFrame()
        card.setStyleSheet(UIStyles.get_card_style())
        
        layout = QVBoxLayout(card)
        layout.setSpacing(16)
        
        # عنوان کارت
        title = QLabel("وضعیت ربات‌ها")
        title.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        """)
        layout.addWidget(title)
        
        # ربات وام فرزند
        child_robot = self.create_robot_item(
            "ربات وام فرزند", 
            "فعال", 
            "25 روز باقیمانده", 
            "#10B981"
        )
        layout.addWidget(child_robot)
        
        # ربات وام ازدواج
        marriage_robot = self.create_robot_item(
            "ربات وام ازدواج", 
            "در حال توسعه", 
            "تاریخ انتشار: 2 هفته دیگر", 
            "#F59E0B"
        )
        layout.addWidget(marriage_robot)
        
        return card
        
    def create_robot_item(self, name, status, info, color):
        """ایتم ربات"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {UIStyles.COLORS['bg_primary']};
                border-left: 3px solid {color};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(4)
        
        # عنوان و وضعیت
        header_layout = QHBoxLayout()
        
        robot_name = QLabel(name)
        robot_name.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_primary']};
            font-weight: 500;
            font-size: 14px;
        """)
        
        status_label = QLabel(f"● {status}")
        status_label.setStyleSheet(f"""
            color: {color};
            font-weight: 500;
            font-size: 12px;
        """)
        
        header_layout.addWidget(robot_name)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        # اطلاعات اضافی
        info_label = QLabel(info)
        info_label.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_muted']};
            font-size: 11px;
        """)
        
        layout.addLayout(header_layout)
        layout.addWidget(info_label)
        
        return frame
        
    def create_api_status_card(self):
        """کارت وضعیت API ها"""
        card = QFrame()
        card.setStyleSheet(UIStyles.get_card_style())
        
        layout = QVBoxLayout(card)
        layout.setSpacing(16)
        
        # عنوان
        title = QLabel("وضعیت API ها")
        title.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        """)
        layout.addWidget(title)
        
        # لیست API ها
        apis = [
            ("SMS Forwarder", True),
            ("2Captcha", True),
            ("Database", True),
            ("Selenium", False)
        ]
        
        for api_name, is_connected in apis:
            api_item = self.create_api_item(api_name, is_connected)
            layout.addWidget(api_item)
            
        return card
        
    def create_api_item(self, name, is_connected):
        """ایتم API"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {UIStyles.COLORS['bg_primary']};
                border-radius: 6px;
                padding: 10px 12px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        
        name_label = QLabel(name)
        name_label.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_primary']};
            font-size: 12px;
            font-weight: 400;
        """)
        
        status_color = "#10B981" if is_connected else "#EF4444"
        status_text = "متصل" if is_connected else "قطع"
        status_label = QLabel(f"● {status_text}")
        status_label.setStyleSheet(f"""
            color: {status_color};
            font-size: 11px;
            font-weight: 500;
        """)
        
        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(status_label)
        
        return frame
        
    def create_detailed_stats_card(self):
        """کارت آمار تفصیلی"""
        card = QFrame()
        card.setStyleSheet(UIStyles.get_card_style())
        
        layout = QVBoxLayout(card)
        layout.setSpacing(20)
        
        # عنوان
        title = QLabel("آمار تفصیلی متقاضیان")
        title.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
        """)
        layout.addWidget(title)
        
        try:
            stats = self.main_window.data_service.get_stats()
            
            # ردیف اول آمار
            first_row = QHBoxLayout()
            first_row.setSpacing(20)
            
            stat_items_1 = [
                ("کل متقاضیان", str(stats.get('total_count', 0)), "#3B82F6"),
                ("در انتظار", str(stats.get('pending_count', 0)), "#F59E0B"),
                ("در حال پردازش", str(stats.get('processing_count', 0)), "#8B5CF6"),
                ("تکمیل شده", str(stats.get('completed_count', 0)), "#10B981")
            ]
            
            for label, value, color in stat_items_1:
                stat_widget = self.create_stat_widget(label, value, color)
                first_row.addWidget(stat_widget)
                
            # ردیف دوم آمار
            second_row = QHBoxLayout()
            second_row.setSpacing(20)
            
            stat_items_2 = [
                ("ناموفق", str(stats.get('failed_count', 0)), "#EF4444"),
                ("امروز", str(stats.get('today_count', 0)), "#06B6D4"),
                ("این هفته", str(stats.get('week_count', 0)), "#84CC16"),
                ("این ماه", str(stats.get('month_count', 0)), "#F97316")
            ]
            
            for label, value, color in stat_items_2:
                stat_widget = self.create_stat_widget(label, value, color)
                second_row.addWidget(stat_widget)
                
            layout.addLayout(first_row)
            layout.addLayout(second_row)
            
            # نرخ موفقیت
            success_rate = stats.get('success_rate', 0)
            success_widget = self.create_success_rate_widget(success_rate)
            layout.addWidget(success_widget)
            
        except Exception as e:
            error_label = QLabel(f"خطا در بارگذاری آمار: {str(e)}")
            error_label.setStyleSheet(f"color: {UIStyles.COLORS['text_muted']}; font-size: 14px;")
            layout.addWidget(error_label)
            
        return card
        
    def create_stat_widget(self, label, value, color):
        """ویجت آمار"""
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {UIStyles.COLORS['bg_primary']};
                border-left: 3px solid {color};
                border-radius: 8px;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(6)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 22px;
            font-weight: bold;
        """)
        
        label_label = QLabel(label)
        label_label.setAlignment(Qt.AlignCenter)
        label_label.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_secondary']};
            font-size: 12px;
            font-weight: 400;
        """)
        
        layout.addWidget(value_label)
        layout.addWidget(label_label)
        
        return widget
        
    def create_success_rate_widget(self, success_rate):
        """ویجت نرخ موفقیت"""
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {UIStyles.COLORS['bg_primary']};
                border-radius: 8px;
                padding: 16px;
                margin-top: 10px;
            }}
        """)
        
        layout = QHBoxLayout(widget)
        
        label = QLabel("نرخ موفقیت:")
        label.setStyleSheet(f"""
            color: {UIStyles.COLORS['text_primary']};
            font-size: 14px;
            font-weight: 500;
        """)
        
        value = QLabel(f"{success_rate}%")
        value.setStyleSheet(f"""
            color: {UIStyles.COLORS['accent_blue']};
            font-size: 18px;
            font-weight: bold;
        """)
        
        layout.addWidget(label)
        layout.addWidget(value)
        layout.addStretch()
        
        return widget
        
    def create_child_loan_page(self):
        """صفحه ربات وام فرزند"""
        page_widget = QWidget()
        layout = QHBoxLayout(page_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # بخش فرم (سمت چپ)
        form_section = self.create_form_section()
        layout.addWidget(form_section, 1)
        
        # بخش لیست‌ها (سمت راست)
        list_section = self.main_window.robot_controller.create_lists_section_widget()
        layout.addWidget(list_section, 1)
        
        return page_widget
        
    def create_form_section(self):
        """بخش فرم ثبت نام"""
        form_frame = QFrame()
        form_frame.setStyleSheet(UIStyles.get_card_style())
        form_frame.setMinimumWidth(500)
        form_frame.setMaximumWidth(650)
        
        layout = QVBoxLayout(form_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # کنترل ربات
        self.main_window.robot_controller.create_robot_controls(layout)
        
        # فرم ثبت نام
        self.main_window.form_handler.create_applicant_form(layout)
        
        # دکمه‌های عملیات
        self.main_window.robot_controller.create_action_buttons(layout)
        
        # پنل SMS
        self.main_window.robot_controller.create_sms_panel(layout)
        
        return form_frame
        
    def create_marriage_loan_page(self):
        """صفحه ربات وام ازدواج - به زودی"""
        page_widget = QWidget()
        layout = QVBoxLayout(page_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)
        
        # کارت اصلی
        main_card = QFrame()
        main_card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {UIStyles.COLORS['accent_blue']}, 
                    stop:1 #667eea);
                border-radius: 20px;
                padding: 60px;
            }}
        """)
        main_card.setMaximumWidth(600)
        
        card_layout = QVBoxLayout(main_card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(20)
        
        # آیکن
        icon_label = QLabel("💍")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 64px; margin-bottom: 10px;")
        
        # عنوان
        title_label = QLabel("ربات وام ازدواج")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        
        # متن اصلی
        main_text = QLabel("به زودی در دسترس خواهد بود")
        main_text.setAlignment(Qt.AlignCenter)
        main_text.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 15px;
        """)
        
        # توضیحات
        desc_text = QLabel("تیم توسعه YARA در حال کار بر روی این ربات می‌باشد\nلطفاً تا تکمیل این بخش صبر کنید")
        desc_text.setAlignment(Qt.AlignCenter)
        desc_text.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 25px;
        """)
        
        # دکمه بازگشت
        back_btn = QPushButton("بازگشت به صفحه اصلی")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                padding: 12px 24px;
                border-radius: 25px;
                font-weight: 500;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
                border-color: rgba(255, 255, 255, 0.5);
            }
        """)
        back_btn.clicked.connect(lambda: self.main_window.switch_page("home"))
        
        card_layout.addWidget(icon_label)
        card_layout.addWidget(title_label)
        card_layout.addWidget(main_text)
        card_layout.addWidget(desc_text)
        card_layout.addWidget(back_btn)
        
        layout.addWidget(main_card)
        
        return page_widget#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QGroupBox)
from PyQt5.QtCore import Qt

class PageManager:
    def __init__(self, main_window):
        self.main_window = main_window
        
    def show_page(self, page_id):
        if page_id == "home":
            self.show_welcome_page()
        elif page_id == "child-loan":
            self.show_child_loan_page()
        elif page_id == "marriage-loan":
            self.show_marriage_coming_soon()
        else:
            self.show_simple_page(page_id)
            
    def show_welcome_page(self):
        if self.main_window.main_content:
            self.main_window.main_content.setParent(None)
            
        self.main_window.main_content = QWidget()
        self.main_window.main_area.setLayout(QVBoxLayout())
        self.main_window.main_area.layout().addWidget(self.main_window.main_content)
        
        layout = QVBoxLayout(self.main_window.main_content)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # فریم خوشامدگویی
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 15px;
                padding: 30px;
            }
        """)
        welcome_frame.setMaximumHeight(150)
        
        welcome_layout = QHBoxLayout(welcome_frame)
        welcome_layout.setAlignment(Qt.AlignCenter)
        
        title_part = QVBoxLayout()
        title_label = QLabel("به سیستم YARA خوش آمدید")
        title_label.setStyleSheet("""
            color: white; 
            font-size: 28px; 
            font-weight: bold;
            margin-bottom: 10px;
        """)
        
        subtitle_label = QLabel("ثبت نام خودکار در سایت‌های بانکی")
        subtitle_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9); 
            font-size: 16px;
        """)
        
        title_part.addWidget(title_label)
        title_part.addWidget(subtitle_label)
        welcome_layout.addLayout(title_part)
        
        # ویجت وضعیت ربات‌ها
        robot_status_frame = self.create_robot_status_widget()
        
        # ویجت آمار متقاضیان
        stats_frame = self.create_detailed_stats_widget()
        
        # ویجت وضعیت API ها
        api_status_frame = self.create_api_status_widget()
        
        # چیدمان صفحه
        layout.addWidget(welcome_frame)
        layout.addSpacing(20)
        
        # ردیف اول - وضعیت ربات‌ها و API ها
        first_row = QHBoxLayout()
        first_row.addWidget(robot_status_frame, 2)
        first_row.addWidget(api_status_frame, 1)
        layout.addLayout(first_row)
        
        layout.addSpacing(15)
        layout.addWidget(stats_frame)
        
    def create_robot_status_widget(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 10px;
                border: 1px solid #334155;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        
        # عنوان
        title = QLabel("🤖 وضعیت ربات‌ها")
        title.setStyleSheet("""
            color: #60A5FA;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
        """)
        layout.addWidget(title)
        
        # ربات وام فرزند
        child_robot_frame = QFrame()
        child_robot_frame.setStyleSheet("""
            QFrame {
                background-color: #334155;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }
        """)
        
        child_layout = QVBoxLayout(child_robot_frame)
        
        child_header = QHBoxLayout()
        child_title = QLabel("👶 ربات وام فرزند")
        child_title.setStyleSheet("color: #E2E8F0; font-weight: 500; font-size: 14px;")
        
        child_status = QLabel("● فعال")
        child_status.setStyleSheet("color: #10B981; font-weight: 500; font-size: 12px;")
        
        child_header.addWidget(child_title)
        child_header.addStretch()
        child_header.addWidget(child_status)
        
        child_info = QLabel("مهلت: 25 روز باقیمانده | نسخه: 2.1.0")
        child_info.setStyleSheet("color: #94A3B8; font-size: 11px; margin-top: 5px;")
        
        child_layout.addLayout(child_header)
        child_layout.addWidget(child_info)
        
        # ربات وام ازدواج
        marriage_robot_frame = QFrame()
        marriage_robot_frame.setStyleSheet("""
            QFrame {
                background-color: #334155;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        marriage_layout = QVBoxLayout(marriage_robot_frame)
        
        marriage_header = QHBoxLayout()
        marriage_title = QLabel("💍 ربات وام ازدواج")
        marriage_title.setStyleSheet("color: #E2E8F0; font-weight: 500; font-size: 14px;")
        
        marriage_status = QLabel("● در حال توسعه")
        marriage_status.setStyleSheet("color: #F59E0B; font-weight: 500; font-size: 12px;")
        
        marriage_header.addWidget(marriage_title)
        marriage_header.addStretch()
        marriage_header.addWidget(marriage_status)
        
        marriage_info = QLabel("تاریخ انتشار: تقریبی 2 هفته دیگر")
        marriage_info.setStyleSheet("color: #94A3B8; font-size: 11px; margin-top: 5px;")
        
        marriage_layout.addLayout(marriage_header)
        marriage_layout.addWidget(marriage_info)
        
        layout.addWidget(child_robot_frame)
        layout.addWidget(marriage_robot_frame)
        
        return frame
        
    def create_detailed_stats_widget(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 10px;
                border: 1px solid #334155;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        
        # عنوان
        title = QLabel("📊 آمار تفصیلی متقاضیان")
        title.setStyleSheet("""
            color: #60A5FA;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
        """)
        layout.addWidget(title)
        
        # دریافت آمار از دیتابیس
        try:
            stats = self.main_window.data_service.get_stats()
            
            # ردیف اول آمار
            first_row = QHBoxLayout()
            
            stat_items_row1 = [
                ("📈", "کل متقاضیان", str(stats.get('total_count', 0)), "#3B82F6"),
                ("⏳", "در انتظار", str(stats.get('pending_count', 0)), "#F59E0B"),
                ("🔄", "در حال پردازش", str(stats.get('processing_count', 0)), "#8B5CF6"),
                ("✅", "تکمیل شده", str(stats.get('completed_count', 0)), "#10B981")
            ]
            
            for icon, label, value, color in stat_items_row1:
                stat_widget = self.create_enhanced_stat_widget(icon, label, value, color)
                first_row.addWidget(stat_widget)
            
            # ردیف دوم آمار
            second_row = QHBoxLayout()
            
            stat_items_row2 = [
                ("❌", "ناموفق", str(stats.get('failed_count', 0)), "#EF4444"),
                ("📅", "امروز", str(stats.get('today_count', 0)), "#06B6D4"),
                ("📆", "این هفته", str(stats.get('week_count', 0)), "#84CC16"),
                ("🗓️", "این ماه", str(stats.get('month_count', 0)), "#F97316")
            ]
            
            for icon, label, value, color in stat_items_row2:
                stat_widget = self.create_enhanced_stat_widget(icon, label, value, color)
                second_row.addWidget(stat_widget)
                
            # اضافه کردن نرخ موفقیت
            success_rate = stats.get('success_rate', 0)
            success_frame = QFrame()
            success_frame.setStyleSheet("""
                QFrame {
                    background-color: #334155;
                    border-radius: 8px;
                    padding: 10px;
                    margin-top: 10px;
                }
            """)
            success_layout = QHBoxLayout(success_frame)
            
            success_label = QLabel("🎯 نرخ موفقیت:")
            success_label.setStyleSheet("color: #E2E8F0; font-size: 14px; font-weight: 500;")
            
            success_value = QLabel(f"{success_rate}%")
            success_value.setStyleSheet("color: #10B981; font-size: 16px; font-weight: bold;")
            
            # Progress bar برای نرخ موفقیت
            progress_container = QFrame()
            progress_container.setFixedHeight(6)
            progress_container.setStyleSheet("""
                QFrame {
                    background-color: #4B5563;
                    border-radius: 3px;
                }
            """)
            
            success_layout.addWidget(success_label)
            success_layout.addWidget(success_value)
            success_layout.addStretch()
            
            layout.addLayout(first_row)
            layout.addSpacing(10)
            layout.addLayout(second_row)
            layout.addWidget(success_frame)
            
        except Exception as e:
            error_label = QLabel(f"خطا در بارگذاری آمار: {str(e)}")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("color: #EF4444; font-size: 14px;")
            layout.addWidget(error_label)
            
        return frame
        
    def create_enhanced_stat_widget(self, icon, label, value, color):
        widget = QFrame()
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: #334155;
                border-radius: 8px;
                border-left: 3px solid {color};
                padding: 12px;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(5)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 20px; margin-bottom: 3px;")
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"""
            color: {color}; 
            font-size: 20px; 
            font-weight: bold;
        """)
        
        label_label = QLabel(label)
        label_label.setAlignment(Qt.AlignCenter)
        label_label.setStyleSheet("""
            color: #94A3B8; 
            font-size: 11px;
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(label_label)
        
        return widget
        
    def create_api_status_widget(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 10px;
                border: 1px solid #334155;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        
        # عنوان
        title = QLabel("🔗 وضعیت API ها")
        title.setStyleSheet("""
            color: #60A5FA;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
        """)
        layout.addWidget(title)
        
        # لیست API ها
        apis = [
            ("SMS Forwarder", "● متصل", "#10B981"),
            ("2Captcha", "● متصل", "#10B981"),
            ("Database", "● متصل", "#10B981"),
            ("Selenium", "○ قطع", "#EF4444")
        ]
        
        for api_name, status, color in apis:
            api_frame = QFrame()
            api_frame.setStyleSheet("""
                QFrame {
                    background-color: #334155;
                    border-radius: 6px;
                    padding: 10px;
                    margin-bottom: 8px;
                }
            """)
            
            api_layout = QHBoxLayout(api_frame)
            
            name_label = QLabel(api_name)
            name_label.setStyleSheet("color: #E2E8F0; font-size: 12px;")
            
            status_label = QLabel(status)
            status_label.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: 500;")
            
            api_layout.addWidget(name_label)
            api_layout.addStretch()
            api_layout.addWidget(status_label)
            
            layout.addWidget(api_frame)
            
        return frame
        
    def create_stat_widget(self, icon, label, value):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #334155;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px; margin-bottom: 5px;")
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("""
            color: #60A5FA; 
            font-size: 24px; 
            font-weight: bold;
        """)
        
        label_label = QLabel(label)
        label_label.setAlignment(Qt.AlignCenter)
        label_label.setStyleSheet("""
            color: #94A3B8; 
            font-size: 12px;
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(label_label)
        
        return widget
        
    def show_child_loan_page(self):
        if self.main_window.main_content:
            self.main_window.main_content.setParent(None)
            
        self.main_window.main_content = QWidget()
        self.main_window.main_area.setLayout(QVBoxLayout())
        self.main_window.main_area.layout().addWidget(self.main_window.main_content)
        
        main_layout = QHBoxLayout(self.main_window.main_content)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # بخش فرم
        self.create_form_section(main_layout)
        
        # بخش لیست‌ها
        self.main_window.robot_controller.create_lists_section(main_layout)
        
    def create_form_section(self, parent_layout):
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 10px;
                border: 1px solid #334155;
            }
        """)
        form_frame.setMinimumWidth(500)
        form_frame.setMaximumWidth(600)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # کنترل ربات
        self.main_window.robot_controller.create_robot_controls(form_layout)
        
        # فرم ثبت نام
        self.main_window.form_handler.create_applicant_form(form_layout)
        
        # دکمه‌های عملیات
        self.main_window.robot_controller.create_action_buttons(form_layout)
        
        # پنل SMS
        self.main_window.robot_controller.create_sms_panel(form_layout)
        
        parent_layout.addWidget(form_frame)
        
    def show_marriage_coming_soon(self):
        if self.main_window.main_content:
            self.main_window.main_content.setParent(None)
            
        self.main_window.main_content = QWidget()
        self.main_window.main_area.setLayout(QVBoxLayout())
        self.main_window.main_area.layout().addWidget(self.main_window.main_content)
        
        layout = QVBoxLayout(self.main_window.main_content)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)
        
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 20px;
                padding: 60px;
            }
        """)
        
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setAlignment(Qt.AlignCenter)
        frame_layout.setSpacing(25)
        
        icon_label = QLabel("💍")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 72px; margin-bottom: 20px;")
        
        title_label = QLabel("ربات وام ازدواج")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: white; 
            font-size: 36px; 
            font-weight: bold;
            margin-bottom: 15px;
        """)
        
        main_text = QLabel("به زودی در دسترس خواهد بود")
        main_text.setAlignment(Qt.AlignCenter)
        main_text.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9); 
            font-size: 22px;
            font-weight: 500;
            margin-bottom: 20px;
        """)
        
        description_text = QLabel("تیم توسعه YARA در حال کار بر روی این ربات می‌باشد\nلطفاً تا تکمیل این بخش صبر کنید")
        description_text.setAlignment(Qt.AlignCenter)
        description_text.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8); 
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 30px;
        """)
        
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
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border-color: rgba(255, 255, 255, 0.5);
            }
        """)
        back_button.clicked.connect(lambda: self.main_window.switch_page("home"))
        
        frame_layout.addWidget(icon_label)
        frame_layout.addWidget(title_label)
        frame_layout.addWidget(main_text)
        frame_layout.addWidget(description_text)
        frame_layout.addWidget(back_button)
        
        layout.addWidget(main_frame)
        
    def show_simple_page(self, page_id):
        if self.main_window.main_content:
            self.main_window.main_content.setParent(None)
            
        self.main_window.main_content = QWidget()
        self.main_window.main_area.setLayout(QVBoxLayout())
        self.main_window.main_area.layout().addWidget(self.main_window.main_content)
        
        layout = QVBoxLayout(self.main_window.main_content)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)
        
        page_names = {
            "settings": ("⚙️", "تنظیمات"),
            "education": ("📚", "آموزش")
        }
        
        icon, title = page_names.get(page_id, ("📄", "صفحه"))
        
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 64px; margin-bottom: 20px;")
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #E2E8F0; 
            font-size: 32px; 
            font-weight: bold;
            margin-bottom: 10px;
        """)
        
        subtitle_label = QLabel("این بخش در حال توسعه است")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            color: #94A3B8; 
            font-size: 16px;
        """)
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        layout.addWidget(title_frame)