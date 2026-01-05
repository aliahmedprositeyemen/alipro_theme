
import frappe
import os
from frappe.model.document import Document

class AliproSetting(Document):
	def on_update(self):
		self.generate_css()

	def generate_css(self):
		css = ""
		
		# Navbar
		if self.navbar_color:
			css += f".navbar {{ background-color: {self.navbar_color} !important; }}\n"
		if self.navbar_text_color:
			css += f".navbar .navbar-nav .nav-link, .navbar .navbar-brand {{ color: {self.navbar_text_color} !important; }}\n"
			
		# Primary Button
		if self.button_background_color:
			css += f".btn-primary {{ background-color: {self.button_background_color} !important; border-color: {self.button_background_color} !important; }}\n"
		if self.button_text_color:
			css += f".btn-primary {{ color: {self.button_text_color} !important; }}\n"
		if self.button_hover_background_color:
			css += f".btn-primary:hover {{ background-color: {self.button_hover_background_color} !important; border-color: {self.button_hover_background_color} !important; }}\n"
		if self.button_hover_text_color:
			css += f".btn-primary:hover {{ color: {self.button_hover_text_color} !important; }}\n"

		# Secondary Button (assuming btn-default or similar)
		if self.secondary_button_background_color:
			css += f".btn-default {{ background-color: {self.secondary_button_background_color} !important; }}\n"
		if self.secondary_button_text_color:
			css += f".btn-default {{ color: {self.secondary_button_text_color} !important; }}\n"
			
		# Login Page
		if self.login_page_background_color: # Assuming page_background_type is checked in JS or redundant here
			css += f".login-page {{ background-color: {self.login_page_background_color} !important; }}\n"
		if self.login_button_background_color:
			css += f".login-page .btn-primary {{ background-color: {self.login_button_background_color} !important; border-color: {self.login_button_background_color} !important; }}\n"
		if self.login_button_text_color:
			css += f".login-page .btn-primary {{ color: {self.login_button_text_color} !important; }}\n"

		# Main Body
		if self.body_background_color:
			css += f"body {{ background-color: {self.body_background_color} !important; }}\n"
		if self.main_body_content_box_background_color:
			css += f".page-container {{ background-color: {self.main_body_content_box_background_color} !important; }}\n"

		# Tables
		if self.table_head_background_color:
			css += f".table thead th {{ background-color: {self.table_head_background_color} !important; }}\n"
		if self.table_head_text_color:
			css += f".table thead th {{ color: {self.table_head_text_color} !important; }}\n"
		if self.table_body_background_color:
			css += f".table tbody td {{ background-color: {self.table_body_background_color} !important; }}\n"
		if self.table_body_text_color:
			css += f".table tbody td {{ color: {self.table_body_text_color} !important; }}\n"

		# Inputs
		if self.input_background_color:
			css += f".form-control {{ background-color: {self.input_background_color} !important; }}\n"
		if self.input_text_color:
			css += f".form-control {{ color: {self.input_text_color} !important; }}\n"
		if self.input_border_color:
			css += f".form-control {{ border-color: {self.input_border_color} !important; }}\n"
		if self.input_label_color:
			css += f".form-group label {{ color: {self.input_label_color} !important; }}\n"

		# Widgets / Number Cards
		if self.number_card_background_color:
			css += f".widget {{ background-color: {self.number_card_background_color} !important; }}\n"
		if self.number_card_text_color:
			css += f".widget {{ color: {self.number_card_text_color} !important; }}\n"
			
		# Write to file
		path = frappe.get_app_path("alipro_theme", "public/css/alipro_dynamic.css")
		with open(path, "w") as f:
			f.write(css)

