"""Policy expression validator for where clauses."""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Set


@dataclass
class PolicyValidationResult:
    """Result of policy expression validation."""

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    expression: str = ""


class PolicyValidator:
    """Validator for policy where clause expressions (Appendix B)."""

    # Operators per specification
    COMPARISON_OPS = {"==", "!=", ">", "<", ">=", "<="}
    STRING_OPS = {"~", "!~", "contains", "starts_with", "ends_with"}
    COLLECTION_OPS = {"in", "not in"}
    LOGICAL_OPS = {"&&", "||", "and", "or"}
    UNARY_OPS = {"not"}

    ALL_OPERATORS = COMPARISON_OPS | STRING_OPS | COLLECTION_OPS | LOGICAL_OPS | UNARY_OPS

    # Context variables
    VALID_CONTEXTS = {"tool", "message", "agent", "runtime"}

    # Token patterns
    IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
    NUMBER_PATTERN = re.compile(r"^-?\d+(\.\d+)?$")
    STRING_PATTERN = re.compile(r"^'([^'\\]|\\.)*'$")

    def validate(self, expression: str) -> PolicyValidationResult:
        """
        Validate a policy where clause expression.

        Args:
            expression: The policy expression to validate

        Returns:
            PolicyValidationResult with validation status
        """
        errors: List[str] = []
        warnings: List[str] = []

        if not expression:
            errors.append("Expression cannot be empty")
            return PolicyValidationResult(is_valid=False, errors=errors, expression=expression)

        # Tokenize expression
        try:
            tokens = self._tokenize(expression)
        except Exception as e:
            errors.append(f"Tokenization error: {e}")
            return PolicyValidationResult(is_valid=False, errors=errors, expression=expression)

        # Check for common syntax errors
        syntax_errors = self._check_syntax(tokens, expression)
        errors.extend(syntax_errors)

        # Validate operators
        operator_errors = self._validate_operators(tokens, expression)
        errors.extend(operator_errors)

        # Validate context variables
        context_warnings = self._validate_context_vars(tokens)
        # Check if any returns from _validate_context_vars are actually errors
        for warning in context_warnings:
            if 'Invalid syntax' in warning:
                errors.append(warning)
            else:
                warnings.append(warning)

        # Check parentheses balance
        if not self._check_balanced_parens(expression):
            errors.append("Unbalanced parentheses")

        # Check for invalid operator combinations
        combo_errors = self._check_operator_combos(tokens)
        errors.extend(combo_errors)

        is_valid = len(errors) == 0

        return PolicyValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            expression=expression,
        )

    def _tokenize(self, expression: str) -> List[str]:
        """Simple tokenizer for policy expressions."""
        # Replace multi-char operators with placeholders to avoid splitting
        expr = expression
        expr = expr.replace("starts_with", "§STARTS_WITH§")
        expr = expr.replace("ends_with", "§ENDS_WITH§")
        expr = expr.replace("not in", "§NOT_IN§")
        expr = expr.replace("contains", "§CONTAINS§")
        
        # Handle quoted strings
        string_pattern = re.compile(r"'([^'\\]|\\.)*'")
        strings = string_pattern.findall(expr)
        for i, s in enumerate(strings):
            placeholder = f"§STRING{i}§"
            expr = expr.replace(f"'{s}'", placeholder)

        # Split on whitespace and operators
        tokens = []
        current = ""
        
        for char in expr:
            if char in " \t\n":
                if current:
                    tokens.append(current)
                    current = ""
            elif char in "()[]{}":
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(char)
            else:
                current += char
        
        if current:
            tokens.append(current)

        # Restore placeholders
        restored = []
        for token in tokens:
            token = token.replace("§STARTS_WITH§", "starts_with")
            token = token.replace("§ENDS_WITH§", "ends_with")
            token = token.replace("§NOT_IN§", "not in")
            token = token.replace("§CONTAINS§", "contains")
            for i, s in enumerate(strings):
                token = token.replace(f"§STRING{i}§", f"'{s}'")
            restored.append(token)

        return restored

    def _check_syntax(self, tokens: List[str], expression: str) -> List[str]:
        """Check for basic syntax errors."""
        errors = []

        # Check for empty expression after tokenization
        if not tokens:
            errors.append("Expression tokenized to empty")
            return errors

        # Check for consecutive operators (except 'not')
        prev_was_op = False
        for i, token in enumerate(tokens):
            is_op = self._is_operator(token)
            if is_op and prev_was_op and token != "not" and tokens[i - 1] != "not":
                errors.append(f"Consecutive operators: {tokens[i-1]} {token}")
            prev_was_op = is_op and token != "not"

        return errors

    def _validate_operators(self, tokens: List[str], expression: str) -> List[str]:
        """Validate operator usage."""
        errors = []

        for token in tokens:
            # Check for common typos
            if token == "===":
                errors.append("Invalid operator '==='. Use '==' for equality")
            elif token == "=":
                errors.append("Invalid operator '='. Use '==' for comparison")
            elif token in {"&", "|"}:
                errors.append(f"Invalid operator '{token}'. Use '&&' or '||' for logical operations")
            elif token == "!":
                errors.append("Invalid operator '!'. Use 'not' for negation")

        return errors

    def _validate_context_vars(self, tokens: List[str]) -> List[str]:
        """Validate context variable references."""
        warnings = []
        errors = []

        for token in tokens:
            # Check if token starts with ! (invalid negation) but is not a valid operator like != or !~
            if token.startswith("!") and len(token) > 1 and not token.startswith("!=") and not token.startswith("!~"):
                errors.append(f"Invalid syntax: '{token}'. Use 'not' keyword for negation, not '!' prefix")
            
            if "." in token and not token.startswith("'"):
                parts = token.split(".")
                if len(parts) >= 2:
                    context_root = parts[0]
                    if context_root not in self.VALID_CONTEXTS:
                        warnings.append(
                            f"Unknown context variable '{context_root}'. "
                            f"Valid contexts: {', '.join(sorted(self.VALID_CONTEXTS))}"
                        )

        # Return errors if any, otherwise warnings
        return errors if errors else warnings

    def _check_balanced_parens(self, expression: str) -> bool:
        """Check if parentheses are balanced."""
        stack = []
        pairs = {"(": ")", "[": "]", "{": "}"}
        
        for char in expression:
            if char in pairs:
                stack.append(char)
            elif char in pairs.values():
                if not stack:
                    return False
                opening = stack.pop()
                if pairs[opening] != char:
                    return False
        
        return len(stack) == 0

    def _check_operator_combos(self, tokens: List[str]) -> List[str]:
        """Check for invalid operator combinations."""
        errors = []

        # Look for binary operators without operands
        for i, token in enumerate(tokens):
            if token in self.COMPARISON_OPS | self.STRING_OPS | self.COLLECTION_OPS | self.LOGICAL_OPS:
                # Check if there's a preceding operand (skip if start or after opening paren)
                if i == 0:
                    errors.append(f"Operator '{token}' at start of expression needs left operand")
                elif tokens[i - 1] in {"(", "["}:
                    errors.append(f"Operator '{token}' after '{tokens[i-1]}' needs left operand")
                
                # Check if there's a following operand (skip if end or before closing paren)
                if i == len(tokens) - 1:
                    errors.append(f"Operator '{token}' at end of expression needs right operand")
                elif i < len(tokens) - 1 and tokens[i + 1] in {")", "]"}:
                    errors.append(f"Operator '{token}' before '{tokens[i+1]}' needs right operand")

        return errors

    def _is_operator(self, token: str) -> bool:
        """Check if token is an operator."""
        return token in self.ALL_OPERATORS

    def _is_literal(self, token: str) -> bool:
        """Check if token is a literal value."""
        if token in {"true", "false", "null"}:
            return True
        if self.NUMBER_PATTERN.match(token):
            return True
        if self.STRING_PATTERN.match(token):
            return True
        return False
