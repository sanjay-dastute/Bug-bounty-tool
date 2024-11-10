from typing import Dict, List
import os
from ..base import SecurityTool
from datetime import datetime

class ReconScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("recon", config)

    async def setup(self) -> bool:
        """Install and configure reconnaissance tools"""
        try:
            tools = [
                "subfinder",
                "amass",
                "assetfinder",
                "findomain",
                "altdns",
                "dnsx"
            ]

            # Update package list
            await self.execute_command(["sudo", "apt-get", "update"])

            # Install Go if not present (required for most tools)
            stdout, stderr = await self.execute_command(["which", "go"])
            if not stdout:
                await self.execute_command(["sudo", "apt-get", "install", "-y", "golang-go"])

            # Set up Go environment
            go_path = os.path.expanduser("~/go/bin")
            os.environ["PATH"] = f"{go_path}:{os.environ.get('PATH', '')}"

            # Install each tool
            for tool in tools:
                if tool == "subfinder":
                    await self.execute_command(["go", "install", "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"])
                elif tool == "amass":
                    await self.execute_command(["go", "install", "github.com/OWASP/Amass/v3/...@master"])
                elif tool == "assetfinder":
                    await self.execute_command(["go", "install", "github.com/tomnomnom/assetfinder@latest"])
                elif tool == "findomain":
                    await self.execute_command(["curl", "-LO", "https://github.com/findomain/findomain/releases/latest/download/findomain-linux"])
                    await self.execute_command(["chmod", "+x", "findomain-linux"])
                    await self.execute_command(["sudo", "mv", "findomain-linux", "/usr/local/bin/findomain"])
                elif tool == "altdns":
                    await self.execute_command(["pip3", "install", "py-altdns"])
                elif tool == "dnsx":
                    await self.execute_command(["go", "install", "github.com/projectdiscovery/dnsx/cmd/dnsx@latest"])

            return True
        except Exception as e:
            print(f"Failed to setup reconnaissance tools: {e}")
            return False

    async def scan(self, target: str) -> Dict:
        """Run all reconnaissance tools against a target"""
        results = {
            "tool": self.name,
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": []
        }

        # Run each tool
        tools = {
            "subfinder": ["subfinder", "-d", target],
            "amass": ["amass", "enum", "-d", target],
            "assetfinder": ["assetfinder", target],
            "findomain": ["findomain", "-t", target],
            "dnsx": ["dnsx", "-d", target]
        }

        for tool_name, command in tools.items():
            try:
                stdout, stderr = await self.execute_command(command)
                results["findings"].extend(self.parse_tool_output(tool_name, stdout))
            except Exception as e:
                print(f"Error running {tool_name}: {e}")

        return results


    def parse_tool_output(self, tool_name: str, output: str) -> List[Dict]:
        """Parse tool output into structured format"""
        findings = []
        for line in output.split('\n'):
            if line.strip():
                findings.append({
                    "source": tool_name,
                    "finding": line.strip()
                })
        return findings
