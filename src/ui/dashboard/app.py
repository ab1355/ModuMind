import os
from nicegui import ui
from supabase import create_client, Client

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")
supabase: Client = create_client(url, key)

# Dashboard UI
with ui.column().classes('w-full h-screen'):
    with ui.header().classes('bg-blue-600 text-white'):
        ui.label('ModuMind Dashboard').classes('text-h4 q-my-md')
    
    with ui.row().classes('w-full'):
        with ui.column().classes('w-1/4 p-4'):
            # Sidebar navigation
            with ui.card().classes('w-full'):
                ui.label('Navigation').classes('text-h6')
                ui.separator()
                with ui.column().classes('w-full'):
                    ui.button('Dashboard', icon='dashboard').classes('w-full text-left')
                    ui.button('Agents', icon='smart_toy').classes('w-full text-left')
                    ui.button('Integrations', icon='link').classes('w-full text-left')
                    ui.button('Logs', icon='article').classes('w-full text-left')
                    ui.button('Settings', icon='settings').classes('w-full text-left')

        with ui.column().classes('w-3/4 p-4'):
            # Main content area
            with ui.card().classes('w-full'):
                ui.label('Agent Status').classes('text-h5')
                ui.separator()
                
                agent_data = [
                    {'name': 'Orchestrator', 'status': 'Running', 'tasks': 5},
                    {'name': 'Researcher', 'status': 'Running', 'tasks': 2},
                    {'name': 'Executor', 'status': 'Idle', 'tasks': 0},
                ]
                
                columns = [
                    {'name': 'name', 'label': 'Agent', 'field': 'name', 'required': True},
                    {'name': 'status', 'label': 'Status', 'field': 'status', 'required': True},
                    {'name': 'tasks', 'label': 'Active Tasks', 'field': 'tasks', 'required': True},
                ]
                
                ui.table(columns=columns, rows=agent_data, row_key='name')
            
            with ui.card().classes('w-full mt-4'):
                ui.label('Quick Actions').classes('text-h5')
                ui.separator()
                
                with ui.row().classes('w-full justify-between'):
                    ui.button('Add Agent', icon='add').props('color=primary')
                    ui.button('Sync Odoo', icon='sync').props('color=secondary')
                    ui.button('Deploy Flow', icon='play_arrow').props('color=positive')

ui.run(title='ModuMind Dashboard')