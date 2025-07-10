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

# Add new properties for Q&A
bpy.types.Scene.forgecore_qa_question = StringProperty(
    name="Blender Question",
    description="Ask a Blender/3D question",
    default=""
)
bpy.types.Scene.forgecore_qa_answer = StringProperty(
    name="Answer",
    description="Answer to your Blender/3D question",
    default=""
)

# Add new properties for Tools, Memory/History, Scene Analysis, and Server
bpy.types.Scene.forgecore_tool_input = StringProperty(
    name="Tool Command",
    description="Enter a tool command (e.g., run python: print('hi'))",
    default=""
)
bpy.types.Scene.forgecore_tool_result = StringProperty(
    name="Tool Result",
    description="Result of the last tool command",
    default=""
)
bpy.types.Scene.forgecore_scene_summary = StringProperty(
    name="Scene Summary",
    description="Summary of the current Blender scene",
    default=""
)
bpy.types.Scene.forgecore_server_address = StringProperty(
    name="Server Address",
    description="Address of external Agent Zero server",
    default=""
)

class FORGECORE_OT_ask_qa(Operator):
    bl_idname = "forgecore.ask_qa"
    bl_label = "Ask Blender Question"
    bl_description = "Ask a Blender/3D question and get an answer from the agent"

    def execute(self, context):
        question = context.scene.forgecore_qa_question
        # Import agent bridge and get answer
        try:
            from .agent_bridge import AgentBridge
            bridge = getattr(AgentBridge, 'instance', None)
            if bridge and bridge.agent_core:
                answer = bridge.agent_core.router._handle_knowledge_query(question)
            else:
                answer = "Agent not initialized."
        except Exception as e:
            answer = f"Error: {e}"
        context.scene.forgecore_qa_answer = answer
        return {'FINISHED'}

class FORGECORE_OT_run_tool(Operator):
    bl_idname = "forgecore.run_tool"
    bl_label = "Run Tool Command"
    bl_description = "Run a tool command (code execution, web search, file management)"

    def execute(self, context):
        tool_cmd = context.scene.forgecore_tool_input
        try:
            from .agent_bridge import AgentBridge
            bridge = getattr(AgentBridge, 'instance', None)
            if bridge and bridge.agent_core:
                result = bridge.agent_core.router._handle_tool(tool_cmd)
            else:
                result = "Agent not initialized."
        except Exception as e:
            result = f"Error: {e}"
        context.scene.forgecore_tool_result = result
        return {'FINISHED'}

class FORGECORE_OT_clear_history(Operator):
    bl_idname = "forgecore.clear_history"
    bl_label = "Clear Agent History"
    bl_description = "Clear the agent's memory/history"

    def execute(self, context):
        try:
            from .agent_bridge import AgentBridge
            bridge = getattr(AgentBridge, 'instance', None)
            if bridge and bridge.agent_core:
                bridge.agent_core.memory['history'] = []
                bridge.agent_core.history = []
                bridge.agent_core._save_memory()
        except Exception as e:
            print(f"Error clearing history: {e}")
        return {'FINISHED'}

class FORGECORE_OT_analyze_scene(Operator):
    bl_idname = "forgecore.analyze_scene"
    bl_label = "Analyze Blender Scene"
    bl_description = "Summarize the current Blender scene (objects, materials, etc.)"

    def execute(self, context):
        try:
            import bpy
            objects = [obj for obj in bpy.context.scene.objects]
            meshes = [obj for obj in objects if obj.type == 'MESH']
            lights = [obj for obj in objects if obj.type == 'LIGHT']
            cameras = [obj for obj in objects if obj.type == 'CAMERA']
            summary = f"Objects: {len(objects)}, Meshes: {len(meshes)}, Lights: {len(lights)}, Cameras: {len(cameras)}"
        except Exception as e:
            summary = f"Scene analysis error: {e}"
        context.scene.forgecore_scene_summary = summary
        return {'FINISHED'}

classes = [
    ui_panel.FORGECORE_PT_main_panel,
    ui_panel.FORGECORE_PT_journal_panel,
    run_prompt.FORGECORE_OT_run_prompt,
    export_scene.FORGECORE_OT_export_scene,
    FORGECORE_OT_ask_qa,
    FORGECORE_OT_run_tool,
    FORGECORE_OT_clear_history,
    FORGECORE_OT_analyze_scene,
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