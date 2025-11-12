"""Tests for core validator."""

import json
import pytest
from pathlib import Path
from jsonagents.validator import Validator, validate_manifest, ValidationResult


def test_validator_init():
    """Test validator initialization."""
    validator = Validator()
    assert validator is not None
    assert validator.uri_validator is not None
    assert validator.policy_validator is not None


def test_validate_minimal_manifest():
    """Test validation of minimal valid manifest."""
    manifest = {
        "manifest_version": "1.0",
        "profiles": ["core"],
        "agent": {
            "id": "ajson://example.com/agents/test",
            "name": "Test Agent",
            "version": "1.0.0"
        },
        "capabilities": [
            {
                "id": "echo",
                "description": "Echo service"
            }
        ],
        "modalities": {
            "input": ["text"],
            "output": ["text"]
        }
    }
    
    validator = Validator()
    result = validator.validate(manifest)
    
    assert result.is_valid
    assert len(result.errors) == 0


def test_validate_missing_version():
    """Test validation fails without manifest_version."""
    manifest = {
        "profiles": ["core"],
        "agent": {
            "id": "ajson://example.com/agents/test",
            "name": "Test Agent"
        }
    }
    
    validator = Validator()
    result = validator.validate(manifest)
    
    assert not result.is_valid
    assert any("manifest_version" in error.lower() for error in result.errors)


def test_validate_invalid_uri():
    """Test validation catches invalid ajson:// URI."""
    manifest = {
        "manifest_version": "1.0",
        "profiles": ["core"],
        "agent": {
            "id": "ajson:invalid-uri",
            "name": "Test Agent"
        }
    }
    
    validator = Validator()
    result = validator.validate(manifest)
    
    assert not result.is_valid
    assert any("uri" in error.lower() for error in result.errors)


def test_validate_invalid_policy():
    """Test validation catches invalid policy expression."""
    manifest = {
        "manifest_version": "1.0",
        "profiles": ["core", "gov"],
        "agent": {
            "id": "ajson://example.com/agents/test",
            "name": "Test Agent"
        },
        "capabilities": [
            {
                "id": "echo",
                "description": "Echo service"
            }
        ],
        "modalities": {
            "input": ["text"],
            "output": ["text"]
        },
        "policies": [
            {
                "id": "test-policy",
                "effect": "deny",
                "action": "tool.call",
                "where": "tool.type === 'http'"  # Invalid operator
            }
        ]
    }
    
    validator = Validator()
    result = validator.validate(manifest)
    
    assert not result.is_valid
    assert any("===" in error for error in result.errors)


def test_validate_with_capabilities():
    """Test validation with capabilities."""
    manifest = {
        "manifest_version": "1.0",
        "profiles": ["core"],
        "agent": {
            "id": "ajson://example.com/agents/test",
            "name": "Test Agent",
            "version": "1.0.0"
        },
        "capabilities": [
            {
                "id": "summarization",
                "description": "Summarize text"
            }
        ],
        "modalities": {
            "input": ["text"],
            "output": ["text"]
        }
    }
    
    validator = Validator()
    result = validator.validate(manifest)
    
    assert result.is_valid
    assert len(result.warnings) == 0  # Should have capabilities now


def test_validate_warns_no_capabilities():
    """Test validation warns when no capabilities declared."""
    manifest = {
        "manifest_version": "1.0",
        "profiles": ["core"],
        "agent": {
            "id": "ajson://example.com/agents/test",
            "name": "Test Agent",
            "version": "1.0.0"
        },
        "modalities": {
            "input": ["text"],
            "output": ["text"]
        }
    }
    
    validator = Validator()
    result = validator.validate(manifest)
    
    assert result.is_valid
    assert any("capabilities" in warning.lower() for warning in result.warnings)


def test_validate_strict_mode():
    """Test strict mode treats warnings as errors."""
    manifest = {
        "manifest_version": "1.0",
        "profiles": ["core"],
        "agent": {
            "id": "ajson://example.com/agents/test",
            "name": "Test Agent",
            "version": "1.0.0"
        },
        "modalities": {
            "input": ["text"],
            "output": ["text"]
        }
    }
    
    validator = Validator()
    result = validator.validate(manifest, strict=True)
    
    assert not result.is_valid
    assert any("capabilities" in error.lower() for error in result.errors)


def test_validate_manifest_function():
    """Test convenience function."""
    manifest = {
        "manifest_version": "1.0",
        "profiles": ["core"],
        "agent": {
            "id": "ajson://example.com/agents/test",
            "name": "Test Agent",
            "version": "1.0.0"
        },
        "capabilities": [
            {
                "id": "echo",
                "description": "Echo service"
            }
        ],
        "modalities": {
            "input": ["text"],
            "output": ["text"]
        }
    }
    
    result = validate_manifest(manifest)
    assert result.is_valid


def test_validate_invalid_json_string():
    """Test validation of malformed JSON string."""
    validator = Validator()
    
    # Create temp file with invalid JSON
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{invalid json")
        temp_path = f.name
    
    try:
        result = validator.validate(temp_path)
        assert not result.is_valid
        assert any("json" in error.lower() for error in result.errors)
    finally:
        Path(temp_path).unlink()


def test_validation_result_str():
    """Test ValidationResult string representation."""
    result = ValidationResult(
        is_valid=False,
        errors=["Error 1", "Error 2"],
        warnings=["Warning 1"]
    )
    
    result_str = str(result)
    assert "❌" in result_str
    assert "Error 1" in result_str
    assert "Warning 1" in result_str
