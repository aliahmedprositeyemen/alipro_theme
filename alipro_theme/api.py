
import frappe
import json


@frappe.whitelist(allow_guest=True)
def get_theme_settings():
	"""
	Fetch Alipro Setting for frontend.
	Allows guest access for login page theming.
	"""
	return frappe.get_single("Alipro Setting")


@frappe.whitelist()
def _apply_customizations(data):
	"""
	Apply customizations for a single doctype (Property Setters, Custom Fields, Client Scripts).
	Performs upsert logic – inserts if missing, updates if existing.
	"""
	if isinstance(data, str):
		data = json.loads(data)

	doctype = data.get("doctype")
	if not doctype:
		return

	# --- Property Setters ---
	for ps in data.get("property_setters", []):
		ps_name = ps.get("name")
		if not ps_name:
			continue
		if frappe.db.exists("Property Setter", ps_name):
			doc = frappe.get_doc("Property Setter", ps_name)
			doc.update(ps)
			doc.save(ignore_permissions=True)
		else:
			ps_doc = frappe.get_doc(ps)
			ps_doc.insert(ignore_permissions=True)

	# --- Custom Fields ---
	for cf in data.get("custom_fields", []):
		cf_name = cf.get("name")
		if not cf_name:
			continue
		if frappe.db.exists("Custom Field", cf_name):
			doc = frappe.get_doc("Custom Field", cf_name)
			doc.update(cf)
			doc.save(ignore_permissions=True)
		else:
			cf_doc = frappe.get_doc(cf)
			cf_doc.insert(ignore_permissions=True)

	# --- Client Scripts ---
	for cs in data.get("client_scripts", []):
		cs_name = cs.get("name")
		if not cs_name:
			continue
		if frappe.db.exists("Client Script", cs_name):
			doc = frappe.get_doc("Client Script", cs_name)
			doc.update(cs)
			doc.save(ignore_permissions=True)
		else:
			cs_doc = frappe.get_doc(cs)
			cs_doc.insert(ignore_permissions=True)

	frappe.clear_cache(doctype=doctype)
	return doctype


@frappe.whitelist()
def export_multiple_customizations(doctypes, with_permissions=0):
	"""
	Export customizations (Property Setters, Custom Fields, Client Scripts)
	for multiple doctypes. Returns a JSON string.
	"""
	if isinstance(doctypes, str):
		doctypes = json.loads(doctypes)

	data = {}
	for entry in doctypes:
		dt = entry.get("doctype_name")
		if not dt:
			continue

		custom_data = {
			"doctype": dt,
			"property_setters": frappe.get_all(
				"Property Setter",
				filters={"doc_type": dt},
				fields="*",
			),
			"custom_fields": frappe.get_all(
				"Custom Field",
				filters={"dt": dt},
				fields="*",
			),
			"client_scripts": frappe.get_all(
				"Client Script",
				filters={"dt": dt},
				fields="*",
			),
		}

		if int(with_permissions):
			custom_data["permissions"] = frappe.get_all(
				"Custom DocPerm",
				filters={"parent": dt},
				fields="*",
			)

		data[dt] = custom_data

	return json.dumps(data, indent=2, default=str)


@frappe.whitelist()
def import_multiple_customizations(file_url):
	"""
	Import customizations from an uploaded JSON file (by file_url).
	"""
	try:
		file_doc = frappe.get_doc("File", {"file_url": file_url})
		content = file_doc.get_content()
		data = json.loads(content)

		if not isinstance(data, dict):
			frappe.throw("Invalid JSON format. Expected a dict of doctypes.")

		imported = []
		errors = []

		for doctype_name, custom_data in data.items():
			try:
				_apply_customizations(custom_data)
				imported.append(doctype_name)
			except Exception as e:
				errors.append(f"{doctype_name}: {e}")

		return {
			"status": "completed",
			"imported": imported,
			"errors": errors,
			"message": f"Imported {len(imported)} doctypes. Errors: {len(errors)}.",
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Import Multiple Customizations Error")
		frappe.throw(f"Failed to import customizations: {e}")
