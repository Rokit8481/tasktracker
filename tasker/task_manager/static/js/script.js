document.addEventListener("DOMContentLoaded", () => {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }
  const csrftoken = getCookie('csrftoken');

  let draggedCard = null;
  let prevParent = null;
  let prevNextSibling = null;

  function onDragStart(e) {
    draggedCard = this;
    prevParent = this.parentElement;
    prevNextSibling = this.nextElementSibling;
    this.classList.add('dragging');
    try { e.dataTransfer.setData('text/plain', this.dataset.taskId); } catch (err) {}
  }

  function onDragEnd() {
    if (draggedCard) draggedCard.classList.remove('dragging');
    draggedCard = null;
    prevParent = null;
    prevNextSibling = null;
  }

  function attachDragHandlers(card) {
    card.setAttribute('draggable', 'true');
    card.removeEventListener('dragstart', onDragStart);
    card.removeEventListener('dragend', onDragEnd);
    card.addEventListener('dragstart', onDragStart);
    card.addEventListener('dragend', onDragEnd);
  }

  document.querySelectorAll('.task-card').forEach(attachDragHandlers);

  document.querySelectorAll('.delete-form').forEach(function(form){
    form.addEventListener('submit', function(e){
      if (!confirm('Підтвердити видалення? Цю операцію не можна відмінити.')) {
        e.preventDefault();
      }
    });
  });

  document.querySelectorAll('.board-column').forEach(column => {
    column.addEventListener('dragover', e => {
      e.preventDefault();
      column.classList.add('drag-over');
    });

    column.addEventListener('dragleave', () => {
      column.classList.remove('drag-over');
    });

    column.addEventListener('drop', async (e) => {
      e.preventDefault();
      column.classList.remove('drag-over');

      let card = draggedCard;
      if (!card) {
        const id = e.dataTransfer.getData('text/plain');
        card = document.querySelector(`.task-card[data-task-id="${id}"]`);
      }
      if (!card) return;

      column.appendChild(card);

      const taskId = card.dataset.taskId;
      const newStatus = column.dataset.status;
      const body = new URLSearchParams({ task_id: taskId, status: newStatus });

      try {
        const updateUrl = window.taskUpdateUrl;

        const resp = await fetch(updateUrl, {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': csrftoken || '',
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: body.toString()
        });

        if (!resp.ok) {
          const text = await resp.text();
          console.error('Status update failed', resp.status, text);
          alert('Помилка при оновленні статусу (див. консоль).');
          if (prevParent) {
            if (prevNextSibling) prevParent.insertBefore(card, prevNextSibling);
            else prevParent.appendChild(card);
          }
          return;
        }

        const data = await resp.json();
        if (!data.success) {
          console.error('Server returned error:', data);
          alert('Сервер відкинув оновлення статусу.');
          if (prevParent) {
            if (prevNextSibling) prevParent.insertBefore(card, prevNextSibling);
            else prevParent.appendChild(card);
          }
        }
      } catch (err) {
        console.error('Fetch error:', err);
        alert('Мережева помилка при оновленні статусу.');
        if (prevParent) {
          if (prevNextSibling) prevParent.insertBefore(card, prevNextSibling);
          else prevParent.appendChild(card);
        }
      } finally {
        prevParent = null;
        prevNextSibling = null;
      }
    });
  });
});
