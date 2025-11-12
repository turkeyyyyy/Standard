# What Are These Validators For?

## 🎯 Purpose

The **JSON Agents Validator** ensures that agent manifest files (Portable Agent Manifests) are **correct, complete, and compliant** with the JSON Agents specification.

Think of it as a **quality control system** for agent configuration files - catching errors before they cause problems in production.

---

## 💡 The Problem

When building AI agents, you need to describe:
- ✅ What the agent can do (capabilities)
- ✅ What tools it can access
- ✅ Its security policies
- ✅ How it connects to other agents
- ✅ Its runtime requirements

Without validation, manifests can have:
- ❌ **Typos**: `capabilties` instead of `capabilities`
- ❌ **Missing fields**: Forgot to include `manifest_version`
- ❌ **Invalid URIs**: `http://example.com/agent` instead of `ajson://example.com/agent`
- ❌ **Broken policies**: `tool.type === 'http'` (triple equals is invalid)
- ❌ **Schema violations**: Wrong data types, missing required properties

These errors might not be caught until runtime, causing:
- 💥 Agent frameworks rejecting your manifest
- 🐛 Subtle bugs in agent behavior
- 🔒 Security policy bypasses
- 🔗 Failed agent-to-agent communication

---

## ✅ The Solution

The validator catches these issues **before deployment**:

### Example: Invalid Manifest

```json
{
  "manifest_version": "1.0",
  "agent": {
    "id": "not-a-valid-uri",
    "name": "Broken Agent"
  },
  "capabilities": [
    {
      "id": "qa",
      "description": "Answer questions",
      "policy": {
        "where": "tool.type === 'http'"
      }
    }
  ]
}
```

### Validator Output

```
❌ example-broken.json - INVALID

Errors:
  • Missing required field: 'profiles'
  • Invalid URI scheme. Expected 'ajson://', got: none
  • Policy expression error: Invalid operator '===' (use '==' for equality)
  • Schema violation: 'policy' not allowed in core profile
```

### Fixed Manifest

```json
{
  "manifest_version": "1.0",
  "profiles": ["core"],
  "agent": {
    "id": "ajson://example.com/agents/qa-agent",
    "name": "QA Agent",
    "version": "1.0.0"
  },
  "capabilities": [
    {
      "id": "qa",
      "description": "Answer questions"
    }
  ],
  "modalities": {
    "input": ["text"],
    "output": ["text"]
  }
}
```

```
✅ example.json - VALID
```

---

## 🛠️ What The Validator Checks

### 1. JSON Schema Validation
- ✅ Required fields present (`manifest_version`, `profiles`, `agent`)
- ✅ Correct data types (strings, arrays, objects)
- ✅ Profile-specific requirements (core, exec, gov, graph)
- ✅ Capability schemas match registered types
- ✅ Extension namespaces (`x-*`) properly structured

### 2. URI Validation (Section 16)
- ✅ Correct scheme (`ajson://`)
- ✅ Valid authority (domain or localhost)
- ✅ Proper path structure
- ✅ RFC 3986 compliance
- ✅ HTTPS transformation rules

### 3. Policy Expression Validation (Appendix B)
- ✅ Grammar compliance (16 operators)
- ✅ Correct operators (`==`, `!=`, `~`, `in`, etc.)
- ✅ Variable references (`tool.*`, `message.*`, etc.)
- ✅ Logical expressions (`&&`, `||`, `not`)
- ✅ Parentheses balancing

### 4. Semantic Validation
- ✅ Cross-field consistency
- ✅ Capability references valid
- ✅ Tool definitions complete
- ⚠️ Warnings for best practices

---

## 🎯 Who Needs This?

### 1. **Agent Developers**
Validate manifests during development:
```bash
jsonagents validate my-agent.json
```

### 2. **Framework Implementers**
Integrate validation into SDKs:
```python
from jsonagents import validate_manifest

def load_agent(path):
    result = validate_manifest(path)
    if not result.is_valid:
        raise ValueError(f"Invalid manifest: {result.errors}")
    return result.manifest
```

### 3. **CI/CD Pipelines**
Automatically validate manifests before deployment:
```yaml
- name: Validate Agent Manifests
  run: jsonagents validate agents/*.json --strict
```

### 4. **Agent Registries**
Ensure only valid manifests are published:
```python
@app.post("/agents")
def publish_agent(manifest):
    result = validate_manifest(manifest)
    if not result.is_valid:
        return {"error": result.errors}, 400
    # Store manifest...
```

### 5. **Framework Converters**
Validate converted manifests:
```python
# Convert LangChain agent to PAM
pam_manifest = langchain_to_pam(agent)

# Validate conversion
result = validate_manifest(pam_manifest)
assert result.is_valid, "Conversion produced invalid manifest"
```

---

## 🚀 Real-World Use Cases

### Use Case 1: Pre-Deployment Validation
```bash
# In your CI/CD pipeline
jsonagents validate production/agents/*.json --strict
# Exit code 0 = all valid, 1 = failures
```

### Use Case 2: Development Feedback
```bash
# Get detailed feedback during development
jsonagents validate my-agent.json --verbose
# Shows full manifest, all warnings, suggestions
```

### Use Case 3: URI Verification
```bash
# Verify URI format before registering
jsonagents check-uri ajson://mycompany.com/agents/customer-support
# Shows parsed components and HTTPS transformation
```

### Use Case 4: Policy Testing
```bash
# Test policy expressions before deploying
jsonagents check-policy "tool.type == 'http' && message.content ~ 'search'"
# Validates syntax and shows tokenization
```

### Use Case 5: Programmatic Validation
```python
from jsonagents import Validator

validator = Validator()

# Validate multiple manifests
for manifest_path in manifest_files:
    result = validator.validate_file(manifest_path)
    
    if result.is_valid:
        deploy_agent(result.manifest)
    else:
        log_errors(manifest_path, result.errors)
        alert_team(result.errors)
```

---

## 📊 Benefits

| Benefit | Description |
|---------|-------------|
| **Catch Errors Early** | Find problems before deployment |
| **Ensure Interoperability** | Manifests work across frameworks |
| **Improve Quality** | Maintain consistent standards |
| **Enable CI/CD** | Automated validation in pipelines |
| **Provide Feedback** | Clear, actionable error messages |
| **Support Learning** | Helps developers understand spec |
| **Prevent Security Issues** | Validate policies before runtime |
| **Enable Confidence** | Deploy knowing manifests are correct |

---

## 🌐 The Bigger Picture

The JSON Agents specification enables **framework interoperability**:

```
┌─────────────┐    Convert to PAM     ┌──────────────┐
│  LangChain  │ ──────────────────▶   │              │
│    Agent    │                       │              │
└─────────────┘                       │   Portable   │
                                      │    Agent     │
┌─────────────┐    Convert to PAM     │   Manifest   │
│   OpenAI    │ ──────────────────▶   │    (PAM)     │
│ Assistant   │                       │              │
└─────────────┘                       │   ✅ VALID   │
                                      │              │
┌─────────────┐    Convert to PAM     │              │
│   AutoGen   │ ──────────────────▶   │              │
│    Agent    │                       └──────────────┘
└─────────────┘                              │
                                             │
                       ┌─────────────────────┴──────────────────────┐
                       ▼                     ▼                      ▼
                ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
                │  LangChain  │      │    AutoGen  │      │     MCP     │
                │  Runtime    │      │   Runtime   │      │   Runtime   │
                └─────────────┘      └─────────────┘      └─────────────┘
```

**The validator ensures manifests work everywhere**, enabling:
- 🔄 Convert agents between frameworks
- 📦 Share agents in public registries
- 🏢 Use multiple frameworks in same organization
- 🌍 Build framework-agnostic tools
- 📱 Deploy agents across platforms

---

## 🎓 Learn More

- **Specification**: [json-agents.md](../Standard/json-agents.md)
- **Examples**: [examples/](../Standard/examples/)
- **Validator Docs**: [README.md](README.md)
- **API Reference**: [jsonagents/](jsonagents/)

---

## 💭 Summary

**The JSON Agents Validator is a quality assurance tool that ensures agent manifests are correct, complete, and interoperable.**

It's like:
- 🔍 A spell-checker for agent configurations
- ✅ A test suite for manifest correctness  
- 🛡️ A safety net before production deployment
- 📏 A measuring stick for specification compliance

Without it, you're deploying agent configurations without knowing if they'll work. **With it, you deploy with confidence.**

---

*For detailed usage instructions, see [INSTALL.md](INSTALL.md) and [README.md](README.md)*
