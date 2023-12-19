from . import __version__ as app_version

app_name = "shift_rotation"
app_title = "Shift Rotation"
app_publisher = "preciholesports"
app_description = "Many businesses have operations and business hours that require staffing outside of a traditional 9 a.m. to 5 p.m. schedule. These organizations often use rotating shifts to meet their staffing demands. These shifts allow employees to learn about different facets of the business while helping employers meet production or service goals."
app_email = "azhar@preciholesports.com"
app_license = "MIT"

# Includes in <head>
# ------------------
doctype_js = {
    "Shift Request" : "public/js/shift_request.js"
}
# include js, css files in header of desk.html
# app_include_css = "/assets/shift_rotation/css/shift_rotation.css"
# app_include_js = "/assets/shift_rotation/js/shift_rotation.js"

# include js, css files in header of web template
# web_include_css = "/assets/shift_rotation/css/shift_rotation.css"
# web_include_js = "/assets/shift_rotation/js/shift_rotation.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "shift_rotation/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "shift_rotation.utils.jinja_methods",
#	"filters": "shift_rotation.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "shift_rotation.install.before_install"
# after_install = "shift_rotation.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "shift_rotation.uninstall.before_uninstall"
# after_uninstall = "shift_rotation.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "shift_rotation.utils.before_app_install"
# after_app_install = "shift_rotation.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "shift_rotation.utils.before_app_uninstall"
# after_app_uninstall = "shift_rotation.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "shift_rotation.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Shift Request": {
		"before_insert": "shift_rotation.public.py.shift_request.adjust_shift_dates",
        "on_submit": "shift_rotation.public.py.shift_request.handle_shift_switching",
        "on_cancel": "shift_rotation.public.py.shift_request.revert_shift_change"
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"shift_rotation.tasks.all"
#	],
#	"daily": [
#		"shift_rotation.tasks.daily"
#	],
#	"hourly": [
#		"shift_rotation.tasks.hourly"
#	],
#	"weekly": [
#		"shift_rotation.tasks.weekly"
#	],
#	"monthly": [
#		"shift_rotation.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "shift_rotation.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "shift_rotation.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "shift_rotation.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["shift_rotation.utils.before_request"]
# after_request = ["shift_rotation.utils.after_request"]

# Job Events
# ----------
# before_job = ["shift_rotation.utils.before_job"]
# after_job = ["shift_rotation.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"shift_rotation.auth.validate"
# ]
fixtures = [
	{"dt": "Custom Field", "filters": [["module", "=", "Shift Rotation"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Shift Rotation"]]},
]