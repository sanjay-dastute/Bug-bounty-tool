from typing import Dict, List
import json
import os
from ..base import SecurityTool
from datetime import datetime

class MythrilScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("mythril", config)
        self.infura_key = config.get("infura_key", "")

    async def setup(self) -> bool:
        """Install and configure Mythril"""
        try:
            # Check if Python and pip are installed
            stdout, stderr = await self.execute_command(["which", "pip3"])
            if not stdout:
                await self.execute_command(["sudo", "apt-get", "update"])
                await self.execute_command(["sudo", "apt-get", "install", "-y", "python3-pip"])

            # Install Mythril
            await self.execute_command(["pip3", "install", "mythril"])

            # Verify installation
            stdout, stderr = await self.execute_command(["myth", "version"])
            return "Mythril version" in stdout

        except Exception as e:
            print(f"Failed to setup Mythril: {e}")
            return False

    async def scan(self, target: str, mode: str = "standard") -> Dict:
        """Scan smart contract for vulnerabilities"""
        if not os.path.exists(target) and not target.startswith("0x"):
            raise ValueError("Target must be a file path or contract address")

        command = ["myth", "analyze"]

        # Add mode-specific options
        if mode == "quick":
            command.extend(["--execution-timeout", "90"])
        elif mode == "deep":
            command.extend(["--execution-timeout", "900", "--max-depth", "50"])

        # Handle different target types
        if target.startswith("0x"):
            if not self.infura_key:
                raise ValueError("Infura API key required for scanning deployed contracts")
            command.extend(["--rpc", f"infura-mainnet:{self.infura_key}", target])
        else:
            command.append(target)

        # Add JSON output format
        command.extend(["--format", "json"])

        stdout, stderr = await self.execute_command(command)
        try:
            results = json.loads(stdout)
        except json.JSONDecodeError:
            results = {"error": "Failed to parse Mythril output", "raw": stdout}

        return {
            "tool": self.name,
            "target": target,
            "mode": mode,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": await self.parse_results(results),
            "raw_output": results
        }

    async def parse_results(self, results: Dict) -> List[Dict]:
        """Parse Mythril scan results"""
        findings = []

        if isinstance(results, list):
            for issue in results:
                finding = {
                    "title": issue.get("title", "Unknown"),
                    "description": issue.get("description", ""),
                    "severity": self._map_severity(issue.get("severity", "Unknown")),
                    "swc_id": issue.get("swc-id"),
                    "swc_title": issue.get("swc-title"),
                    "contract": issue.get("contract"),
                    "function": issue.get("function"),
                    "address": issue.get("address"),
                    "code": issue.get("code"),
                    "transaction_sequence": issue.get("transaction_sequence")
                }
                findings.append(finding)

        return findings

    def _map_severity(self, severity: str) -> str:
        """Map Mythril severity levels to standard levels"""
        severity_map = {
            "High": "critical",
            "Medium": "high",
            "Low": "medium",
            "Unknown": "low"
        }
        return severity_map.get(severity, "low")

    async def scan_truffle_project(self, project_path: str) -> List[Dict]:
        """Scan all contracts in a Truffle project"""
        if not os.path.exists(os.path.join(project_path, "truffle-config.js")):
            raise ValueError("Not a valid Truffle project directory")

        contracts_dir = os.path.join(project_path, "contracts")
        results = []

        for root, _, files in os.walk(contracts_dir):
            for file in files:
                if file.endswith(".sol"):
                    contract_path = os.path.join(root, file)
                    try:
                        result = await self.scan(contract_path)
                        results.append(result)
                    except Exception as e:
                        results.append({
                            "tool": self.name,
                            "target": contract_path,
                            "timestamp": datetime.utcnow().isoformat(),
                            "error": str(e)
                        })

        return results

    async def scan_hardhat_project(self, project_path: str) -> List[Dict]:
        """Scan all contracts in a Hardhat project"""
        if not os.path.exists(os.path.join(project_path, "hardhat.config.js")):
            raise ValueError("Not a valid Hardhat project directory")

        contracts_dir = os.path.join(project_path, "contracts")
        results = []

        for root, _, files in os.walk(contracts_dir):
            for file in files:
                if file.endswith(".sol"):
                    contract_path = os.path.join(root, file)
                    try:
                        result = await self.scan(contract_path)
                        results.append(result)
                    except Exception as e:
                        results.append({
                            "tool": self.name,
                            "target": contract_path,
                            "timestamp": datetime.utcnow().isoformat(),
                            "error": str(e)
                        })

        return results

    async def verify_contract(self, address: str, source_code: str) -> Dict:
        """Verify deployed contract against source code"""
        # Create temporary file for source code
        temp_file = f"/tmp/contract_{address}.sol"
        try:
            with open(temp_file, "w") as f:
                f.write(source_code)

            # Scan both deployed contract and source
            deployed_result = await self.scan(address)
            source_result = await self.scan(temp_file)

            return {
                "tool": self.name,
                "target": address,
                "timestamp": datetime.utcnow().isoformat(),
                "deployed_findings": deployed_result["findings"],
                "source_findings": source_result["findings"],
                "verification_result": self._compare_results(
                    deployed_result["findings"],
                    source_result["findings"]
                )
            }
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def _compare_results(self, deployed_findings: List[Dict], source_findings: List[Dict]) -> Dict:
        """Compare findings between deployed contract and source code"""
        return {
            "match": len(deployed_findings) == len(source_findings),
            "deployed_issues_count": len(deployed_findings),
            "source_issues_count": len(source_findings),
            "differences": self._find_differences(deployed_findings, source_findings)
        }

    def _find_differences(self, deployed_findings: List[Dict], source_findings: List[Dict]) -> List[Dict]:
        """Find differences between deployed and source findings"""
        differences = []
        deployed_titles = {f["title"] for f in deployed_findings}
        source_titles = {f["title"] for f in source_findings}

        # Issues in deployed but not in source
        for title in deployed_titles - source_titles:
            differences.append({
                "type": "deployed_only",
                "title": title
            })

        # Issues in source but not in deployed
        for title in source_titles - deployed_titles:
            differences.append({
                "type": "source_only",
                "title": title
            })

        return differences
