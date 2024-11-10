import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import asyncio
import subprocess
from datetime import datetime

class SecurityTool(ABC):
    def __init__(self, name: str, config: Dict):
        self.name = name
        self.config = config
        self.process: Optional[asyncio.subprocess.Process] = None

    @abstractmethod
    async def setup(self) -> bool:
        """Install and configure the security tool"""
        pass

    @abstractmethod
    async def scan(self, target: str) -> Dict:
        """Execute the security scan"""
        pass

    @abstractmethod
    async def parse_results(self, raw_output: str) -> List[Dict]:
        """Parse the scan results"""
        pass

    async def execute_command(self, command: List[str]) -> tuple[str, str]:
        """Execute a shell command and return stdout and stderr"""
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode(), stderr.decode()

class ToolOrchestrator:
    def __init__(self):
        self.tools: Dict[str, SecurityTool] = {}

    def register_tool(self, tool: SecurityTool):
        """Register a security tool with the orchestrator"""
        self.tools[tool.name] = tool

    async def setup_tools(self) -> Dict[str, bool]:
        """Set up all registered tools"""
        setup_results = {}
        for name, tool in self.tools.items():
            setup_results[name] = await tool.setup()
        return setup_results

    async def scan_target(self, target: str) -> List[Dict]:
        """Run all registered tools against a target"""
        results = []
        for tool in self.tools.values():
            try:
                result = await tool.scan(target)
                results.append(result)
            except Exception as e:
                results.append({
                    "tool": tool.name,
                    "target": target,
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": str(e)
                })
        return results
