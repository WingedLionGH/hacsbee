class TodoManagerCard extends HTMLElement {
  setConfig(config) {
    this.config = {
      title: config.title || 'ToDo Manager',
      show_completed: config.show_completed !== false,
      ...config
    };
    if (this.content) {
      this.renderCard();
    }
  }

  set hass(hass) {
    this._hass = hass;
    if (this.content) {
      this.updateCard();
    }
  }

  connectedCallback() {
    this.renderCard();
  }

  renderCard() {
    if (!this.content) {
      const card = document.createElement('ha-card');
      card.header = this.config.title;
      this.content = document.createElement('div');
      this.content.style.padding = '16px';
      card.appendChild(this.content);
      this.appendChild(card);
    }
    this.updateCard();
  }

  async updateCard() {
    if (!this._hass) return;

    try {
      // Get todos and persons from sensor attributes
      const activeSensor = this._hass.states['sensor.todo_manager_active'];
      const todos = activeSensor?.attributes?.todos || [];
      const persons = activeSensor?.attributes?.persons || [];

      const showCompleted = this.config.show_completed;
      const displayTodos = showCompleted ? todos : todos.filter(t => !t.completed);

      let html = this.getStyles() + `
        <div class="todo-manager">
          <div class="todo-header">
            <div class="stats">
              <span>Total: ${todos.length}</span>
              <span>Aktiv: ${todos.filter(t => !t.completed).length}</span>
            </div>
            <button class="btn btn-primary" onclick="this.getRootNode().host.openModal()">
              + Neues ToDo
            </button>
          </div>
          <div class="todo-list">
      `;

      if (displayTodos.length === 0) {
        html += '<p class="empty-state">Keine ToDos vorhanden</p>';
      } else {
        displayTodos.forEach(todo => {
          html += this.renderTodoItem(todo, persons);
        });
      }

      html += `
          </div>
        </div>
        ${this.renderModal(persons)}
      `;

      this.content.innerHTML = html;
      this.attachEventListeners();
    } catch (error) {
      console.error('Error updating card:', error);
      this.content.innerHTML = '<p>Fehler beim Laden der ToDos</p>';
    }
  }

  getStyles() {
    return `
      <style>
        .todo-manager {
          font-family: var(--paper-font-body1_-_font-family, Roboto, sans-serif);
        }
        .todo-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
          padding-bottom: 12px;
          border-bottom: 1px solid var(--divider-color, #e0e0e0);
        }
        .stats {
          display: flex;
          gap: 16px;
          font-size: 14px;
          color: var(--secondary-text-color);
        }
        .btn {
          background: var(--primary-color);
          color: var(--primary-text-color);
          border: none;
          padding: 8px 16px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
          font-weight: 500;
        }
        .btn:hover {
          opacity: 0.9;
        }
        .btn-secondary {
          background: var(--secondary-color);
        }
        .btn-danger {
          background: #f44336;
          color: white;
        }
        .todo-list {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }
        .empty-state {
          text-align: center;
          color: var(--secondary-text-color);
          padding: 32px;
        }
        .todo-item {
          border: 1px solid var(--divider-color, #e0e0e0);
          border-radius: 8px;
          padding: 16px;
          background: var(--card-background-color, #fff);
          transition: all 0.2s;
        }
        .todo-item:hover {
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .todo-item.completed {
          opacity: 0.6;
        }
        .todo-item.overdue {
          border-left: 4px solid #f44336;
        }
        .todo-item.urgent {
          border-left: 4px solid #ff9800;
        }
        .todo-header-row {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 8px;
        }
        .todo-title {
          font-weight: 500;
          font-size: 16px;
          margin-bottom: 4px;
          color: var(--primary-text-color);
        }
        .todo-description {
          color: var(--secondary-text-color);
          font-size: 14px;
          margin-bottom: 8px;
          white-space: pre-wrap;
        }
        .todo-meta {
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          font-size: 12px;
          color: var(--secondary-text-color);
          margin-bottom: 8px;
        }
        .todo-persons {
          display: flex;
          gap: 6px;
          flex-wrap: wrap;
          margin-bottom: 8px;
        }
        .person-badge {
          padding: 4px 10px;
          border-radius: 12px;
          font-size: 11px;
          color: white;
          font-weight: 500;
        }
        .todo-actions {
          display: flex;
          gap: 8px;
          margin-top: 12px;
          padding-top: 12px;
          border-top: 1px solid var(--divider-color, #e0e0e0);
        }
        .todo-items {
          margin-top: 12px;
          padding-top: 12px;
          border-top: 1px solid var(--divider-color, #e0e0e0);
        }
        .todo-item-row {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 6px 0;
        }
        .todo-item-row input[type="checkbox"] {
          cursor: pointer;
          width: 18px;
          height: 18px;
        }
        .todo-item-row span {
          flex: 1;
        }
        .todo-item-row.checked {
          text-decoration: line-through;
          opacity: 0.6;
        }
        .result-box {
          margin-top: 12px;
          padding: 12px;
          background: var(--accent-color, #03a9f4);
          color: white;
          border-radius: 4px;
          font-size: 14px;
        }
        .result-box strong {
          display: block;
          margin-bottom: 4px;
        }
        .modal {
          display: none;
          position: fixed;
          z-index: 1000;
          left: 0;
          top: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(0,0,0,0.5);
          overflow-y: auto;
        }
        .modal.show {
          display: block;
        }
        .modal-content {
          background-color: var(--card-background-color, #fff);
          margin: 5% auto;
          padding: 24px;
          border-radius: 8px;
          width: 90%;
          max-width: 600px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .form-group {
          margin-bottom: 16px;
        }
        .form-group label {
          display: block;
          margin-bottom: 6px;
          font-weight: 500;
          color: var(--primary-text-color);
        }
        .form-group input,
        .form-group textarea,
        .form-group select {
          width: 100%;
          padding: 10px;
          border: 1px solid var(--divider-color, #e0e0e0);
          border-radius: 4px;
          font-size: 14px;
          font-family: inherit;
          box-sizing: border-box;
        }
        .form-group textarea {
          min-height: 100px;
          resize: vertical;
        }
        .person-select {
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          padding: 8px;
          border: 1px solid var(--divider-color, #e0e0e0);
          border-radius: 4px;
        }
        .person-checkbox {
          display: flex;
          align-items: center;
          gap: 6px;
        }
        .item-input-row {
          display: flex;
          gap: 8px;
          margin-bottom: 8px;
        }
        .item-input-row input {
          flex: 1;
        }
        .item-list {
          margin-top: 12px;
          max-height: 300px;
          overflow-y: auto;
        }
        .modal-actions {
          display: flex;
          gap: 8px;
          justify-content: flex-end;
          margin-top: 24px;
        }
      </style>
    `;
  }

  getUrgencyClass(todo) {
    if (todo.completed) return 'completed';
    const dueDate = todo.due_date;
    const dueTime = todo.due_time || '23:59';
    if (!dueDate) return '';

    try {
      const dueStr = `${dueDate}T${dueTime}:00`;
      const dueDt = new Date(dueStr);
      const now = new Date();

      if (dueDt < now) return 'overdue';
      const hoursUntil = (dueDt - now) / (1000 * 60 * 60);
      if (hoursUntil < 24) return 'urgent';
    } catch (e) {
      console.error('Date parsing error:', e);
    }
    return '';
  }

  renderTodoItem(todo, persons) {
    const urgencyClass = this.getUrgencyClass(todo);
    // Handle persons - can be array of IDs or array of objects
    const personIds = (todo.persons || []).map(p => typeof p === 'string' ? p : p.id || p);
    const personBadges = personIds
      .map(pid => {
        const person = persons.find(p => (p.id || p) === pid);
        if (!person) return '';
        const personObj = typeof person === 'object' ? person : { name: person, color: '#1976d2' };
        return `<span class="person-badge" style="background-color: ${personObj.color || '#1976d2'}">${this.escapeHtml(personObj.name || person)}</span>`;
      })
      .filter(b => b)
      .join('');

    const dueText = todo.due_date
      ? `${todo.due_date} ${todo.due_time || '23:59'}`
      : 'Kein Fälligkeitsdatum';

    let itemsHtml = '';
    if (todo.items && Array.isArray(todo.items) && todo.items.length > 0) {
      itemsHtml = '<div class="todo-items"><strong>Items:</strong>';
      todo.items.forEach(item => {
        const checked = item.checked ? 'checked' : '';
        const checkedClass = item.checked ? 'checked' : '';
        itemsHtml += `
          <div class="todo-item-row ${checkedClass}">
            <input type="checkbox" ${checked}
              onchange="this.getRootNode().host.toggleItem('${todo.id}', '${item.id}')">
            <span>${this.escapeHtml(item.name || '')}${item.quantity ? ` (${this.escapeHtml(item.quantity)})` : ''}</span>
          </div>
        `;
      });
      itemsHtml += '</div>';
    }

    let resultHtml = '';
    if (todo.result) {
      resultHtml = `<div class="result-box">
        <strong>Ergebnis:</strong>
        <div>${this.escapeHtml(todo.result)}</div>
      </div>`;
    }

    const typeLabels = {
      'simple': 'Einfach',
      'complex': 'Komplex',
      'shopping': 'Einkaufsliste',
      'packing': 'Packliste'
    };
    const typeLabel = typeLabels[todo.todo_type] || todo.todo_type;

    return `
      <div class="todo-item ${urgencyClass}">
        <div class="todo-header-row">
          <div style="flex: 1;">
            <div class="todo-title">${this.escapeHtml(todo.title || '')}</div>
            ${todo.description ? `<div class="todo-description">${this.escapeHtml(todo.description)}</div>` : ''}
          </div>
          <button class="btn ${todo.completed ? 'btn-secondary' : 'btn-primary'}" 
            style="padding: 6px 12px; font-size: 13px;"
            onclick="this.getRootNode().host.completeTodo('${todo.id}')">
            ${todo.completed ? 'Rückgängig' : 'Erledigt'}
          </button>
        </div>
        <div class="todo-meta">
          <span>📅 ${this.escapeHtml(dueText)}</span>
          <span>📋 ${this.escapeHtml(typeLabel)}</span>
          ${todo.recurring ? '<span>🔄 Wiederkehrend</span>' : ''}
        </div>
        ${personBadges ? `<div class="todo-persons">${personBadges}</div>` : ''}
        ${itemsHtml}
        ${resultHtml}
        <div class="todo-actions">
          <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 13px;"
            onclick="this.getRootNode().host.editTodo('${todo.id}')">Bearbeiten</button>
          <button class="btn btn-danger" style="padding: 6px 12px; font-size: 13px;"
            onclick="this.getRootNode().host.deleteTodo('${todo.id}')">Löschen</button>
        </div>
      </div>
    `;
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  renderModal(persons) {
    return `
      <div id="todoModal" class="modal">
        <div class="modal-content">
          <h2 id="modalTitle" style="margin-top: 0;">Neues ToDo</h2>
          <form id="todoForm">
            <div class="form-group">
              <label>Titel *</label>
              <input type="text" id="todoTitle" required>
            </div>
            <div class="form-group">
              <label>Beschreibung</label>
              <textarea id="todoDescription"></textarea>
            </div>
            <div class="form-group">
              <label>Fälligkeitsdatum</label>
              <input type="date" id="todoDueDate">
            </div>
            <div class="form-group">
              <label>Fälligkeitszeit</label>
              <input type="time" id="todoDueTime" value="23:59">
            </div>
            <div class="form-group">
              <label>Typ</label>
              <select id="todoType">
                <option value="simple">Einfach</option>
                <option value="complex">Komplex</option>
                <option value="shopping">Einkaufsliste</option>
                <option value="packing">Packliste</option>
              </select>
            </div>
            <div class="form-group">
              <label>Personen</label>
              <div class="person-select">
                ${persons.map(p => `
                  <div class="person-checkbox">
                    <input type="checkbox" id="person_${p.id}" value="${p.id}">
                    <label for="person_${p.id}" style="color: ${p.color || '#1976d2'}; cursor: pointer;">${this.escapeHtml(p.name)}</label>
                  </div>
                `).join('')}
                ${persons.length === 0 ? '<p style="color: var(--secondary-text-color); font-size: 12px;">Keine Personen verfügbar</p>' : ''}
              </div>
            </div>
            <div class="form-group">
              <label>
                <input type="checkbox" id="todoRecurring"> Wiederkehrend
              </label>
            </div>
            <div class="form-group" id="recurringRule" style="display: none;">
              <label>Wiederholungsintervall</label>
              <div style="display: flex; gap: 8px;">
                <input type="number" id="recurringInterval" min="1" value="1" style="width: 80px;">
                <select id="recurringUnit" style="flex: 1;">
                  <option value="days">Tage</option>
                  <option value="weeks">Wochen</option>
                  <option value="months">Monate</option>
                </select>
              </div>
            </div>
            <div class="form-group" id="todoItemsContainer" style="display: none;">
              <label>Items</label>
              <div id="todoItemsList" class="item-list"></div>
              <button type="button" class="btn btn-secondary" onclick="this.getRootNode().host.addItem()">+ Item hinzufügen</button>
            </div>
            <div class="form-group" id="todoResultContainer" style="display: none;">
              <label>Ergebnis</label>
              <textarea id="todoResult"></textarea>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn btn-secondary" onclick="this.getRootNode().host.closeModal()">Abbrechen</button>
              <button type="submit" class="btn btn-primary">Speichern</button>
            </div>
          </form>
        </div>
      </div>
    `;
  }

  attachEventListeners() {
    const form = this.content?.querySelector('#todoForm');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.saveTodo();
      });
    }

    const todoType = this.content?.querySelector('#todoType');
    const recurringCheckbox = this.content?.querySelector('#todoRecurring');

    if (todoType) {
      todoType.addEventListener('change', () => {
        this.updateFormFields();
      });
    }

    if (recurringCheckbox) {
      recurringCheckbox.addEventListener('change', () => {
        const ruleDiv = this.content.querySelector('#recurringRule');
        if (ruleDiv) {
          ruleDiv.style.display = recurringCheckbox.checked ? 'block' : 'none';
        }
      });
    }
  }

  updateFormFields() {
    const todoType = this.content?.querySelector('#todoType')?.value;
    const itemsContainer = this.content?.querySelector('#todoItemsContainer');
    const resultContainer = this.content?.querySelector('#todoResultContainer');

    if (itemsContainer) {
      itemsContainer.style.display =
        (todoType === 'shopping' || todoType === 'packing') ? 'block' : 'none';
    }

    if (resultContainer) {
      resultContainer.style.display = todoType === 'complex' ? 'block' : 'none';
    }
  }

  openModal(todoId = null) {
    this.editingTodoId = todoId;
    const modal = this.content.querySelector('#todoModal');
    const title = this.content.querySelector('#modalTitle');
    const form = this.content.querySelector('#todoForm');

    if (modal) {
      modal.classList.add('show');
    }
    if (title) {
      title.textContent = todoId ? 'ToDo bearbeiten' : 'Neues ToDo';
    }

    if (todoId) {
      // Load todo data from sensor
      const activeSensor = this._hass?.states['sensor.todo_manager_active'];
      const todos = activeSensor?.attributes?.todos || [];
      const todo = todos.find(t => t.id === todoId);
      
      if (todo) {
        this.populateForm(todo);
      } else {
        form?.reset();
      }
    } else {
      form?.reset();
      const dueTime = this.content.querySelector('#todoDueTime');
      if (dueTime) dueTime.value = '23:59';
      const todoType = this.content.querySelector('#todoType');
      if (todoType) todoType.value = 'simple';
      const itemsList = this.content.querySelector('#todoItemsList');
      if (itemsList) itemsList.innerHTML = '';
      this.updateFormFields();
    }
  }

  populateForm(todo) {
    const form = this.content.querySelector('#todoForm');
    if (!form) return;

    this.content.querySelector('#todoTitle').value = todo.title || '';
    this.content.querySelector('#todoDescription').value = todo.description || '';
    this.content.querySelector('#todoDueDate').value = todo.due_date || '';
    this.content.querySelector('#todoDueTime').value = todo.due_time || '23:59';
    this.content.querySelector('#todoType').value = todo.todo_type || 'simple';
    this.content.querySelector('#todoRecurring').checked = todo.recurring || false;

    if (todo.recurring_rule) {
      this.content.querySelector('#recurringInterval').value = todo.recurring_rule.interval || 1;
      this.content.querySelector('#recurringUnit').value = todo.recurring_rule.unit || 'days';
    }

    // Reset person checkboxes
    const checkboxes = this.content.querySelectorAll('input[type="checkbox"][id^="person_"]');
    checkboxes.forEach(cb => cb.checked = false);

    // Check assigned persons (handle both ID strings and objects)
    if (todo.persons && Array.isArray(todo.persons)) {
      todo.persons.forEach(p => {
        const pid = typeof p === 'string' ? p : (p.id || p);
        const cb = this.content.querySelector(`#person_${pid}`);
        if (cb) cb.checked = true;
      });
    }

    // Populate items
    const itemsList = this.content.querySelector('#todoItemsList');
    if (itemsList) {
      itemsList.innerHTML = '';
      if (todo.items && Array.isArray(todo.items) && todo.items.length > 0) {
        todo.items.forEach(item => {
          this.addItemToForm(item);
        });
      }
    }

    // Populate result for complex todos
    if (todo.result) {
      this.content.querySelector('#todoResult').value = todo.result;
    }

    this.updateFormFields();
    const ruleDiv = this.content.querySelector('#recurringRule');
    if (ruleDiv) {
      ruleDiv.style.display = todo.recurring ? 'block' : 'none';
    }
  }

  addItemToForm(item) {
    const itemsList = this.content.querySelector('#todoItemsList');
    if (!itemsList) return;

    const itemId = item?.id || `item_${Date.now()}`;
    const itemDiv = document.createElement('div');
    itemDiv.className = 'item-input-row';
    itemDiv.innerHTML = `
      <input type="text" placeholder="Item Name" class="item-name" value="${this.escapeHtml(item?.name || '')}"
        data-item-id="${itemId}">
      <input type="text" placeholder="Menge (optional)" class="item-quantity" value="${this.escapeHtml(item?.quantity || '')}">
      <button type="button" class="btn btn-danger" onclick="this.parentElement.remove()" style="padding: 4px 8px;">×</button>
    `;
    itemsList.appendChild(itemDiv);
  }

  closeModal() {
    const modal = this.content.querySelector('#todoModal');
    if (modal) {
      modal.classList.remove('show');
    }
    this.editingTodoId = null;
  }

  addItem(item = null) {
    this.addItemToForm(item);
  }

  async saveTodo() {
    const form = this.content.querySelector('#todoForm');
    if (!form || !form.checkValidity()) {
      form?.reportValidity();
      return;
    }

    const formData = {
      title: this.content.querySelector('#todoTitle').value,
      description: this.content.querySelector('#todoDescription').value || null,
      due_date: this.content.querySelector('#todoDueDate').value || null,
      due_time: this.content.querySelector('#todoDueTime').value,
      todo_type: this.content.querySelector('#todoType').value,
      persons: Array.from(this.content.querySelectorAll('input[type="checkbox"][id^="person_"]:checked'))
        .map(cb => cb.value),
      recurring: this.content.querySelector('#todoRecurring').checked,
      items: []
    };

    if (formData.recurring) {
      formData.recurring_rule = {
        interval: parseInt(this.content.querySelector('#recurringInterval').value) || 1,
        unit: this.content.querySelector('#recurringUnit').value || 'days'
      };
    }

    // Collect items
    const itemRows = this.content.querySelectorAll('.item-input-row');
    itemRows.forEach(row => {
      const nameInput = row.querySelector('.item-name');
      const quantityInput = row.querySelector('.item-quantity');
      if (nameInput?.value) {
        formData.items.push({
          id: nameInput.dataset.itemId,
          name: nameInput.value,
          quantity: quantityInput?.value || '',
          checked: false
        });
      }
    });

    // Add result for complex todos
    if (formData.todo_type === 'complex') {
      const result = this.content.querySelector('#todoResult')?.value;
      if (result) {
        formData.result = result;
      }
    }

    try {
      const service = this.editingTodoId ? 'update_todo' : 'create_todo';
      const serviceData = this.editingTodoId
        ? { todo_id: this.editingTodoId, ...formData }
        : formData;

      await this._hass.callService('todo_manager', service, serviceData);
      this.closeModal();
      // Refresh after a short delay
      setTimeout(() => {
        this.updateCard();
      }, 500);
    } catch (error) {
      console.error('Error saving todo:', error);
      alert('Fehler beim Speichern: ' + (error.message || 'Unbekannter Fehler'));
    }
  }

  async deleteTodo(todoId) {
    if (confirm('ToDo wirklich löschen?')) {
      try {
        await this._hass.callService('todo_manager', 'delete_todo', { todo_id: todoId });
        setTimeout(() => {
          this.updateCard();
        }, 500);
      } catch (error) {
        console.error('Error deleting todo:', error);
        alert('Fehler beim Löschen');
      }
    }
  }

  async completeTodo(todoId) {
    try {
      await this._hass.callService('todo_manager', 'complete_todo', { todo_id: todoId });
      setTimeout(() => {
        this.updateCard();
      }, 500);
    } catch (error) {
      console.error('Error completing todo:', error);
    }
  }

  async toggleItem(todoId, itemId) {
    try {
      await this._hass.callService('todo_manager', 'toggle_item', {
        todo_id: todoId,
        item_id: itemId
      });
      setTimeout(() => {
        this.updateCard();
      }, 500);
    } catch (error) {
      console.error('Error toggling item:', error);
      alert('Fehler beim Aktualisieren des Items');
    }
  }

  editTodo(todoId) {
    this.openModal(todoId);
  }
}

customElements.define('todo-manager-card', TodoManagerCard);
