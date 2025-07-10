import bpy
import os
import sys
import json
from datetime import datetime

# Add the agent_core directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_core_dir = os.path.join(current_dir, "agent_core")
if agent_core_dir not in sys.path:
    sys.path.append(agent_core_dir)

class AgentBridge:
    """Bridge between Blender and Agent Zero core logic"""
    instance = None
    
    def __init__(self):
        self.agent_core = None
        self.memory_store = {}
        self.initialized = False
        AgentBridge.instance = self
        
    def initialize(self):
        """Initialize the agent core and memory system"""
        try:
            # Import the agent core
            from .agent_core import main as agent_main
            self.agent_core = agent_main
            self.initialized = True
            
            # Initialize memory store
            self._load_memory()
            
            print("ForgeCore AI: Agent bridge initialized successfully")
            
        except Exception as e:
            print(f"ForgeCore AI: Error initializing agent bridge: {e}")
            self.initialized = False
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self._save_memory()
            self.initialized = False
            print("ForgeCore AI: Agent bridge cleaned up")
        except Exception as e:
            print(f"ForgeCore AI: Error during cleanup: {e}")
    
    def handle_prompt(self, prompt: str) -> str:
        """Handle a prompt and return Blender code to execute"""
        if not self.initialized:
            return "# Error: Agent bridge not initialized"
        
        try:
            # Log the prompt
            self._log_prompt(prompt)
            
            # Process the prompt through Agent Zero core
            blender_code = self.agent_core.handle_prompt(prompt)
            
            # Log the result
            self._log_result(prompt, blender_code)
            
            return blender_code
            
        except Exception as e:
            error_msg = f"# Error processing prompt: {str(e)}"
            self._log_result(prompt, error_msg)
            return error_msg
    
    def _log_prompt(self, prompt: str):
        """Log a prompt to memory"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'type': 'prompt',
            'content': prompt
        }
        
        if 'prompts' not in self.memory_store:
            self.memory_store['prompts'] = []
        
        self.memory_store['prompts'].append(log_entry)
        self._save_memory()
    
    def _log_result(self, prompt: str, result: str):
        """Log a result to memory"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'type': 'result',
            'prompt': prompt,
            'content': result
        }
        
        if 'results' not in self.memory_store:
            self.memory_store['results'] = []
        
        self.memory_store['results'].append(log_entry)
        self._save_memory()
    
    def _load_memory(self):
        """Load memory from file"""
        try:
            memory_dir = os.path.join(current_dir, "agent_core", "memory")
            memory_file = os.path.join(memory_dir, "memory_store.json")
            
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    self.memory_store = json.load(f)
            else:
                self.memory_store = {}
                
        except Exception as e:
            print(f"ForgeCore AI: Error loading memory: {e}")
            self.memory_store = {}
    
    def _save_memory(self):
        """Save memory to file"""
        try:
            memory_dir = os.path.join(current_dir, "agent_core", "memory")
            os.makedirs(memory_dir, exist_ok=True)
            memory_file = os.path.join(memory_dir, "memory_store.json")
            
            with open(memory_file, 'w') as f:
                json.dump(self.memory_store, f, indent=2)
                
        except Exception as e:
            print(f"ForgeCore AI: Error saving memory: {e}")
    
    def get_recent_prompts(self, limit: int = 5) -> list:
        """Get recent prompts from memory"""
        if 'prompts' in self.memory_store:
            return self.memory_store['prompts'][-limit:]
        return []
    
    def get_recent_results(self, limit: int = 5) -> list:
        """Get recent results from memory"""
        if 'results' in self.memory_store:
            return self.memory_store['results'][-limit:]
        return []

# Global instance
_agent_bridge = None

def initialize():
    """Initialize the global agent bridge"""
    global _agent_bridge
    _agent_bridge = AgentBridge()
    _agent_bridge.initialize()

def cleanup():
    """Cleanup the global agent bridge"""
    global _agent_bridge
    if _agent_bridge:
        _agent_bridge.cleanup()
        _agent_bridge = None

def get_bridge() -> AgentBridge:
    """Get the global agent bridge instance"""
    global _agent_bridge
    return _agent_bridge