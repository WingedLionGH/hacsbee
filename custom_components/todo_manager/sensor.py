"""Sensor platform for ToDo Manager."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TodoCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ToDo Manager sensor entities."""
    coordinator: TodoCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Create summary sensors
    async_add_entities([
        TodoSummarySensor(coordinator, "all"),
        TodoSummarySensor(coordinator, "active"),
        TodoSummarySensor(coordinator, "overdue"),
    ])


class TodoSummarySensor(CoordinatorEntity, SensorEntity):
    """Representation of a ToDo summary sensor."""

    def __init__(
        self,
        coordinator: TodoCoordinator,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"ToDo Manager {sensor_type.capitalize()}"
        self._attr_unique_id = f"{DOMAIN}_{sensor_type}"
        self._attr_icon = "mdi:format-list-checks"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self._sensor_type == "all":
            return len(self.coordinator.todos)
        elif self._sensor_type == "active":
            todos = self.coordinator.get_todos(filter_completed=True)
            return len(todos)
        elif self._sensor_type == "overdue":
            todos = self.coordinator.get_todos(filter_completed=True)
            now = datetime.now()
            overdue_count = 0
            for todo in todos:
                due_date = todo.get("due_date")
                due_time = todo.get("due_time", "23:59")
                if due_date:
                    try:
                        due_str = f"{due_date} {due_time}"
                        due_dt = datetime.strptime(due_str, "%Y-%m-%d %H:%M")
                        if due_dt < now:
                            overdue_count += 1
                    except (ValueError, TypeError):
                        pass
            return overdue_count
        return 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        if self._sensor_type == "active":
            todos = self.coordinator.get_todos(filter_completed=True)
            # Include all todos, not just top 10, for frontend
            return {
                "todos": [self._todo_to_dict(t) for t in todos],
                "total_count": len(todos),
                "persons": self.coordinator.get_persons(),
            }
        return {}

    def _todo_to_dict(self, todo: dict[str, Any]) -> dict[str, Any]:
        """Convert todo dict to a simplified version for attributes."""
        return {
            "id": todo.get("id"),
            "title": todo.get("title"),
            "description": todo.get("description"),
            "due_date": todo.get("due_date"),
            "due_time": todo.get("due_time"),
            "todo_type": todo.get("todo_type"),
            "persons": todo.get("persons", []),
            "recurring": todo.get("recurring", False),
            "recurring_rule": todo.get("recurring_rule"),
            "completed": todo.get("completed", False),
            "completed_date": todo.get("completed_date"),
            "result": todo.get("result"),
            "items": todo.get("items", []),
            "urgency_score": self.coordinator._get_urgency_score(todo),
        }
