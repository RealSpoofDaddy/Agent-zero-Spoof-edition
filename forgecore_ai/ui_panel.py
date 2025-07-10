import bpy
from bpy.types import Panel
from bpy.props import StringProperty
import os
import json
from datetime import datetime

class FORGECORE_PT_main_panel(Panel):
    bl_label = "ForgeCore AI"
    bl_idname = "FORGECORE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ForgeCore AI'

    def draw(self, context):
        layout = self.layout
        
        # Main prompt section
        box = layout.box()
        box.label(text="AI Assistant", icon='BOT')
        
        # Prompt input
        layout.prop(context.scene, "forgecore_prompt", text="Prompt")
        
        # Run button
        row = layout.row()
        row.scale_y = 1.5
        row.operator("forgecore.run_prompt", text="Run Prompt", icon='PLAY')
        
        # Status section
        if hasattr(context.scene, 'forgecore_status'):
            box = layout.box()
            box.label(text="Status", icon='INFO')
            box.label(text=context.scene.forgecore_status)
        
        # Recent results
        if hasattr(context.scene, 'forgecore_last_result'):
            box = layout.box()
            box.label(text="Last Result", icon='FILE_TEXT')
            box.label(text=context.scene.forgecore_last_result)

class FORGECORE_PT_journal_panel(Panel):
    bl_label = "Dev Journal"
    bl_idname = "FORGECORE_PT_journal_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ForgeCore AI'
    bl_parent_id = "FORGECORE_PT_main_panel"

    def draw(self, context):
        layout = self.layout
        
        # Journal input section
        box = layout.box()
        box.label(text="Daily Journal", icon='TEXT')
        
        # Goal input
        layout.prop(context.scene, "forgecore_goal", text="Today's Goal")
        
        # Progress input
        layout.prop(context.scene, "forgecore_progress", text="Progress")
        
        # Save button
        row = layout.row()
        row.operator("forgecore.save_journal", text="Save Entry", icon='SAVE')
        
        # Recent entries
        box = layout.box()
        box.label(text="Recent Entries", icon='HISTORY')
        
        # Load and display recent entries
        journal_entries = self.load_journal_entries()
        for entry in journal_entries[-5:]:  # Show last 5 entries
            col = box.column()
            col.label(text=f"Date: {entry.get('date', 'Unknown')}")
            col.label(text=f"Goal: {entry.get('goal', '')}")
            col.label(text=f"Progress: {entry.get('progress', '')}")
            col.separator()

    def load_journal_entries(self):
        """Load journal entries from the memory file"""
        try:
            # Get the addon directory
            addon_dir = os.path.dirname(os.path.abspath(__file__))
            memory_dir = os.path.join(addon_dir, "agent_core", "memory")
            journal_file = os.path.join(memory_dir, "journal_entries.json")
            
            if os.path.exists(journal_file):
                with open(journal_file, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading journal entries: {e}")
            return []

def save_journal_entry(goal, progress):
    """Save a journal entry to the memory file"""
    try:
        # Get the addon directory
        addon_dir = os.path.dirname(os.path.abspath(__file__))
        memory_dir = os.path.join(addon_dir, "agent_core", "memory")
        os.makedirs(memory_dir, exist_ok=True)
        
        journal_file = os.path.join(memory_dir, "journal_entries.json")
        
        # Load existing entries
        entries = []
        if os.path.exists(journal_file):
            with open(journal_file, 'r') as f:
                entries = json.load(f)
        
        # Add new entry
        new_entry = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'goal': goal,
            'progress': progress
        }
        entries.append(new_entry)
        
        # Save back to file
        with open(journal_file, 'w') as f:
            json.dump(entries, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving journal entry: {e}")
        return False