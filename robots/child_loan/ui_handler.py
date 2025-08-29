#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ChildLoanUIHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        
    def create_interface(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        label = QLabel("ربات وام فرزند - در حال توسعه")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; color: #2d3748;")
        
        layout.addWidget(label)
        return widget
        
    def update_status(self, message):
        pass
        
    def show_sms_panel(self):
        pass
        
    def on_robot_completed(self, success):
        pass