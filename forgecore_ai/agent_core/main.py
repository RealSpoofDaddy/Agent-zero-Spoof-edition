"""
ForgeCore AI - Main Agent Core
Adapted from Agent Zero for Blender integration
"""

import re
import json
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import os
import subprocess
import requests
import random
import logging
import threading
import time
import glob
import urllib.parse

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
            'utility': self._handle_utility,
            'knowledge': self._handle_knowledge_query,
            'tool': self._handle_tool,
            'procedural': self._handle_procedural,
            'scene_analysis': self._handle_scene_analysis
        }
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()
    
    def split_prompt(self, prompt: str) -> list:
        """Split a complex prompt into subtasks using conjunctions and punctuation."""
        # Simple split on 'and', ';', or '.'
        parts = re.split(r'\band\b|;|\.', prompt)
        return [p.strip() for p in parts if p.strip()]

    def _load_knowledge_base(self):
        """Load Blender knowledge base from a JSON file."""
        kb_path = os.path.join(os.path.dirname(__file__), '..', '..', 'knowledge', 'blender_faq.json')
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                import json
                return json.load(f)
        except Exception:
            return {}

    def _handle_knowledge_query(self, prompt: str) -> str:
        """Answer Blender/3D questions using the knowledge base."""
        # Simple keyword search
        q = prompt.lower().strip()
        for entry in self.knowledge_base.get('faqs', []):
            if q in entry['question'].lower():
                return entry['answer']
        # Fallback: try partial match
        for entry in self.knowledge_base.get('faqs', []):
            if any(word in entry['question'].lower() for word in q.split()):
                return entry['answer']
        return "Sorry, I don't know the answer to that question yet."

    def _handle_tool(self, prompt: str) -> str:
        """Handle custom tool requests: code execution, web search, file management."""
        prompt_lower = prompt.lower()
        # Safer code execution
        if 'run python' in prompt_lower or 'execute code' in prompt_lower:
            code = prompt.split(':', 1)[-1].strip()
            result = {'output': None, 'error': None}
            def run_code():
                try:
                    # Restrict built-ins
                    safe_builtins = {'print': print, 'range': range, 'len': len, 'str': str, 'int': int, 'float': float, 'bool': bool, 'list': list, 'dict': dict, 'set': set, 'tuple': tuple, 'enumerate': enumerate, 'abs': abs, 'min': min, 'max': max, 'sum': sum}
                    exec_globals = {'__builtins__': safe_builtins}
                    exec_locals = {}
                    exec(code, exec_globals, exec_locals)
                    result['output'] = exec_locals.get('result', 'Code executed.')
                except Exception as e:
                    result['error'] = f"Error executing code: {e}"
            thread = threading.Thread(target=run_code)
            thread.start()
            thread.join(timeout=3)  # 3 second timeout
            if thread.is_alive():
                return "Error: Code execution timed out."
            if result['error']:
                return result['error']
            return str(result['output'])
        # Batch file operations
        elif 'delete all' in prompt_lower and 'files' in prompt_lower:
            try:
                parts = prompt_lower.split('delete all')[-1].split('files')[0].strip()
                ext = parts if parts.startswith('.') else f'.{parts}' if parts else '.tmp'
                path = prompt.split('in', 1)[-1].strip() if 'in' in prompt_lower else '.'
                files = glob.glob(os.path.join(path, f'*{ext}'))
                for f in files:
                    os.remove(f)
                return f"Deleted {len(files)} files with extension {ext} in {path}"
            except Exception as e:
                logging.error(f"Batch file delete error: {e}")
                return f"Batch file delete error: {e}"
        # Web search improvements
        elif 'web search' in prompt_lower:
            try:
                # Engine selection
                engine = 'duckduckgo'
                if 'google' in prompt_lower:
                    engine = 'google'
                query = prompt.split(':', 1)[-1].strip()
                if engine == 'duckduckgo':
                    resp = requests.get(f'https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json')
                    if resp.ok:
                        data = resp.json()
                        abstract = data.get('AbstractText', '')
                        related = data.get('RelatedTopics', [])
                        if abstract:
                            return abstract
                        elif related:
                            # Show first related topic
                            topic = related[0]
                            if isinstance(topic, dict):
                                return f"{topic.get('Text', '')} ({topic.get('FirstURL', '')})"
                        return 'No summary found.'
                    return 'Web search failed.'
                elif engine == 'google':
                    # Placeholder: Google Custom Search API would be needed for real results
                    return f"Google search for '{query}' is not implemented (API key required)."
            except Exception as e:
                logging.error(f"Web search error: {e}")
                return f"Web search error: {e}"
        elif 'list files' in prompt_lower:
            path = prompt.split(':', 1)[-1].strip() or '.'
            try:
                files = os.listdir(path)
                return '\n'.join(files)
            except Exception as e:
                return f"File listing error: {e}"
        elif 'delete file' in prompt_lower:
            path = prompt.split(':', 1)[-1].strip()
            try:
                os.remove(path)
                return f"Deleted file: {path}"
            except Exception as e:
                return f"File deletion error: {e}"
        else:
            return "Unknown tool command."

    def _handle_procedural(self, prompt: str) -> str:
        """Advanced procedural content generation."""
        p = prompt.lower()
        if 'city' in p:
            return "# Generate a grid of cubes as buildings\nfor x in range(5):\n    for y in range(5):\n        bpy.ops.mesh.primitive_cube_add(size=1, location=(x*2, y*2, 0))\n"
        elif 'terrain' in p:
            return "# Generate random terrain\nimport random\nfor x in range(10):\n    for y in range(10):\n        z = random.uniform(0, 2)\n        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))\n"
        elif 'forest' in p:
            return "# Generate a forest of random trees\nimport random\nfor i in range(20):\n    x, y = random.uniform(-10, 10), random.uniform(-10, 10)\n    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=2, location=(x, y, 1))\n    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(x, y, 2))\n"
        elif 'spiral staircase' in p:
            return "# Generate a spiral staircase\nimport math\nsteps = 20\nradius = 2\nfor i in range(steps):\n    angle = i * (math.pi / 8)\n    x = math.cos(angle) * radius\n    y = math.sin(angle) * radius\n    z = i * 0.3\n    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(x, y, z))\n"
        elif 'scatter rocks' in p:
            return "# Scatter rocks on terrain\nimport random\nfor i in range(30):\n    x, y = random.uniform(-10, 10), random.uniform(-10, 10)\n    z = random.uniform(0, 1)\n    bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(0.2, 0.6), location=(x, y, z))\n"
        else:
            return "Procedural generation not implemented for this prompt."

    def _handle_scene_analysis(self, prompt: str) -> str:
        """Advanced scene analysis: list materials, unused meshes, animation data."""
        try:
            import bpy
            objects = [obj for obj in bpy.context.scene.objects]
            meshes = [obj for obj in objects if obj.type == 'MESH']
            lights = [obj for obj in objects if obj.type == 'LIGHT']
            cameras = [obj for obj in objects if obj.type == 'CAMERA']
            # Materials
            materials = set()
            for obj in meshes:
                for mat in getattr(obj.data, 'materials', []):
                    if mat:
                        materials.add(mat.name)
            # Unused meshes
            all_meshes = set(bpy.data.meshes.keys())
            used_meshes = set(obj.data.name for obj in meshes if hasattr(obj, 'data'))
            unused_meshes = all_meshes - used_meshes
            # Animation data
            animated = [obj.name for obj in objects if obj.animation_data and obj.animation_data.action]
            summary = f"Objects: {len(objects)}, Meshes: {len(meshes)}, Lights: {len(lights)}, Cameras: {len(cameras)}\n"
            summary += f"Materials used: {', '.join(materials) if materials else 'None'}\n"
            summary += f"Unused meshes: {', '.join(unused_meshes) if unused_meshes else 'None'}\n"
            summary += f"Animated objects: {', '.join(animated) if animated else 'None'}"
            return summary
        except Exception as e:
            logging.error(f"Scene analysis error: {e}")
            return f"Scene analysis error: {e}"

    def route_prompt(self, prompt: str) -> str:
        """Route a prompt to the appropriate handler and return Blender code. Supports multi-step prompts."""
        subtasks = self.split_prompt(prompt)
        if len(subtasks) > 1:
            # Multi-step: return a marker for sub-agent orchestration
            return json.dumps({'multi_step': True, 'subtasks': subtasks})
        
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
        elif any(word in prompt_lower for word in ['how do i', 'what is', 'how to', 'faq', 'question', 'explain']):
            return self._handle_knowledge_query(prompt)
        elif any(word in prompt_lower for word in ['tool', 'run python', 'execute code', 'web search', 'list files', 'delete file']):
            return self._handle_tool(prompt)
        if any(word in prompt_lower for word in ['generate city', 'generate terrain', 'procedural']):
            return self._handle_procedural(prompt)
        if any(word in prompt_lower for word in ['analyze scene', 'scene analysis', 'summarize scene']):
            return self._handle_scene_analysis(prompt)
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
        self.memory = self._load_memory()
        self.sub_agents = {}  # Track sub-agents by UUID
        self.sub_agent_results = []
        self.history = self.memory.get('history', [])
    
    def _load_memory(self):
        """Load persistent memory/history from file."""
        mem_path = os.path.join(os.path.dirname(__file__), 'memory', 'memory_store.json')
        if os.path.exists(mem_path):
            try:
                with open(mem_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_memory(self):
        """Save persistent memory/history to file."""
        mem_path = os.path.join(os.path.dirname(__file__), 'memory', 'memory_store.json')
        try:
            with open(mem_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2)
        except Exception:
            pass

    def handle_prompt(self, prompt: str) -> str:
        """Main entry point for handling prompts. Supports multi-agent orchestration."""
        try:
            self._log_prompt(prompt)
            router_result = self.router.route_prompt(prompt)
            # Check for multi-step marker
            if isinstance(router_result, str):
                try:
                    router_result_json = json.loads(router_result)
                except Exception:
                    router_result_json = None
            else:
                router_result_json = None
            if router_result_json and router_result_json.get('multi_step'):
                # Multi-agent orchestration
                subtasks = router_result_json['subtasks']
                self.sub_agent_results = []
                for subtask in subtasks:
                    sub_agent_id = str(uuid.uuid4())
                    sub_agent = AgentCore()
                    self.sub_agents[sub_agent_id] = sub_agent
                    result = sub_agent.handle_prompt(subtask)
                    self.sub_agent_results.append({'id': sub_agent_id, 'prompt': subtask, 'result': result})
                # Aggregate all results into a single script
                all_code = '\n\n'.join([r['result'] for r in self.sub_agent_results])
                self._log_result(prompt, all_code)
                return all_code
            
            blender_code = router_result if isinstance(router_result, str) else str(router_result)
            safe_code = self._wrap_code_safely(blender_code)
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

    def get_sub_agent_activity(self):
        """Return a summary of sub-agent activity/results."""
        return self.sub_agent_results

    def get_history(self):
        return self.history

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