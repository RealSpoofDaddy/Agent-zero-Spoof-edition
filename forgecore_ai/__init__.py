bl_info = {
    "name": "ForgeCore AI",
    "author": "Agent Zero Team",
    "version": (1, 0, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > ForgeCore AI",
    "description": "AI-powered Blender assistant for mesh generation, material creation, and scene management",
    "warning": "",
    "doc_url": "",
    "category": "Interface",
}

import bpy
from bpy.props import StringProperty
from bpy.types import Panel, Operator
import os
import sys

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from . import ui_panel
from . import agent_bridge
from .ops import run_prompt, export_scene

# Global properties
bpy.types.Scene.forgecore_prompt = StringProperty(
    name="AI Prompt",
    description="Enter your natural language prompt for AI generation",
    default=""
)

bpy.types.Scene.forgecore_goal = StringProperty(
    name="Today's Goal",
    description="What you want to accomplish today",
    default=""
)

bpy.types.Scene.forgecore_progress = StringProperty(
    name="Current Progress",
    description="Your current progress and notes",
    default=""
)

classes = [
    ui_panel.FORGECORE_PT_main_panel,
    ui_panel.FORGECORE_PT_journal_panel,
    run_prompt.FORGECORE_OT_run_prompt,
    export_scene.FORGECORE_OT_export_scene,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Initialize the agent bridge
    agent_bridge.initialize()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Cleanup the agent bridge
    agent_bridge.cleanup()

if __name__ == "__main__":
    register()