import bpy
from bpy.types import Operator
import os

class FORGECORE_OT_export_scene(Operator):
    bl_idname = "forgecore.export_scene"
    bl_label = "Export Scene"
    bl_description = "Export scene to Unity/Unreal ready formats"
    
    def execute(self, context):
        try:
            # Get the filepath
            blend_filepath = bpy.data.filepath
            if not blend_filepath:
                self.report({'ERROR'}, "Please save the blend file first")
                return {'CANCELLED'}
            
            # Create export directory
            blend_dir = os.path.dirname(blend_filepath)
            export_dir = os.path.join(blend_dir, "exports")
            os.makedirs(export_dir, exist_ok=True)
            
            # Export as FBX for Unity
            fbx_path = os.path.join(export_dir, "scene_unity.fbx")
            bpy.ops.export_scene.fbx(
                filepath=fbx_path,
                use_selection=False,
                use_active_collection=False,
                global_scale=1.0,
                apply_unit_scale=True,
                apply_scale_options='FBX_SCALE_ALL',
                bake_space_transform=False,
                object_types={'MESH', 'ARMATURE', 'EMPTY', 'CAMERA', 'LIGHT'},
                use_mesh_modifiers=True,
                mesh_smooth_type='OFF',
                use_tspace=True,
                use_custom_props=True,
                add_leaf_bones=False,
                primary_bone_axis='Y',
                secondary_bone_axis='X',
                use_armature_deform_only=False,
                bake_anim=True,
                bake_anim_use_all_bones=True,
                bake_anim_use_nla_strips=True,
                bake_anim_use_all_actions=True,
                bake_anim_force_startend_keying=True,
                bake_anim_step=1.0,
                bake_anim_simplify_factor=1.0,
                path_mode='AUTO',
                embed_textures=False,
                batch_mode='OFF',
                use_metadata=True
            )
            
            # Export as FBX for Unreal (different settings)
            fbx_unreal_path = os.path.join(export_dir, "scene_unreal.fbx")
            bpy.ops.export_scene.fbx(
                filepath=fbx_unreal_path,
                use_selection=False,
                use_active_collection=False,
                global_scale=100.0,  # Unreal uses cm, Blender uses m
                apply_unit_scale=True,
                apply_scale_options='FBX_SCALE_ALL',
                bake_space_transform=True,
                object_types={'MESH', 'ARMATURE', 'EMPTY', 'CAMERA', 'LIGHT'},
                use_mesh_modifiers=True,
                mesh_smooth_type='OFF',
                use_tspace=True,
                use_custom_props=True,
                add_leaf_bones=False,
                primary_bone_axis='Y',
                secondary_bone_axis='X',
                use_armature_deform_only=False,
                bake_anim=True,
                bake_anim_use_all_bones=True,
                bake_anim_use_nla_strips=True,
                bake_anim_use_all_actions=True,
                bake_anim_force_startend_keying=True,
                bake_anim_step=1.0,
                bake_anim_simplify_factor=1.0,
                path_mode='AUTO',
                embed_textures=False,
                batch_mode='OFF',
                use_metadata=True
            )
            
            self.report({'INFO'}, f"Scene exported to {export_dir}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}