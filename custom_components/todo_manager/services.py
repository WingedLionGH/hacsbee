"""Services for ToDo Manager."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any
import uuid

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    SERVICE_CREATE_TODO,
    SERVICE_UPDATE_TODO,
    SERVICE_DELETE_TODO,
    SERVICE_COMPLETE_TODO,
    SERVICE_CREATE_PERSON,
    SERVICE_UPDATE_PERSON,
    SERVICE_DELETE_PERSON,
    ATTR_TODO_ID,
    ATTR_TITLE,
    ATTR_DESCRIPTION,
    ATTR_DUE_DATE,
    ATTR_DUE_TIME,
    ATTR_TODO_TYPE,
    ATTR_PERSONS,
    ATTR_RECURRING,
    ATTR_RECURRING_RULE,
    ATTR_RESULT,
    ATTR_ITEMS,
    ATTR_ITEM_NAME,
    ATTR_ITEM_QUANTITY,
    ATTR_PERSON_ID,
    ATTR_PERSON_NAME,
    ATTR_PERSON_COLOR,
    TODO_TYPE_SIMPLE,
    TODO_TYPE_COMPLEX,
    TODO_TYPE_SHOPPING,
    TODO_TYPE_PACKING,
)

_LOGGER = logging.getLogger(__name__)

# Service schemas
CREATE_TODO_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TITLE): cv.string,
        vol.Optional(ATTR_DESCRIPTION): cv.string,
        vol.Optional(ATTR_DUE_DATE): cv.string,
        vol.Optional(ATTR_DUE_TIME, default="23:59"): cv.string,
        vol.Optional(ATTR_TODO_TYPE, default=TODO_TYPE_SIMPLE): vol.In(
            [TODO_TYPE_SIMPLE, TODO_TYPE_COMPLEX, TODO_TYPE_SHOPPING, TODO_TYPE_PACKING]
        ),
        vol.Optional(ATTR_PERSONS, default=[]): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(ATTR_RECURRING, default=False): cv.boolean,
        vol.Optional(ATTR_RECURRING_RULE): vol.Schema({
            vol.Required("interval"): vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Required("unit"): vol.In(["days", "weeks", "months"]),
        }),
        vol.Optional(ATTR_ITEMS, default=[]): vol.All(cv.ensure_list),
    }
)

UPDATE_TODO_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TODO_ID): cv.string,
        vol.Optional(ATTR_TITLE): cv.string,
        vol.Optional(ATTR_DESCRIPTION): cv.string,
        vol.Optional(ATTR_DUE_DATE): cv.string,
        vol.Optional(ATTR_DUE_TIME): cv.string,
        vol.Optional(ATTR_TODO_TYPE): vol.In(
            [TODO_TYPE_SIMPLE, TODO_TYPE_COMPLEX, TODO_TYPE_SHOPPING, TODO_TYPE_PACKING]
        ),
        vol.Optional(ATTR_PERSONS): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(ATTR_RECURRING): cv.boolean,
        vol.Optional(ATTR_RECURRING_RULE): vol.Schema({
            vol.Required("interval"): vol.All(vol.Coerce(int), vol.Range(min=1)),
            vol.Required("unit"): vol.In(["days", "weeks", "months"]),
        }),
        vol.Optional(ATTR_RESULT): cv.string,
        vol.Optional(ATTR_ITEMS): vol.All(cv.ensure_list),
    }
)

DELETE_TODO_SCHEMA = vol.Schema({vol.Required(ATTR_TODO_ID): cv.string})

COMPLETE_TODO_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TODO_ID): cv.string,
        vol.Optional(ATTR_RESULT): cv.string,
    }
)

TOGGLE_ITEM_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TODO_ID): cv.string,
        vol.Required(ATTR_ITEM_ID): cv.string,
    }
)

CREATE_PERSON_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_PERSON_NAME): cv.string,
        vol.Optional(ATTR_PERSON_COLOR, default="#1976d2"): cv.string,
    }
)

UPDATE_PERSON_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_PERSON_ID): cv.string,
        vol.Optional(ATTR_PERSON_NAME): cv.string,
        vol.Optional(ATTR_PERSON_COLOR): cv.string,
    }
)

DELETE_PERSON_SCHEMA = vol.Schema({vol.Required(ATTR_PERSON_ID): cv.string})


def get_coordinator(hass: HomeAssistant) -> Any:
    """Get the coordinator from hass data."""
    from .coordinator import TodoCoordinator
    
    # Find the coordinator in hass.data
    domain_data = hass.data.get(DOMAIN, {})
    
    # Try to get from config entry first
    config_entries = hass.config_entries.async_entries(DOMAIN)
    if config_entries:
        coordinator = domain_data.get(config_entries[0].entry_id)
        if isinstance(coordinator, TodoCoordinator):
            return coordinator
    
    # Fallback: find any coordinator
    for key, value in domain_data.items():
        if isinstance(value, TodoCoordinator):
            return value
    
    return None


@callback
async def async_create_todo_service(service: ServiceCall) -> None:
    """Handle create todo service call."""
    coordinator = get_coordinator(service.hass)
    if not coordinator:
        _LOGGER.error("Coordinator not found")
        return

    todo_id = str(uuid.uuid4())
    todo_data = {
        "id": todo_id,
        "title": service.data[ATTR_TITLE],
        "description": service.data.get(ATTR_DESCRIPTION, ""),
        "due_date": service.data.get(ATTR_DUE_DATE),
        "due_time": service.data.get(ATTR_DUE_TIME, "23:59"),
        "todo_type": service.data.get(ATTR_TODO_TYPE, TODO_TYPE_SIMPLE),
        "persons": service.data.get(ATTR_PERSONS, []),
        "recurring": service.data.get(ATTR_RECURRING, False),
        "recurring_rule": service.data.get(ATTR_RECURRING_RULE),
        "completed": False,
        "completed_date": None,
        "result": None,
        "items": service.data.get(ATTR_ITEMS, []),
        "created_at": datetime.now().isoformat(),
    }
    
    # Initialize items for shopping and packing lists
    if todo_data["todo_type"] in [TODO_TYPE_SHOPPING, TODO_TYPE_PACKING]:
        if not todo_data["items"]:
            todo_data["items"] = []
        else:
            # Ensure items have the right structure
            formatted_items = []
            for item in todo_data["items"]:
                if isinstance(item, dict):
                    formatted_items.append({
                        "id": item.get("id", str(uuid.uuid4())),
                        "name": item.get("name", item.get(ATTR_ITEM_NAME, "")),
                        "quantity": item.get("quantity", item.get(ATTR_ITEM_QUANTITY, "")),
                        "checked": item.get("checked", False),
                    })
                else:
                    formatted_items.append({
                        "id": str(uuid.uuid4()),
                        "name": str(item),
                        "quantity": "",
                        "checked": False,
                    })
            todo_data["items"] = formatted_items
    
    coordinator.todos[todo_id] = todo_data
    await coordinator.async_save_data()
    _LOGGER.info("Created todo: %s", todo_data["title"])


@callback
async def async_update_todo_service(service: ServiceCall) -> None:
    """Handle update todo service call."""
    coordinator = get_coordinator(service.hass)
    if not coordinator:
        _LOGGER.error("Coordinator not found")
        return

    todo_id = service.data[ATTR_TODO_ID]
    todo = coordinator.todos.get(todo_id)
    if not todo:
        _LOGGER.error("Todo not found: %s", todo_id)
        return

    # Update allowed fields
    if ATTR_TITLE in service.data:
        todo["title"] = service.data[ATTR_TITLE]
    if ATTR_DESCRIPTION in service.data:
        todo["description"] = service.data[ATTR_DESCRIPTION]
    if ATTR_DUE_DATE in service.data:
        todo["due_date"] = service.data[ATTR_DUE_DATE]
    if ATTR_DUE_TIME in service.data:
        todo["due_time"] = service.data[ATTR_DUE_TIME]
    if ATTR_TODO_TYPE in service.data:
        todo["todo_type"] = service.data[ATTR_TODO_TYPE]
    if ATTR_PERSONS in service.data:
        todo["persons"] = service.data[ATTR_PERSONS]
    if ATTR_RECURRING in service.data:
        todo["recurring"] = service.data[ATTR_RECURRING]
    if ATTR_RECURRING_RULE in service.data:
        todo["recurring_rule"] = service.data[ATTR_RECURRING_RULE]
    if ATTR_RESULT in service.data:
        todo["result"] = service.data[ATTR_RESULT]
    if ATTR_ITEMS in service.data:
        todo["items"] = service.data[ATTR_ITEMS]
    if "completed" in service.data:
        todo["completed"] = service.data["completed"]
        if not service.data["completed"]:
            todo["completed_date"] = None

    await coordinator.async_save_data()
    _LOGGER.info("Updated todo: %s", todo_id)


@callback
async def async_delete_todo_service(service: ServiceCall) -> None:
    """Handle delete todo service call."""
    coordinator = get_coordinator(service.hass)
    if not coordinator:
        _LOGGER.error("Coordinator not found")
        return

    todo_id = service.data[ATTR_TODO_ID]
    if todo_id in coordinator.todos:
        del coordinator.todos[todo_id]
        await coordinator.async_save_data()
        _LOGGER.info("Deleted todo: %s", todo_id)
    else:
        _LOGGER.error("Todo not found: %s", todo_id)


@callback
async def async_complete_todo_service(service: ServiceCall) -> None:
    """Handle complete todo service call."""
    coordinator = get_coordinator(service.hass)
    if not coordinator:
        _LOGGER.error("Coordinator not found")
        return

    todo_id = service.data[ATTR_TODO_ID]
    todo = coordinator.todos.get(todo_id)
    if not todo:
        _LOGGER.error("Todo not found: %s", todo_id)
        return

    # Toggle completion
    was_completed = todo.get("completed", False)
    todo["completed"] = not was_completed
    
    if todo["completed"]:
        todo["completed_date"] = datetime.now().isoformat()
        if ATTR_RESULT in service.data:
            todo["result"] = service.data[ATTR_RESULT]
    else:
        todo["completed_date"] = None

    await coordinator.async_save_data()
    _LOGGER.info("Completed todo: %s", todo_id)


@callback
async def async_toggle_item_service(service: ServiceCall) -> None:
    """Handle toggle item service call."""
    coordinator = get_coordinator(service.hass)
    if not coordinator:
        _LOGGER.error("Coordinator not found")
        return

    todo_id = service.data[ATTR_TODO_ID]
    item_id = service.data[ATTR_ITEM_ID]
    
    todo = coordinator.todos.get(todo_id)
    if not todo:
        _LOGGER.error("Todo not found: %s", todo_id)
        return

    items = todo.get("items", [])
    item = next((i for i in items if i.get("id") == item_id), None)
    
    if not item:
        _LOGGER.error("Item not found: %s in todo %s", item_id, todo_id)
        return

    item["checked"] = not item.get("checked", False)
    await coordinator.async_save_data()
    _LOGGER.info("Toggled item %s in todo %s", item_id, todo_id)


@callback
async def async_create_person_service(service: ServiceCall) -> None:
    """Handle create person service call."""
    coordinator = get_coordinator(service.hass)
    if not coordinator:
        _LOGGER.error("Coordinator not found")
        return

    person_id = str(uuid.uuid4())
    person_data = {
        "id": person_id,
        "name": service.data[ATTR_PERSON_NAME],
        "color": service.data.get(ATTR_PERSON_COLOR, "#1976d2"),
    }

    coordinator.persons[person_id] = person_data
    await coordinator.async_save_data()
    _LOGGER.info("Created person: %s", person_data["name"])


@callback
async def async_update_person_service(service: ServiceCall) -> None:
    """Handle update person service call."""
    coordinator = get_coordinator(service.hass)
    if not coordinator:
        _LOGGER.error("Coordinator not found")
        return

    person_id = service.data[ATTR_PERSON_ID]
    person = coordinator.persons.get(person_id)
    if not person:
        _LOGGER.error("Person not found: %s", person_id)
        return

    if ATTR_PERSON_NAME in service.data:
        person["name"] = service.data[ATTR_PERSON_NAME]
    if ATTR_PERSON_COLOR in service.data:
        person["color"] = service.data[ATTR_PERSON_COLOR]

    await coordinator.async_save_data()
    _LOGGER.info("Updated person: %s", person_id)


@callback
async def async_delete_person_service(service: ServiceCall) -> None:
    """Handle delete person service call."""
    coordinator = get_coordinator(service.hass)
    if not coordinator:
        _LOGGER.error("Coordinator not found")
        return

    person_id = service.data[ATTR_PERSON_ID]
    if person_id in coordinator.persons:
        # Remove person from all todos
        for todo in coordinator.todos.values():
            if person_id in todo.get("persons", []):
                todo["persons"].remove(person_id)
        
        del coordinator.persons[person_id]
        await coordinator.async_save_data()
        _LOGGER.info("Deleted person: %s", person_id)
    else:
        _LOGGER.error("Person not found: %s", person_id)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for ToDo Manager."""
    hass.services.async_register(
        DOMAIN, SERVICE_CREATE_TODO, async_create_todo_service, schema=CREATE_TODO_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_UPDATE_TODO, async_update_todo_service, schema=UPDATE_TODO_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_DELETE_TODO, async_delete_todo_service, schema=DELETE_TODO_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_COMPLETE_TODO, async_complete_todo_service, schema=COMPLETE_TODO_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_TOGGLE_ITEM, async_toggle_item_service, schema=TOGGLE_ITEM_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_CREATE_PERSON, async_create_person_service, schema=CREATE_PERSON_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_UPDATE_PERSON, async_update_person_service, schema=UPDATE_PERSON_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_DELETE_PERSON, async_delete_person_service, schema=DELETE_PERSON_SCHEMA
    )
