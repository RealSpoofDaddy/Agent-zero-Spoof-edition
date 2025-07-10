"""
ForgeCore AI - Main Agent Core
Adapted from Agent Zero for Blender integration
"""

import re
import json
from typing import Dict, List, Optional
from datetime import datetime

class PromptRouter:
    """Routes prompts to appropriate handlers based on content"""
    
    def __init__(self):
        self.handlers = {
            'mesh': self._handle_mesh_generation,
            'material': self._handle_material_generation,
            'layout': self._handle_scene_layout,
            'camera': self._handle_camera_setup,
            'lighting': self._handle_lighting_setup,
            'animation': self._handle_animation,
            'export': self._handle_export,
            'utility': self._handle_utility
        }
    
    def route_prompt(self, prompt: str) -> str:
        """Route a prompt to the appropriate handler and return Blender code"""
        prompt_lower = prompt.lower()
        
        # Determine the type of operation based on keywords
        if any(word in prompt_lower for word in ['cube', 'sphere', 'cylinder', 'mesh', 'object', 'model', 'create']):
            return self._handle_mesh_generation(prompt)
        elif any(word in prompt_lower for word in ['material', 'texture', 'shader', 'color', 'metal', 'wood']):
            return self._handle_material_generation(prompt)
        elif any(word in prompt_lower for word in ['layout', 'arrange', 'position', 'scene', 'setup']):
            return self._handle_scene_layout(prompt)
        elif any(word in prompt_lower for word in ['camera', 'view', 'render']):
            return self._handle_camera_setup(prompt)
        elif any(word in prompt_lower for word in ['light', 'lighting', 'illuminate']):
            return self._handle_lighting_setup(prompt)
        elif any(word in prompt_lower for word in ['animate', 'animation', 'keyframe']):
            return self._handle_animation(prompt)
        elif any(word in prompt_lower for word in ['export', 'save', 'fbx', 'obj']):
            return self._handle_export(prompt)
        else:
            return self._handle_utility(prompt)
    
    def _handle_mesh_generation(self, prompt: str) -> str:
        """Generate Blender code for mesh creation"""
        code_lines = []
        
        # Basic mesh creation based on prompt keywords
        if 'cube' in prompt.lower():
            code_lines.append("bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))")
            code_lines.append("cube = bpy.context.active_object")
            code_lines.append("cube.name = 'Generated_Cube'")
        elif 'sphere' in prompt.lower():
            code_lines.append("bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))")
            code_lines.append("sphere = bpy.context.active_object")
            code_lines.append("sphere.name = 'Generated_Sphere'")
        elif 'cylinder' in prompt.lower():
            code_lines.append("bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0, 0, 0))")
            code_lines.append("cylinder = bpy.context.active_object")
            code_lines.append("cylinder.name = 'Generated_Cylinder'")
        else:
            # Default to cube for generic mesh requests
            code_lines.append("bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))")
            code_lines.append("obj = bpy.context.active_object")
            code_lines.append("obj.name = 'Generated_Object'")
        
        # Add modifiers based on prompt
        if 'smooth' in prompt.lower():
            code_lines.append("modifier = obj.modifiers.new(name='Smooth', type='SUBSURF')")
            code_lines.append("modifier.levels = 2")
        
        if 'bevel' in prompt.lower():
            code_lines.append("bevel = obj.modifiers.new(name='Bevel', type='BEVEL')")
            code_lines.append("bevel.width = 0.1")
        
        return "\n".join(code_lines)
    
    def _handle_material_generation(self, prompt: str) -> str:
        """Generate Blender code for material creation"""
        code_lines = []
        
        # Create material
        code_lines.append("material = bpy.data.materials.new(name='Generated_Material')")
        code_lines.append("material.use_nodes = True")
        code_lines.append("nodes = material.node_tree.nodes")
        code_lines.append("links = material.node_tree.links")
        
        # Clear default nodes
        code_lines.append("nodes.clear()")
        
        # Add principled BSDF
        code_lines.append("principled = nodes.new(type='ShaderNodeBsdfPrincipled')")
        code_lines.append("output = nodes.new(type='ShaderNodeOutputMaterial')")
        code_lines.append("links.new(principled.outputs['BSDF'], output.inputs['Surface'])")
        
        # Set material properties based on prompt
        if 'metal' in prompt.lower():
            code_lines.append("principled.inputs['Metallic'].default_value = 1.0")
            code_lines.append("principled.inputs['Roughness'].default_value = 0.1")
        elif 'plastic' in prompt.lower():
            code_lines.append("principled.inputs['Metallic'].default_value = 0.0")
            code_lines.append("principled.inputs['Roughness'].default_value = 0.3")
        elif 'glass' in prompt.lower():
            code_lines.append("principled.inputs['Transmission'].default_value = 1.0")
            code_lines.append("principled.inputs['IOR'].default_value = 1.45")
        
        # Set color if specified
        if 'red' in prompt.lower():
            code_lines.append("principled.inputs['Base Color'].default_value = (1, 0, 0, 1)")
        elif 'blue' in prompt.lower():
            code_lines.append("principled.inputs['Base Color'].default_value = (0, 0, 1, 1)")
        elif 'green' in prompt.lower():
            code_lines.append("principled.inputs['Base Color'].default_value = (0, 1, 0, 1)")
        
        # Apply to selected objects
        code_lines.append("for obj in bpy.context.selected_objects:")
        code_lines.append("    if obj.type == 'MESH':")
        code_lines.append("        if obj.data.materials:")
        code_lines.append("            obj.data.materials[0] = material")
        code_lines.append("        else:")
        code_lines.append("            obj.data.materials.append(material)")
        
        return "\n".join(code_lines)
    
    def _handle_scene_layout(self, prompt: str) -> str:
        """Generate Blender code for scene layout"""
        code_lines = []
        
        # Create a collection for organized layout
        code_lines.append("layout_collection = bpy.data.collections.new('Layout_Collection')")
        code_lines.append("bpy.context.scene.collection.children.link(layout_collection)")
        
        # Add camera if not exists
        code_lines.append("if not bpy.data.cameras:")
        code_lines.append("    bpy.ops.object.camera_add(location=(5, -5, 3))")
        code_lines.append("    camera = bpy.context.active_object")
        code_lines.append("    camera.rotation_euler = (1.1, 0, 0.785)")
        code_lines.append("    bpy.context.scene.camera = camera")
        
        # Add lighting if not exists
        code_lines.append("if not bpy.data.lights:")
        code_lines.append("    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))")
        code_lines.append("    sun = bpy.context.active_object")
        code_lines.append("    sun.data.energy = 5.0")
        
        # Arrange objects in a grid if multiple objects
        code_lines.append("objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']")
        code_lines.append("for i, obj in enumerate(objects):")
        code_lines.append("    row = i // 3")
        code_lines.append("    col = i % 3")
        code_lines.append("    obj.location = (col * 3, row * 3, 0)")
        
        return "\n".join(code_lines)
    
    def _handle_camera_setup(self, prompt: str) -> str:
        """Generate Blender code for camera setup"""
        code_lines = []
        
        # Create or modify camera
        code_lines.append("if not bpy.data.cameras:")
        code_lines.append("    bpy.ops.object.camera_add()")
        code_lines.append("camera = bpy.context.active_object")
        code_lines.append("bpy.context.scene.camera = camera")
        
        # Set camera properties based on prompt
        if 'close' in prompt.lower():
            code_lines.append("camera.location = (2, -2, 1.5)")
        elif 'far' in prompt.lower():
            code_lines.append("camera.location = (10, -10, 5)")
        else:
            code_lines.append("camera.location = (5, -5, 3)")
        
        # Set camera rotation to look at origin
        code_lines.append("camera.rotation_euler = (1.1, 0, 0.785)")
        
        return "\n".join(code_lines)
    
    def _handle_lighting_setup(self, prompt: str) -> str:
        """Generate Blender code for lighting setup"""
        code_lines = []
        
        # Clear existing lights
        code_lines.append("for obj in bpy.context.scene.objects:")
        code_lines.append("    if obj.type == 'LIGHT':")
        code_lines.append("        bpy.data.objects.remove(obj, do_unlink=True)")
        
        # Add lighting based on prompt
        if 'studio' in prompt.lower():
            # Studio lighting setup
            code_lines.append("bpy.ops.object.light_add(type='AREA', location=(3, 0, 2))")
            code_lines.append("key_light = bpy.context.active_object")
            code_lines.append("key_light.data.energy = 1000")
            code_lines.append("key_light.data.size = 2")
            
            code_lines.append("bpy.ops.object.light_add(type='AREA', location=(-3, 0, 2))")
            code_lines.append("fill_light = bpy.context.active_object")
            code_lines.append("fill_light.data.energy = 500")
            code_lines.append("fill_light.data.size = 2")
            
        elif 'dramatic' in prompt.lower():
            # Dramatic lighting
            code_lines.append("bpy.ops.object.light_add(type='SPOT', location=(0, 0, 5))")
            code_lines.append("spot = bpy.context.active_object")
            code_lines.append("spot.data.energy = 2000")
            code_lines.append("spot.data.spot_size = 0.5")
            
        else:
            # Default sun lighting
            code_lines.append("bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))")
            code_lines.append("sun = bpy.context.active_object")
            code_lines.append("sun.data.energy = 5.0")
        
        return "\n".join(code_lines)
    
    def _handle_animation(self, prompt: str) -> str:
        """Generate Blender code for animation"""
        code_lines = []
        
        # Set up animation
        code_lines.append("bpy.context.scene.frame_start = 1")
        code_lines.append("bpy.context.scene.frame_end = 120")
        
        # Animate selected objects
        code_lines.append("for obj in bpy.context.selected_objects:")
        code_lines.append("    if obj.type == 'MESH':")
        code_lines.append("        obj.keyframe_insert(data_path='location', frame=1)")
        code_lines.append("        obj.location.z += 2")
        code_lines.append("        obj.keyframe_insert(data_path='location', frame=60)")
        code_lines.append("        obj.location.z -= 2")
        code_lines.append("        obj.keyframe_insert(data_path='location', frame=120)")
        
        return "\n".join(code_lines)
    
    def _handle_export(self, prompt: str) -> str:
        """Generate Blender code for export operations"""
        code_lines = []
        
        # Set up export path
        code_lines.append("import os")
        code_lines.append("blend_path = bpy.data.filepath")
        code_lines.append("if blend_path:")
        code_lines.append("    export_dir = os.path.join(os.path.dirname(blend_path), 'exports')")
        code_lines.append("    os.makedirs(export_dir, exist_ok=True)")
        code_lines.append("    fbx_path = os.path.join(export_dir, 'scene.fbx')")
        code_lines.append("    bpy.ops.export_scene.fbx(filepath=fbx_path)")
        
        return "\n".join(code_lines)
    
    def _handle_utility(self, prompt: str) -> str:
        """Handle utility operations"""
        code_lines = []
        
        # Default utility operations
        code_lines.append("# Utility operation")
        code_lines.append("print('ForgeCore AI: Processing utility request')")
        
        if 'clear' in prompt.lower():
            code_lines.append("bpy.ops.object.select_all(action='SELECT')")
            code_lines.append("bpy.ops.object.delete(use_global=False)")
        elif 'select' in prompt.lower():
            code_lines.append("bpy.ops.object.select_all(action='SELECT')")
        elif 'deselect' in prompt.lower():
            code_lines.append("bpy.ops.object.select_all(action='DESELECT')")
        
        return "\n".join(code_lines)

class AgentCore:
    """Main agent core for ForgeCore AI"""
    
    def __init__(self):
        self.router = PromptRouter()
        self.memory = {}
    
    def handle_prompt(self, prompt: str) -> str:
        """Main entry point for handling prompts"""
        try:
            # Log the prompt
            self._log_prompt(prompt)
            
            # Route the prompt to appropriate handler
            blender_code = self.router.route_prompt(prompt)
            
            # Add safety wrapper
            safe_code = self._wrap_code_safely(blender_code)
            
            # Log the result
            self._log_result(prompt, safe_code)
            
            return safe_code
            
        except Exception as e:
            error_code = f"# Error processing prompt: {str(e)}\nprint('ForgeCore AI: Error occurred')"
            self._log_result(prompt, error_code)
            return error_code
    
    def _wrap_code_safely(self, code: str) -> str:
        """Wrap code in safety checks"""
        safe_wrapper = [
            "# ForgeCore AI Generated Code",
            "try:",
            "    " + "\n    ".join(code.split("\n")),
            "    print('ForgeCore AI: Code executed successfully')",
            "except Exception as e:",
            "    print(f'ForgeCore AI: Error executing code: {e}')"
        ]
        return "\n".join(safe_wrapper)
    
    def _log_prompt(self, prompt: str):
        """Log a prompt to memory"""
        timestamp = datetime.now().isoformat()
        if 'prompts' not in self.memory:
            self.memory['prompts'] = []
        self.memory['prompts'].append({
            'timestamp': timestamp,
            'prompt': prompt
        })
    
    def _log_result(self, prompt: str, result: str):
        """Log a result to memory"""
        timestamp = datetime.now().isoformat()
        if 'results' not in self.memory:
            self.memory['results'] = []
        self.memory['results'].append({
            'timestamp': timestamp,
            'prompt': prompt,
            'result': result
        })

# Global instance
_agent_core = None

def get_agent_core() -> AgentCore:
    """Get the global agent core instance"""
    global _agent_core
    if _agent_core is None:
        _agent_core = AgentCore()
    return _agent_core

def handle_prompt(prompt: str) -> str:
    """Main function to handle prompts"""
    agent = get_agent_core()
    return agent.handle_prompt(prompt)