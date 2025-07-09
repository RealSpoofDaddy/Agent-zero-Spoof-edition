# ForgeCore AI - Blender Plugin

A powerful AI assistant for Blender that transforms natural language prompts into 3D content creation. Built on the Agent Zero framework, ForgeCore AI provides intelligent mesh generation, material creation, scene layout, and more.

## Features

### 🤖 AI-Powered Content Creation
- **Natural Language Processing**: Describe what you want in plain English
- **Mesh Generation**: Create cubes, spheres, cylinders, and custom objects
- **Material Creation**: Generate materials with specific properties (metal, plastic, glass, etc.)
- **Scene Layout**: Automatically arrange objects, cameras, and lighting
- **Animation**: Create simple animations with keyframes

### 📝 Development Journal
- **Goal Tracking**: Set daily goals and track progress
- **Progress Logging**: Save notes and achievements
- **Memory System**: Persistent storage of your development journey

### 🛠️ Advanced Features
- **Export Integration**: Export to Unity/Unreal ready formats
- **Modular Design**: Easy to extend with new capabilities
- **Error Handling**: Robust error handling and user feedback
- **Memory System**: Learns from your usage patterns

## Installation

### Method 1: Manual Installation
1. Download the `forgecore_ai` folder
2. Open Blender
3. Go to Edit > Preferences > Add-ons
4. Click "Install" and select the `forgecore_ai` folder
5. Enable the addon by checking the box

### Method 2: Development Installation
1. Clone or download the repository
2. Copy the `forgecore_ai` folder to your Blender addons directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.4\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/4.4/scripts/addons/`
   - **Linux**: `~/.config/blender/4.4/scripts/addons/`
3. Restart Blender
4. Enable the addon in Preferences > Add-ons

## Usage

### Basic Usage

1. **Open the Panel**: In the 3D Viewport, press `N` to open the sidebar
2. **Navigate to ForgeCore AI**: Click on the "ForgeCore AI" tab
3. **Enter a Prompt**: Type your request in natural language
4. **Execute**: Click "Run Prompt" to generate and execute the code

### Example Prompts

#### Mesh Generation
```
"Create a red cube with smooth shading"
"Make a large sphere at position (5, 0, 0)"
"Generate a cylinder with beveled edges"
```

#### Material Creation
```
"Create a metallic material for the selected objects"
"Make a glass material with blue tint"
"Generate a plastic material with high roughness"
```

#### Scene Setup
```
"Set up studio lighting for the scene"
"Arrange all objects in a grid layout"
"Add a camera with dramatic angle"
```

#### Animation
```
"Animate the selected objects moving up and down"
"Create a rotation animation for the cube"
```

### Development Journal

1. **Set Goals**: Enter your daily development goals
2. **Track Progress**: Log your achievements and notes
3. **Review History**: View your recent journal entries

## Architecture

### Core Components

```
forgecore_ai/
├── __init__.py              # Main addon entry point
├── ui_panel.py              # Blender UI panels
├── agent_bridge.py          # Connects Blender to AI core
├── ops/
│   ├── run_prompt.py        # Prompt execution operator
│   └── export_scene.py      # Export functionality
└── agent_core/
    ├── main.py              # Main AI logic
    ├── memory/              # Memory system
    └── modules/             # Extensible modules
```

### Agent Zero Integration

ForgeCore AI is built on the Agent Zero framework, adapted for Blender:

- **Prompt Routing**: Intelligent routing of prompts to appropriate handlers
- **Code Generation**: Safe Blender Python code generation
- **Memory System**: Persistent learning and storage
- **Modular Design**: Easy to extend with new capabilities

## Development

### Adding New Modules

1. Create a new file in `agent_core/modules/`
2. Implement your module following the existing pattern
3. Register it in the main router
4. Test with various prompts

### Example Module

```python
# agent_core/modules/my_module.py
class MyModule:
    def handle_prompt(self, prompt: str) -> str:
        # Your logic here
        return "bpy.ops.mesh.primitive_cube_add()"
```

### Extending the UI

1. Add new panels in `ui_panel.py`
2. Create corresponding operators in `ops/`
3. Register them in `__init__.py`

## Troubleshooting

### Common Issues

**Plugin not appearing in addons list**
- Ensure the folder structure is correct
- Check that `__init__.py` contains proper `bl_info`

**Prompts not working**
- Check the Blender console for error messages
- Ensure you're in the correct mode (Object mode recommended)

**Memory not persisting**
- Check file permissions in the addon directory
- Verify the memory directory exists

### Debug Mode

Enable debug mode by adding this to the console:
```python
import bpy
bpy.context.scene.forgecore_debug = True
```

## Future Enhancements

### Planned Features
- **Advanced AI Integration**: Connect to external AI services
- **Texture Generation**: AI-powered texture creation
- **Animation Tools**: More sophisticated animation capabilities
- **Rigging Assistant**: AI-powered character rigging
- **Scene Analysis**: Analyze existing scenes and suggest improvements

### Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is based on the Agent Zero framework and is licensed under the same terms.

## Acknowledgments

- **Agent Zero Team**: For the original AI framework
- **Blender Foundation**: For the amazing 3D software
- **Blender Community**: For inspiration and support

## Support

For issues, questions, or contributions:
- Create an issue on the repository
- Join our community discussions
- Check the documentation for common solutions

---

**ForgeCore AI** - Transforming natural language into 3D reality in Blender.