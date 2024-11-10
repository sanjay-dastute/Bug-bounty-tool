# UI and Database Specifications

## UI Design (Based on Sn1per and Nuclei)

### Dashboard Layout
```
+----------------------------------------+
|  Logo    Search    Profile    Settings  |
+----------------------------------------+
|        |                               |
| Nav    |     Active Scans Panel        |
| Bar    |                               |
|        +-------------------------------+
|        |                               |
|        |     Vulnerability Feed        |
|        |                               |
|        +-------------------------------+
|        |                               |
|        |     Statistics & Metrics      |
|        |                               |
+----------------------------------------+
```

### Key UI Components

1. **Navigation Bar**
   - Scan Management
   - Vulnerability Database
   - Reports
   - Tools Configuration
   - Settings

2. **Active Scans Panel**
   - Real-time scan progress
   - Target information
   - Tool status indicators
   - Cancel/Pause controls

3. **Vulnerability Feed**
   - Real-time findings
   - Severity indicators
   - Quick actions
   - Filtering options

4. **Manual Testing Interface**
   - Custom payload input
   - Request/Response viewer
   - Parameter manipulation
   - Authentication token manager

### Theme and Styling
- Dark mode (default)
- Light mode option
- Responsive design for all screen sizes

## Open-Source Database Integration

### Primary Vulnerability Databases
1. **National Vulnerability Database (NVD)**
   ```python
   class NVDDatabase:
       def __init__(self):
           self.api_endpoint = "https://services.nvd.nist.gov/rest/json/cves/2.0"
           self.update_interval = 24  # hours

       async def fetch_vulnerabilities(self, cpe: str) -> List[Vulnerability]:
           pass

       async def update_local_cache(self):
           pass
   ```

2. **CVE Details Integration**
   ```python
   class CVEDatabase:
       def __init__(self):
           self.local_db_path = "data/cve_database.sqlite"
           self.last_update = None

       async def search_by_product(self, product: str) -> List[CVE]:
           pass
   ```

3. **Exploit Database**
   ```python
   class ExploitDB:
       def __init__(self):
           self.github_repo = "offensive-security/exploit-database"
           self.local_path = "data/exploit-db"

       async def find_exploits(self, cve_id: str) -> List[Exploit]:
           pass
   ```

### Custom Database Components

1. **Local Cache System**
   ```python
   class VulnerabilityCache:
       def __init__(self):
           self.db_engine = create_engine("sqlite:///data/vulnerability_cache.db")
           self.Session = sessionmaker(bind=self.db_engine)

       def cache_vulnerability(self, vuln: Vulnerability):
           pass

       def get_cached_vulnerabilities(self, target: str) -> List[Vulnerability]:
           pass
   ```

2. **Aggregator Service**
   ```python
   class VulnerabilityAggregator:
       def __init__(self):
           self.sources = [
               NVDDatabase(),
               CVEDatabase(),
               ExploitDB()
           ]

       async def comprehensive_search(self, target: str) -> AggregatedResults:
           pass
   ```

### Database Schema

```sql
-- Vulnerabilities Table
CREATE TABLE vulnerabilities (
    id TEXT PRIMARY KEY,
    cve_id TEXT,
    description TEXT,
    affected_components TEXT,
    discovery_date DATE,
    remediation TEXT,
    technical_details TEXT
);

-- Exploits Table
CREATE TABLE exploits (
    id TEXT PRIMARY KEY,
    vulnerability_id TEXT,
    exploit_type TEXT,
    payload TEXT,
    requirements TEXT,
    reproduction_steps TEXT,
    FOREIGN KEY (vulnerability_id) REFERENCES vulnerabilities(id)
);

-- Scan Results Table
CREATE TABLE scan_results (
    id TEXT PRIMARY KEY,
    target TEXT,
    scan_date TIMESTAMP,
    vulnerability_id TEXT,
    status TEXT,
    notes TEXT,
    FOREIGN KEY (vulnerability_id) REFERENCES vulnerabilities(id)
);
```

## Manual Testing Features

### Custom Test Creation
1. **Payload Management**
   - Custom payload creation
   - Payload templates
   - Payload generation rules

2. **Request Builder**
   - HTTP method selection
   - Header manipulation
   - Parameter fuzzing
   - Authentication handling

3. **Response Analysis**
   - Pattern matching
   - Response comparison
   - Difference highlighting
   - Export capabilities

### Test Automation
1. **Custom Test Cases**
   ```python
   class CustomTest:
       def __init__(self):
           self.name = str
           self.description = str
           self.steps = List[TestStep]
           self.validation = List[ValidationRule]

       async def execute(self, target: str) -> TestResult:
           pass
   ```

2. **Test Sequence Builder**
   ```python
   class TestSequence:
       def __init__(self):
           self.tests = List[CustomTest]
           self.dependencies = Dict[str, List[str]]


       async def run_sequence(self, target: str) -> SequenceResult:
           pass
   ```

## Integration with Existing Tools

### Tool Wrapper Interface
```python
class ToolWrapper:
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.config = self.load_config()
        self.results_parser = ResultsParser()

    async def execute(self, target: str) -> Results:
        pass

    def parse_results(self, raw_output: str) -> ParsedResults:
        pass
```

### Results Integration
```python
class ResultsIntegrator:
    def __init__(self):
        self.tools = Dict[str, ToolWrapper]
        self.aggregator = VulnerabilityAggregator()

    async def integrate_results(self,
                              tool_results: List[Results],
                              manual_results: List[TestResult]) -> Report:
        pass
```

This specification complements the development plan with detailed UI design similar to Sn1per and Nuclei, comprehensive open-source database integration, and manual testing capabilities. The design ensures effective vulnerability scanning while maintaining user-friendly interaction patterns familiar to users of existing tools.
