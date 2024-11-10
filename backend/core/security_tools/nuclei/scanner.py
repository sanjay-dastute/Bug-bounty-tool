from typing import Dict, List
import json
import os
from ..base import SecurityTool
from datetime import datetime

class NucleiScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("nuclei", config)
        self.templates_dir = os.path.expanduser("~/.nuclei-templates")
        self.severity_levels = ["critical", "high", "medium", "low", "info"]

    async def setup(self) -> bool:
        """Install and configure Nuclei"""
        try:
            # Check if Nuclei is installed
            stdout, stderr = await self.execute_command(["which", "nuclei"])
            if not stdout:
                # Install Go if not present
                await self.execute_command(["sudo", "apt-get", "update"])
                await self.execute_command(["sudo", "apt-get", "install", "-y", "golang-go"])

                # Install Nuclei
                go_path = os.path.expanduser("~/go/bin")
                os.environ["PATH"] = f"{go_path}:{os.environ.get('PATH', '')}"
                await self.execute_command(["go", "install", "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"])

            # Update templates
            await self.execute_command(["nuclei", "-update-templates"])
            return True
        except Exception as e:
            print(f"Failed to setup Nuclei: {e}")
            return False

    async def scan(self, target: str, severity: List[str] = None, tags: List[str] = None) -> Dict:
        """Execute Nuclei scan with specified options"""
        command = ["nuclei", "-u", target, "-json"]

        # Add severity filters
        if severity:
            valid_severities = [s for s in severity if s.lower() in self.severity_levels]
            if valid_severities:
                command.extend(["-severity", ",".join(valid_severities)])

        # Add tag filters
        if tags:
            command.extend(["-tags", ",".join(tags)])

        stdout, stderr = await self.execute_command(command)
        results = await self.parse_results(stdout)

        return {
            "tool": self.name,
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": results,
            "raw_output": stdout,
            "errors": stderr
        }

    async def parse_results(self, raw_output: str) -> List[Dict]:
        """Parse Nuclei scan results"""
        findings = []
        for line in raw_output.split('\n'):
            if not line.strip():
                continue

            try:
                result = json.loads(line)
                finding = {
                    "template_id": result.get("template-id"),
                    "template_name": result.get("info", {}).get("name"),
                    "severity": result.get("info", {}).get("severity", "unknown"),
                    "type": result.get("type"),
                    "matched": result.get("matched"),
                    "description": result.get("info", {}).get("description"),
                    "tags": result.get("info", {}).get("tags", []),
                    "reference": result.get("info", {}).get("reference", []),
                    "cwe_id": result.get("info", {}).get("classification", {}).get("cwe-id"),
                    "cvss_metrics": result.get("info", {}).get("classification", {}).get("cvss-metrics"),
                    "cvss_score": result.get("info", {}).get("classification", {}).get("cvss-score"),
                    "timestamp": result.get("timestamp")
                }
                findings.append(finding)
            except json.JSONDecodeError:
                continue

        return findings

    async def list_templates(self, severity: List[str] = None, tags: List[str] = None) -> List[Dict]:
        """List available Nuclei templates"""
        command = ["nuclei", "-tl"]
        if severity:
            command.extend(["-severity", ",".join(severity)])
        if tags:
            command.extend(["-tags", ",".join(tags)])

        stdout, stderr = await self.execute_command(command)
        templates = []

        for line in stdout.split('\n'):
            if line.strip() and "[" in line and "]" in line:
                try:
                    template_info = line.split(']', 1)[1].strip()
                    severity = line[line.find('[')+1:line.find(']')]
                    templates.append({
                        "name": template_info,
                        "severity": severity
                    })
                except Exception:
                    continue

        return templates

    async def update_templates(self) -> bool:
        """Update Nuclei templates"""
        try:
            stdout, stderr = await self.execute_command(["nuclei", "-update-templates"])
            return "Successfully updated nuclei-templates" in stdout
        except Exception as e:
            print(f"Failed to update templates: {e}")
            return False

    async def custom_template_scan(self, target: str, template_path: str) -> Dict:
        """Run scan with custom template"""
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")

        command = ["nuclei", "-u", target, "-t", template_path, "-json"]
        stdout, stderr = await self.execute_command(command)
        results = await self.parse_results(stdout)

        return {
            "tool": self.name,
            "target": target,
            "template": template_path,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": results,
            "raw_output": stdout,
            "errors": stderr
        }
