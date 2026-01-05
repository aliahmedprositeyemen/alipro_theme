import re
from frappe.model.document import Document

class AliproSetting(Document):
	def before_save(self):
		if self.login_page_title is not None:
			extra_spaces = re.search(r'^\s+', self.login_page_title)
			if extra_spaces:
				self.login_page_title=''
			else:
				pass
