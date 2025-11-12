"""Core validator for JSON Agents manifests."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

import jsonschema
from jsonschema import Draft202012Validator, RefResolver

from .uri import URIValidator
from .policy import PolicyValidator


@dataclass
class ValidationResult:
    """Result of manifest validation."""

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    manifest: Optional[Dict[str, Any]] = None

    def __str__(self) -> str:
        """String representation of validation result."""
        if self.is_valid:
            return "✅ Validation passed"
        
        lines = ["❌ Validation failed:"]
        for error in self.errors:
            lines.append(f"  • {error}")
        if self.warnings:
            lines.append("\n⚠️  Warnings:")
            for warning in self.warnings:
                lines.append(f"  • {warning}")
        return "\n".join(lines)


class Validator:
    """Main validator for JSON Agents manifests."""

    def __init__(self, schema_path: Optional[str] = None) -> None:
        """
        Initialize validator.

        Args:
            schema_path: Path to json-agents.json schema file.
                        If None, uses bundled schema.
        """
        self.schema_path = schema_path
        self.uri_validator = URIValidator()
        self.policy_validator = PolicyValidator()
        self._schema: Optional[Dict[str, Any]] = None
        self._validator: Optional[Draft202012Validator] = None

    def _load_schema(self) -> Dict[str, Any]:
        """Load JSON Agents schema."""
        if self._schema is not None:
            return self._schema

        if self.schema_path:
            schema_file = Path(self.schema_path)
        else:
            # Use bundled schema (from Standard repo)
            schema_file = Path(__file__).parent / "schemas" / "json-agents.json"

        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")

        with open(schema_file, "r", encoding="utf-8") as f:
            self._schema = json.load(f)

        return self._schema

    def _get_validator(self) -> Draft202012Validator:
        """Get JSON Schema validator instance."""
        if self._validator is not None:
            return self._validator

        schema = self._load_schema()
        
        # Set up resolver for schema references
        schema_dir = Path(self.schema_path).parent if self.schema_path else \
                     Path(__file__).parent / "schemas"
        resolver = RefResolver(
            base_uri=f"file://{schema_dir}/",
            referrer=schema
        )
        
        self._validator = Draft202012Validator(schema, resolver=resolver)
        return self._validator

    def validate(
        self,
        manifest: Union[str, Path, Dict[str, Any]],
        strict: bool = False
    ) -> ValidationResult:
        """
        Validate a JSON Agents manifest.

        Args:
            manifest: Path to manifest file or manifest dict
            strict: If True, treat warnings as errors

        Returns:
            ValidationResult with validation status and messages
        """
        errors: List[str] = []
        warnings: List[str] = []
        manifest_dict: Optional[Dict[str, Any]] = None

        # Load manifest
        try:
            if isinstance(manifest, (str, Path)):
                with open(manifest, "r", encoding="utf-8") as f:
                    manifest_dict = json.load(f)
            else:
                manifest_dict = manifest
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {e}")
            return ValidationResult(is_valid=False, errors=errors)
        except FileNotFoundError as e:
            errors.append(f"File not found: {e}")
            return ValidationResult(is_valid=False, errors=errors)

        # JSON Schema validation
        try:
            validator = self._get_validator()
            schema_errors = sorted(validator.iter_errors(manifest_dict), key=lambda e: e.path)
            
            for error in schema_errors:
                path = ".".join(str(p) for p in error.path) if error.path else "root"
                errors.append(f"Schema error at '{path}': {error.message}")
        
        except Exception as e:
            errors.append(f"Schema validation error: {e}")

        # Validate URIs
        if manifest_dict and "agent" in manifest_dict:
            agent_id = manifest_dict["agent"].get("id")
            if agent_id:
                uri_result = self.uri_validator.validate(agent_id)
                if not uri_result.is_valid:
                    errors.extend(uri_result.errors)
                warnings.extend(uri_result.warnings)

        # Validate tool URIs
        if manifest_dict and "tools" in manifest_dict:
            for i, tool in enumerate(manifest_dict["tools"]):
                tool_id = tool.get("id")
                if tool_id and tool_id.startswith("ajson://"):
                    uri_result = self.uri_validator.validate(tool_id)
                    if not uri_result.is_valid:
                        errors.extend([f"Tool[{i}] {e}" for e in uri_result.errors])

        # Validate graph node refs
        if manifest_dict and "graph" in manifest_dict:
            graph = manifest_dict["graph"]
            if "nodes" in graph:
                for i, node in enumerate(graph["nodes"]):
                    ref = node.get("ref")
                    if ref and ref.startswith("ajson://"):
                        uri_result = self.uri_validator.validate(ref)
                        if not uri_result.is_valid:
                            errors.extend([f"Graph node[{i}] {e}" for e in uri_result.errors])

        # Validate policy expressions
        if manifest_dict and "policies" in manifest_dict:
            for i, policy in enumerate(manifest_dict["policies"]):
                where = policy.get("where")
                if where:
                    policy_result = self.policy_validator.validate(where)
                    if not policy_result.is_valid:
                        errors.extend([f"Policy[{i}] {e}" for e in policy_result.errors])
                    warnings.extend([f"Policy[{i}] {w}" for w in policy_result.warnings])

        # Validate graph edge conditions
        if manifest_dict and "graph" in manifest_dict:
            graph = manifest_dict["graph"]
            if "edges" in graph:
                for i, edge in enumerate(graph["edges"]):
                    condition = edge.get("condition")
                    if condition:
                        policy_result = self.policy_validator.validate(condition)
                        if not policy_result.is_valid:
                            errors.extend([f"Edge[{i}] condition {e}" for e in policy_result.errors])

        # Check for warnings
        if manifest_dict:
            # Warn if no capabilities declared
            if not manifest_dict.get("capabilities"):
                warnings.append("No capabilities declared")
            
            # Warn if using deprecated fields (future-proofing)
            # (none currently deprecated in v1.0)

        # Final result
        if strict and warnings:
            errors.extend(warnings)
            warnings = []

        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            manifest=manifest_dict
        )


def validate_manifest(
    manifest: Union[str, Path, Dict[str, Any]],
    strict: bool = False,
    schema_path: Optional[str] = None
) -> ValidationResult:
    """
    Convenience function to validate a manifest.

    Args:
        manifest: Path to manifest file or manifest dict
        strict: If True, treat warnings as errors
        schema_path: Optional custom schema path

    Returns:
        ValidationResult
    """
    validator = Validator(schema_path=schema_path)
    return validator.validate(manifest, strict=strict)
