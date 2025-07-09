"""
Mesh Generation Module - ForgeCore AI
Handles advanced mesh generation operations
"""

import bpy
from typing import Dict, List, Optional

class MeshGenerator:
    """Advanced mesh generation for ForgeCore AI"""
    
    def __init__(self):
        self.primitive_types = {
            'cube': self._create_cube,
            'sphere': self._create_sphere,
            'cylinder': self._create_cylinder,
            'cone': self._create_cone,
            'plane': self._create_plane,
            'torus': self._create_torus
        }
    
    def generate_mesh(self, mesh_type: str, **kwargs) -> str:
        """Generate Blender code for mesh creation"""
        mesh_type = mesh_type.lower()
        
        if mesh_type in self.primitive_types:
            return self.primitive_types[mesh_type](**kwargs)
        else:
            return self._create_custom_mesh(mesh_type, **kwargs)
    
    def _create_cube(self, **kwargs) -> str:
        """Generate cube creation code"""
        size = kwargs.get('size', 2.0)
        location = kwargs.get('location', (0, 0, 0))
        
        code_lines = [
            f"bpy.ops.mesh.primitive_cube_add(size={size}, location={location})",
            "cube = bpy.context.active_object",
            "cube.name = 'Generated_Cube'"
        ]
        
        # Add modifiers
        if kwargs.get('smooth', False):
            code_lines.extend([
                "modifier = cube.modifiers.new(name='Smooth', type='SUBSURF')",
                "modifier.levels = 2"
            ])
        
        return "\n".join(code_lines)
    
    def _create_sphere(self, **kwargs) -> str:
        """Generate sphere creation code"""
        radius = kwargs.get('radius', 1.0)
        location = kwargs.get('location', (0, 0, 0))
        segments = kwargs.get('segments', 32)
        rings = kwargs.get('rings', 16)
        
        code_lines = [
            f"bpy.ops.mesh.primitive_uv_sphere_add(radius={radius}, location={location}, segments={segments}, ring_count={rings})",
            "sphere = bpy.context.active_object",
            "sphere.name = 'Generated_Sphere'"
        ]
        
        return "\n".join(code_lines)
    
    def _create_cylinder(self, **kwargs) -> str:
        """Generate cylinder creation code"""
        radius = kwargs.get('radius', 1.0)
        depth = kwargs.get('depth', 2.0)
        location = kwargs.get('location', (0, 0, 0))
        
        code_lines = [
            f"bpy.ops.mesh.primitive_cylinder_add(radius={radius}, depth={depth}, location={location})",
            "cylinder = bpy.context.active_object",
            "cylinder.name = 'Generated_Cylinder'"
        ]
        
        return "\n".join(code_lines)
    
    def _create_cone(self, **kwargs) -> str:
        """Generate cone creation code"""
        radius1 = kwargs.get('radius1', 1.0)
        radius2 = kwargs.get('radius2', 0.0)
        depth = kwargs.get('depth', 2.0)
        location = kwargs.get('location', (0, 0, 0))
        
        code_lines = [
            f"bpy.ops.mesh.primitive_cone_add(radius1={radius1}, radius2={radius2}, depth={depth}, location={location})",
            "cone = bpy.context.active_object",
            "cone.name = 'Generated_Cone'"
        ]
        
        return "\n".join(code_lines)
    
    def _create_plane(self, **kwargs) -> str:
        """Generate plane creation code"""
        size = kwargs.get('size', 2.0)
        location = kwargs.get('location', (0, 0, 0))
        
        code_lines = [
            f"bpy.ops.mesh.primitive_plane_add(size={size}, location={location})",
            "plane = bpy.context.active_object",
            "plane.name = 'Generated_Plane'"
        ]
        
        return "\n".join(code_lines)
    
    def _create_torus(self, **kwargs) -> str:
        """Generate torus creation code"""
        major_radius = kwargs.get('major_radius', 1.0)
        minor_radius = kwargs.get('minor_radius', 0.25)
        location = kwargs.get('location', (0, 0, 0))
        
        code_lines = [
            f"bpy.ops.mesh.primitive_torus_add(major_radius={major_radius}, minor_radius={minor_radius}, location={location})",
            "torus = bpy.context.active_object",
            "torus.name = 'Generated_Torus'"
        ]
        
        return "\n".join(code_lines)
    
    def _create_custom_mesh(self, mesh_type: str, **kwargs) -> str:
        """Generate custom mesh creation code"""
        code_lines = [
            "# Custom mesh generation",
            f"print('ForgeCore AI: Creating custom mesh type: {mesh_type}')",
            "bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))",
            "obj = bpy.context.active_object",
            f"obj.name = 'Generated_{mesh_type.title()}'"
        ]
        
        return "\n".join(code_lines)

# Global instance
_mesh_generator = None

def get_mesh_generator() -> MeshGenerator:
    """Get the global mesh generator instance"""
    global _mesh_generator
    if _mesh_generator is None:
        _mesh_generator = MeshGenerator()
    return _mesh_generator