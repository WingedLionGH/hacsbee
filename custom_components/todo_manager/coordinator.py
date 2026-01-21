"""Data coordinator for ToDo Manager."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any
import uuid

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import storage
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from .const import (
    DOMAIN,
    STORAGE_KEY_TODOS,
    STORAGE_KEY_PERSONS,
    STORAGE_VERSION,
    TODO_TYPE_SIMPLE,
)

_LOGGER = logging.getLogger(__name__)


class TodoCoordinator(DataUpdateCoordinator):
    """Class to manage ToDo data."""

    def __init__(self, hass: HomeAssistant, store: storage.Store) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),  # Update every minute
        )
        self.store = store
        self.todos: dict[str, dict[str, Any]] = {}
        self.persons: dict[str, dict[str, Any]] = {}
        self._entity_registry = None

    async def async_load_data(self) -> None:
        """Load data from storage."""
        data = await self.store.async_load()
        if data:
            self.todos = data.get(STORAGE_KEY_TODOS, {})
            self.persons = data.get(STORAGE_KEY_PERSONS, {})
        else:
            # Initialize with default person if none exists
            if not self.persons:
                default_person_id = str(uuid.uuid4())
                self.persons[default_person_id] = {
                    "id": default_person_id,
                    "name": "Standard",
                    "color": "#1976d2",
                }
                await self.async_save_data()

    async def async_save_data(self) -> None:
        """Save data to storage."""
        data = {
            STORAGE_KEY_TODOS: self.todos,
            STORAGE_KEY_PERSONS: self.persons,
        }
        await self.store.async_save(data)
        await self.async_request_refresh()

    async def _async_update_data(self) -> None:
        """Update data."""
        # Check for recurring todos that need to be created
        await self._check_recurring_todos()
        return {
            "todos": self.todos,
            "persons": self.persons,
        }

    async def _check_recurring_todos(self) -> None:
        """Check and create recurring todos."""
        now = datetime.now()
        created_new = False
        
        for todo_id, todo in list(self.todos.items()):
            if not todo.get("recurring", False):
                continue
            
            recurring_rule = todo.get("recurring_rule", {})
            if not recurring_rule:
                continue
            
            interval = recurring_rule.get("interval", 1)
            unit = recurring_rule.get("unit", "days")
            
            # Check if todo is completed - if so, create next occurrence
            if todo.get("completed", False):
                completed_date = todo.get("completed_date")
                if not completed_date:
                    continue
                    
                try:
                    completed_dt = datetime.fromisoformat(completed_date.replace("Z", "+00:00"))
                    if completed_dt.tzinfo:
                        completed_dt = completed_dt.replace(tzinfo=None)
                except (ValueError, TypeError):
                    continue
                
                # Calculate next due date
                if unit == "days":
                    next_due = completed_dt + timedelta(days=interval)
                elif unit == "weeks":
                    next_due = completed_dt + timedelta(weeks=interval)
                elif unit == "months":
                    # Calculate months properly
                    year = completed_dt.year
                    month = completed_dt.month + interval
                    day = completed_dt.day
                    # Handle month overflow
                    while month > 12:
                        month -= 12
                        year += 1
                    # Handle day overflow (e.g., Feb 30 -> Feb 28)
                    while True:
                        try:
                            next_due = datetime(year, month, day)
                            break
                        except ValueError:
                            day -= 1
                else:
                    continue
                
                # Check if next occurrence should be created (only if due date has passed)
                if now >= next_due:
                    # Check if this occurrence already exists
                    # Look for todos with same title, recurring pattern, and due date
                    existing = False
                    for existing_todo in self.todos.values():
                        if (existing_todo.get("title") == todo.get("title") and
                            existing_todo.get("recurring", False) and
                            existing_todo.get("recurring_rule") == recurring_rule and
                            existing_todo.get("due_date") == next_due.strftime("%Y-%m-%d") and
                            not existing_todo.get("completed", False)):
                            existing = True
                            break
                    
                    if not existing:
                        # Create new todo based on this one
                        new_todo_id = str(uuid.uuid4())
                        new_todo = todo.copy()
                        new_todo["id"] = new_todo_id
                        new_todo["completed"] = False
                        new_todo["completed_date"] = None
                        new_todo["due_date"] = next_due.strftime("%Y-%m-%d")
                        new_todo["result"] = None  # Reset result
                        
                        # If items exist (shopping/packing lists), reset them
                        if "items" in new_todo:
                            for item in new_todo["items"]:
                                item["checked"] = False
                        
                        self.todos[new_todo_id] = new_todo
                        created_new = True
        
        if created_new:
            await self.async_save_data()

    async def async_setup_entities(self) -> None:
        """Setup sensor entities for todos."""
        # Entities will be created dynamically based on todos
        pass

    @callback
    def get_todos(self, filter_completed: bool = False) -> list[dict[str, Any]]:
        """Get all todos, optionally filtered."""
        todos = list(self.todos.values())
        if filter_completed:
            todos = [t for t in todos if not t.get("completed", False)]
        # Convert to proper dict format
        return sorted(todos, key=lambda x: self._get_urgency_score(x), reverse=True)
    
    @callback
    def get_todos_dict(self) -> dict[str, dict[str, Any]]:
        """Get todos as dictionary for easier access."""
        return self.todos

    @callback
    def _get_urgency_score(self, todo: dict[str, Any]) -> float:
        """Calculate urgency score for sorting."""
        if todo.get("completed", False):
            return 0.0
        
        due_date = todo.get("due_date")
        due_time = todo.get("due_time", "23:59")
        
        if not due_date:
            return 0.5  # No due date = medium priority
        
        try:
            due_str = f"{due_date} {due_time}"
            due_dt = datetime.strptime(due_str, "%Y-%m-%d %H:%M")
            now = datetime.now()
            
            if due_dt < now:
                # Overdue - return high score based on how overdue
                hours_overdue = (now - due_dt).total_seconds() / 3600
                return 1000.0 + hours_overdue
            
            # Calculate hours until due
            hours_until = (due_dt - now).total_seconds() / 3600
            
            # Return inverse score - closer to due = higher score
            if hours_until < 24:
                return 100.0 - hours_until
            elif hours_until < 168:  # 1 week
                return 50.0 - (hours_until / 7)
            else:
                return 10.0 - (hours_until / 168)
        except (ValueError, TypeError):
            return 0.5

    @callback
    def get_todo(self, todo_id: str) -> dict[str, Any] | None:
        """Get a specific todo."""
        return self.todos.get(todo_id)

    @callback
    def get_persons(self) -> list[dict[str, Any]]:
        """Get all persons."""
        return list(self.persons.values())

    @callback
    def get_person(self, person_id: str) -> dict[str, Any] | None:
        """Get a specific person."""
        return self.persons.get(person_id)
