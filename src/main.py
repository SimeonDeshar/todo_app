from nicegui import app, ui


@ui.page('/')
def main_page():
    # --- 1. Load tasks from user storage (server-side, writable anytime) ---
    if 'tasks' not in app.storage.user:
        app.storage.user['tasks'] = []

    def get_tasks():
        return app.storage.user['tasks']

    # --- 2. Helpers ---
    def render_task(index, task):
        with ui.row().classes('w-full items-center bg-gray-100 rounded p-2 gap-2'):
            def on_toggle(e, i=index):
                get_tasks()[i]['completed'] = e.value
                refresh()

            ui.checkbox(value=task['completed'], on_change=on_toggle)

            label_classes = 'flex-grow text-base'
            if task['completed']:
                label_classes += ' line-through text-gray-400'
            ui.label(task['title']).classes(label_classes)

            def on_delete(i=index):
                get_tasks().pop(i)
                refresh()

            ui.button(icon='delete', on_click=on_delete).props('flat dense color=red')

    def refresh():
        task_container.clear()
        with task_container:
            tasks = get_tasks()
            if not tasks:
                ui.label('No tasks yet. Add one above!').classes('text-gray-400 italic')
            else:
                for i, task in enumerate(tasks):
                    render_task(i, task)

    def add_task():
        title = (task_input.value or '').strip()
        if not title:
            return
        get_tasks().append({'title': title, 'completed': False})
        task_input.value = ''
        refresh()

    # --- 3. Build the UI ---
    with ui.column().classes('w-full max-w-2xl mx-auto p-6 gap-4'):
        ui.label('📝 My To-Do List').classes('text-3xl font-bold')

        with ui.row().classes('w-full gap-2 items-center'):
            task_input = ui.input(placeholder='What needs to be done?') \
                .classes('flex-grow').props('outlined dense')
            ui.button('Add', on_click=add_task).props('unelevated')

        task_container = ui.column().classes('w-full gap-2')

    # --- 4. Bind Enter key and render initial state ---
    task_input.on('keydown.enter', add_task)
    refresh()


ui.run(title='To-Do List', storage_secret='replace-me-with-a-long-random-string')