"""Tests for URI validator."""

import pytest
from jsonagents.uri import URIValidator


def test_uri_validator_init():
    """Test URI validator initialization."""
    validator = URIValidator()
    assert validator is not None


def test_valid_uri():
    """Test validation of valid ajson:// URI."""
    validator = URIValidator()
    result = validator.validate("ajson://example.com/agents/hello")
    
    assert result.is_valid
    assert len(result.errors) == 0
    assert result.parsed["scheme"] == "ajson"
    assert result.parsed["authority"] == "example.com"
    assert result.parsed["path"] == "/agents/hello"


def test_valid_uri_with_version():
    """Test URI with version in path."""
    validator = URIValidator()
    result = validator.validate("ajson://example.com/agents/hello/v1.0.0")
    
    assert result.is_valid
    assert result.parsed["path"] == "/agents/hello/v1.0.0"


def test_valid_uri_localhost():
    """Test URI with localhost."""
    validator = URIValidator()
    result = validator.validate("ajson://localhost/agents/test")
    
    assert result.is_valid
    assert result.parsed["authority"] == "localhost"


def test_valid_uri_with_fragment():
    """Test URI with fragment."""
    validator = URIValidator()
    result = validator.validate("ajson://example.com/agents/hello#metadata")
    
    assert result.is_valid
    assert result.parsed["fragment"] == "metadata"


def test_invalid_scheme():
    """Test URI with wrong scheme."""
    validator = URIValidator()
    result = validator.validate("https://example.com/agents/hello")
    
    assert not result.is_valid
    assert any("scheme" in error.lower() for error in result.errors)


def test_missing_authority():
    """Test URI without authority."""
    validator = URIValidator()
    result = validator.validate("ajson:///agents/hello")
    
    assert not result.is_valid
    assert any("authority" in error.lower() for error in result.errors)


def test_invalid_authority():
    """Test URI with invalid authority."""
    validator = URIValidator()
    result = validator.validate("ajson://invalid domain/agents/hello")
    
    assert not result.is_valid
    assert any("authority" in error.lower() for error in result.errors)


def test_missing_path():
    """Test URI without path."""
    validator = URIValidator()
    result = validator.validate("ajson://example.com")
    
    assert result.is_valid
    assert any("path" in warning.lower() for warning in result.warnings)


def test_path_no_leading_slash():
    """Test URI with path not starting with /."""
    validator = URIValidator()
    result = validator.validate("ajson://example.com/agents/hello")
    
    assert result.is_valid


def test_empty_uri():
    """Test empty URI."""
    validator = URIValidator()
    result = validator.validate("")
    
    assert not result.is_valid
    assert any("empty" in error.lower() for error in result.errors)


def test_uri_with_port():
    """Test URI with port."""
    validator = URIValidator()
    result = validator.validate("ajson://example.com:8080/agents/hello")
    
    assert result.is_valid


def test_uri_with_userinfo():
    """Test URI with userinfo (should warn)."""
    validator = URIValidator()
    result = validator.validate("ajson://user@example.com/agents/hello")
    
    # Should be valid but with warning
    assert result.is_valid
    assert any("userinfo" in warning.lower() for warning in result.warnings)


def test_to_https():
    """Test URI to HTTPS transformation."""
    validator = URIValidator()
    https_url = validator.to_https("ajson://example.com/agents/router")
    
    assert https_url == "https://example.com/.well-known/agents/router.agents.json"


def test_to_https_with_fragment():
    """Test URI to HTTPS transformation with fragment."""
    validator = URIValidator()
    https_url = validator.to_https("ajson://example.com/agents/router#metadata")
    
    assert https_url == "https://example.com/.well-known/agents/router.agents.json#metadata"


def test_to_https_already_has_extension():
    """Test URI to HTTPS when path already has extension."""
    validator = URIValidator()
    https_url = validator.to_https("ajson://example.com/agents/router.agents.json")
    
    assert https_url == "https://example.com/.well-known/agents/router.agents.json"


def test_to_https_invalid_uri():
    """Test to_https raises error for invalid URI."""
    validator = URIValidator()
    
    with pytest.raises(ValueError):
        validator.to_https("invalid-uri")
