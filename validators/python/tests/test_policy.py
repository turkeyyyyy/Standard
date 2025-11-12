"""Tests for policy expression validator."""

import pytest
from jsonagents.policy import PolicyValidator


def test_policy_validator_init():
    """Test policy validator initialization."""
    validator = PolicyValidator()
    assert validator is not None


def test_valid_simple_comparison():
    """Test simple comparison expression."""
    validator = PolicyValidator()
    result = validator.validate("tool.type == 'http'")
    
    assert result.is_valid
    assert len(result.errors) == 0


def test_valid_complex_expression():
    """Test complex logical expression."""
    validator = PolicyValidator()
    result = validator.validate(
        "tool.type == 'http' && tool.auth.method != 'none'"
    )
    
    assert result.is_valid


def test_valid_regex_match():
    """Test regex pattern matching."""
    validator = PolicyValidator()
    result = validator.validate("tool.endpoint ~ '^https://.*\\.internal'")
    
    assert result.is_valid


def test_valid_in_operator():
    """Test 'in' operator."""
    validator = PolicyValidator()
    result = validator.validate("tool.type in ['http', 'function']")
    
    assert result.is_valid


def test_valid_not_operator():
    """Test 'not' operator."""
    validator = PolicyValidator()
    result = validator.validate("not (tool.type == 'system')")
    
    assert result.is_valid


def test_valid_string_operators():
    """Test string operators."""
    validator = PolicyValidator()
    
    expressions = [
        "message.payload contains 'urgent'",
        "agent.id starts_with 'ajson://internal'",
        "tool.endpoint ends_with '.internal.corp'",
    ]
    
    for expr in expressions:
        result = validator.validate(expr)
        assert result.is_valid, f"Failed: {expr}"


def test_invalid_triple_equals():
    """Test invalid === operator."""
    validator = PolicyValidator()
    result = validator.validate("tool.type === 'http'")
    
    assert not result.is_valid
    assert any("===" in error for error in result.errors)


def test_invalid_single_equals():
    """Test invalid = operator."""
    validator = PolicyValidator()
    result = validator.validate("tool.type = 'http'")
    
    assert not result.is_valid
    assert any("=" in error or "==" in error for error in result.errors)


def test_invalid_single_ampersand():
    """Test invalid & operator."""
    validator = PolicyValidator()
    result = validator.validate("tool.type == 'http' & tool.auth == 'none'")
    
    assert not result.is_valid
    assert any("&" in error for error in result.errors)


def test_invalid_exclamation():
    """Test invalid ! operator."""
    validator = PolicyValidator()
    result = validator.validate("!tool.type == 'http'")
    
    assert not result.is_valid
    assert any("!" in error or "not" in error.lower() for error in result.errors)


def test_empty_expression():
    """Test empty expression."""
    validator = PolicyValidator()
    result = validator.validate("")
    
    assert not result.is_valid
    assert any("empty" in error.lower() for error in result.errors)


def test_unbalanced_parentheses():
    """Test unbalanced parentheses."""
    validator = PolicyValidator()
    result = validator.validate("(tool.type == 'http'")
    
    assert not result.is_valid
    assert any("paren" in error.lower() for error in result.errors)


def test_operator_at_start():
    """Test operator at start of expression."""
    validator = PolicyValidator()
    result = validator.validate("== 'http'")
    
    assert not result.is_valid
    assert any("operand" in error.lower() for error in result.errors)


def test_operator_at_end():
    """Test operator at end of expression."""
    validator = PolicyValidator()
    result = validator.validate("tool.type ==")
    
    assert not result.is_valid
    assert any("operand" in error.lower() for error in result.errors)


def test_unknown_context_warning():
    """Test warning for unknown context variable."""
    validator = PolicyValidator()
    result = validator.validate("unknown.field == 'value'")
    
    # Should be syntactically valid but warn about unknown context
    assert result.is_valid
    assert any("unknown" in warning.lower() for warning in result.warnings)


def test_valid_context_variables():
    """Test known context variables don't warn."""
    validator = PolicyValidator()
    
    expressions = [
        "tool.type == 'http'",
        "message.intent == 'faq'",
        "agent.id starts_with 'ajson://'",
        "runtime.environment == 'production'",
    ]
    
    for expr in expressions:
        result = validator.validate(expr)
        assert result.is_valid
        # Should not warn about context variables
        assert not any("unknown" in warning.lower() for warning in result.warnings)


def test_complex_nested_expression():
    """Test complex nested expression."""
    validator = PolicyValidator()
    result = validator.validate(
        "(tool.type == 'http' && tool.auth.method != 'none') || "
        "(message.priority > 8 && message.urgent == true)"
    )
    
    assert result.is_valid


def test_not_in_operator():
    """Test 'not in' operator."""
    validator = PolicyValidator()
    result = validator.validate("tool.type not in ['system', 'plugin']")
    
    assert result.is_valid
