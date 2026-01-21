"""Constants for the ToDo Manager integration."""

DOMAIN = "todo_manager"
DATA_COORDINATOR = "coordinator"
DATA_STORAGE = "storage"

# Service names
SERVICE_CREATE_TODO = "create_todo"
SERVICE_UPDATE_TODO = "update_todo"
SERVICE_DELETE_TODO = "delete_todo"
SERVICE_COMPLETE_TODO = "complete_todo"
SERVICE_TOGGLE_ITEM = "toggle_item"
SERVICE_CREATE_PERSON = "create_person"
SERVICE_UPDATE_PERSON = "update_person"
SERVICE_DELETE_PERSON = "delete_person"

# ToDo types
TODO_TYPE_SIMPLE = "simple"
TODO_TYPE_COMPLEX = "complex"
TODO_TYPE_SHOPPING = "shopping"
TODO_TYPE_PACKING = "packing"

# Storage keys
STORAGE_KEY_TODOS = "todos"
STORAGE_KEY_PERSONS = "persons"
STORAGE_VERSION = 1

# Attributes
ATTR_TODO_ID = "todo_id"
ATTR_TITLE = "title"
ATTR_DESCRIPTION = "description"
ATTR_DUE_DATE = "due_date"
ATTR_DUE_TIME = "due_time"
ATTR_TODO_TYPE = "todo_type"
ATTR_PERSONS = "persons"
ATTR_RECURRING = "recurring"
ATTR_RECURRING_RULE = "recurring_rule"
ATTR_COMPLETED = "completed"
ATTR_COMPLETED_DATE = "completed_date"
ATTR_RESULT = "result"
ATTR_ITEMS = "items"
ATTR_ITEM_ID = "item_id"
ATTR_ITEM_NAME = "item_name"
ATTR_ITEM_QUANTITY = "item_quantity"
ATTR_ITEM_CHECKED = "item_checked"
ATTR_PERSON_ID = "person_id"
ATTR_PERSON_NAME = "person_name"
ATTR_PERSON_COLOR = "person_color"

# Default values
DEFAULT_TODO_TYPE = TODO_TYPE_SIMPLE
DEFAULT_RECURRING = False
