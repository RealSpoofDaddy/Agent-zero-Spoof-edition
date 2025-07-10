import bpy
from bpy.types import Operator
from bpy.props import StringProperty
import os
import sys

# Add the parent directory to the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from .. import agent_bridge
from .. import ui_panel

class FORGECORE_OT_run_prompt(Operator):
    bl_idname = "forgecore.run_prompt"
    bl_label = "Run AI Prompt"
    bl_description = "Execute the AI prompt and generate Blender code"
    
    def execute(self, context):
        prompt = context.scene.forgecore_prompt.strip()
        
        if not prompt:
            self.report({'ERROR'}, "Please enter a prompt")
            return {'CANCELLED'}
        
        try:
            # Get the agent bridge
            bridge = agent_bridge.get_bridge()
            if not bridge:
                self.report({'ERROR'}, "Agent bridge not initialized")
                return {'CANCELLED'}
            
            # Update status
            context.scene.forgecore_status = "Processing prompt..."
            
            # Handle the prompt
            blender_code = bridge.handle_prompt(prompt)
            
            # Execute the generated code
            if blender_code and not blender_code.startswith("# Error"):
                try:
                    # Execute the code in Blender's context
                    exec(blender_code, {"bpy": bpy, "__builtins__": __builtins__})
                    
                    # Update status and result
                    context.scene.forgecore_status = "Success! Code executed."
                    context.scene.forgecore_last_result = f"Generated and executed code for: {prompt[:50]}..."
                    
                    self.report({'INFO'}, "Prompt executed successfully")
                    
                except Exception as e:
                    error_msg = f"Error executing generated code: {str(e)}"
                    context.scene.forgecore_status = "Error executing code"
                    context.scene.forgecore_last_result = error_msg
                    self.report({'ERROR'}, error_msg)
                    return {'CANCELLED'}
            else:
                # Error in code generation
                context.scene.forgecore_status = "Error generating code"
                context.scene.forgecore_last_result = blender_code
                self.report({'ERROR'}, "Failed to generate valid code")
                return {'CANCELLED'}
            
            return {'FINISHED'}
            
        except Exception as e:
            error_msg = f"Error processing prompt: {str(e)}"
            context.scene.forgecore_status = "Error"
            context.scene.forgecore_last_result = error_msg
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

class FORGECORE_OT_save_journal(Operator):
    bl_idname = "forgecore.save_journal"
    bl_label = "Save Journal Entry"
    bl_description = "Save the current goal and progress to journal"
    
    def execute(self, context):
        goal = context.scene.forgecore_goal.strip()
        progress = context.scene.forgecore_progress.strip()
        
        if not goal and not progress:
            self.report({'ERROR'}, "Please enter a goal or progress")
            return {'CANCELLED'}
        
        try:
            # Save the journal entry
            success = ui_panel.save_journal_entry(goal, progress)
            
            if success:
                # Clear the inputs
                context.scene.forgecore_goal = ""
                context.scene.forgecore_progress = ""
                
                self.report({'INFO'}, "Journal entry saved successfully")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Failed to save journal entry")
                return {'CANCELLED'}
                
        except Exception as e:
            error_msg = f"Error saving journal entry: {str(e)}"
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}