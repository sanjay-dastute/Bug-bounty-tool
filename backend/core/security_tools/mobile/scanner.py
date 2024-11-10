from typing import Dict, List
import os
import json
from ..base import SecurityTool
from datetime import datetime

class MobileScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("mobile", config)

    async def setup(self) -> bool:
        """Install and configure mobile security tools"""
        try:
            # Update package list
            await self.execute_command(["sudo", "apt-get", "update"])

            # Install APKLeaks
            await self.execute_command(["pip3", "install", "apkleaks"])

            # Install Frida
            await self.execute_command(["pip3", "install", "frida-tools"])

            # Install Objection
            await self.execute_command(["pip3", "install", "objection"])

            return True
        except Exception as e:
            print(f"Failed to setup mobile security tools: {e}")
            return False

    async def scan(self, target: str, tool: str = None) -> Dict:
        """Run mobile security scan with specified tool"""
        results = {
            "tool": self.name,
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": []
        }

        if tool == "apkleaks":
            stdout, stderr = await self.execute_command(["apkleaks", "-f", target])
            results["findings"].extend(self.parse_apkleaks_output(stdout))
        elif tool == "frida":
            # Frida requires a running process, handled separately
            pass
        elif tool == "objection":
            # Objection requires an active device connection, handled separately
            pass

        return results

    def parse_apkleaks_output(self, output: str) -> List[Dict]:
        findings = []
        current_pattern = None
        for line in output.split('\n'):
            if line.startswith('[+]'):
                current_pattern = line.replace('[+]', '').strip()
            elif line.strip() and current_pattern:
                findings.append({
                    "pattern": current_pattern,
                    "match": line.strip()
                })
        return findings

    async def run_frida_script(self, package_name: str, script_path: str) -> Dict:
        """Run Frida script on target application"""
        stdout, stderr = await self.execute_command([
            "frida", "-U", "-l", script_path, "-f", package_name
        ])
        return {
            "tool": "frida",
            "package": package_name,
            "output": stdout
        }

    async def run_objection_commands(self, package_name: str, commands: List[str]) -> Dict:
        """Run Objection commands on target application"""
        results = []
        for cmd in commands:
            stdout, stderr = await self.execute_command([
                "objection", "-g", package_name, "run", cmd
            ])
            results.append({
                "command": cmd,
                "output": stdout
            })
        return {
            "tool": "objection",
            "package": package_name,
            "results": results
        }
