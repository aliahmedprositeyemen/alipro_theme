import json

with open("alipro_setting.json", "r") as f:
    data = json.load(f)

new_tabs = [
    # Sidebar
    {"fieldname": "sidebar_tab", "fieldtype": "Tab Break", "label": "Sidebar (Workspace)"},
    {"fieldname": "sidebar_section", "fieldtype": "Section Break", "label": "Sidebar Colors"},
    {"fieldname": "sidebar_background_color", "fieldtype": "Color", "label": "Background Color"},
    {"fieldname": "sidebar_text_color", "fieldtype": "Color", "label": "Text Color"},
    {"fieldname": "sidebar_active_background_color", "fieldtype": "Color", "label": "Active Background Color"},
    {"fieldname": "sidebar_active_text_color", "fieldtype": "Color", "label": "Active Text Color"},
    
    # Page Head
    {"fieldname": "page_head_tab", "fieldtype": "Tab Break", "label": "Page Head"},
    {"fieldname": "page_head_section", "fieldtype": "Section Break", "label": "Page Head Colors"},
    {"fieldname": "page_head_background_color", "fieldtype": "Color", "label": "Background Color"},
    {"fieldname": "page_head_text_color", "fieldtype": "Color", "label": "Text Color"},
    
    # Modal
    {"fieldname": "modal_tab", "fieldtype": "Tab Break", "label": "Modals & Dialogs"},
    {"fieldname": "modal_section", "fieldtype": "Section Break", "label": "Modal Colors"},
    {"fieldname": "modal_background_color", "fieldtype": "Color", "label": "Background Color"},
    {"fieldname": "modal_text_color", "fieldtype": "Color", "label": "Text Color"},
    {"fieldname": "modal_header_background_color", "fieldtype": "Color", "label": "Header Background Color"},
    
    # Dropdown
    {"fieldname": "dropdown_tab", "fieldtype": "Tab Break", "label": "Dropdown & Menus"},
    {"fieldname": "dropdown_section", "fieldtype": "Section Break", "label": "Dropdown Colors"},
    {"fieldname": "dropdown_background_color", "fieldtype": "Color", "label": "Background Color"},
    {"fieldname": "dropdown_text_color", "fieldtype": "Color", "label": "Text Color"},
    {"fieldname": "dropdown_hover_background_color", "fieldtype": "Color", "label": "Hover Background Color"}
]

# Append new fields
for f in new_tabs:
    # Ensure no duplicates
    if not any(existing.get("fieldname") == f["fieldname"] for existing in data["fields"]):
        data["fields"].append(f)
        data["field_order"].append(f["fieldname"])

with open("alipro_setting.json", "w") as f:
    json.dump(data, f, indent=1)

print("JSON updated successfully")
