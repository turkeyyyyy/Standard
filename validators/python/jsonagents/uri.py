"""URI validator for ajson:// scheme."""

import re
from dataclasses import dataclass, field
from typing import List
from urllib.parse import urlparse


@dataclass
class URIValidationResult:
    """Result of URI validation."""

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    uri: str = ""
    parsed: dict = field(default_factory=dict)


class URIValidator:
    """Validator for ajson:// URIs per RFC 3986."""

    # RFC 3986 compliant patterns
    SCHEME_PATTERN = re.compile(r"^ajson://")
    
    # Domain pattern (without port/userinfo for basic validation)
    DOMAIN_PATTERN = re.compile(
        r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$|^localhost$"
    )
    
    PATH_PATTERN = re.compile(r"^(/[a-zA-Z0-9._~!$&'()*+,;=:@\-]*)*$")
    FRAGMENT_PATTERN = re.compile(r"^[a-zA-Z0-9._~!$&'()*+,;=:@/?-]*$")

    def validate(self, uri: str) -> URIValidationResult:
        """
        Validate an ajson:// URI.

        Args:
            uri: The URI to validate

        Returns:
            URIValidationResult with validation status
        """
        errors: List[str] = []
        warnings: List[str] = []
        parsed_data: dict = {}

        if not uri:
            errors.append("URI cannot be empty")
            return URIValidationResult(is_valid=False, errors=errors, uri=uri)

        # Check scheme
        if not self.SCHEME_PATTERN.match(uri):
            errors.append(
                f"Invalid URI scheme. Expected 'ajson://', got: {uri.split('://')[0] if '://' in uri else 'none'}"
            )
            return URIValidationResult(is_valid=False, errors=errors, uri=uri)

        # Parse URI
        try:
            parsed = urlparse(uri)
            parsed_data = {
                "scheme": parsed.scheme,
                "authority": parsed.netloc,
                "path": parsed.path,
                "query": parsed.query,
                "fragment": parsed.fragment,
            }
        except Exception as e:
            errors.append(f"Failed to parse URI: {e}")
            return URIValidationResult(is_valid=False, errors=errors, uri=uri, parsed=parsed_data)

        # Validate authority (netloc)
        authority = parsed.netloc
        if not authority:
            errors.append("URI must include an authority (domain/host) component")
        else:
            # Check for userinfo (not recommended)
            if "@" in authority:
                warnings.append("URI contains userinfo (@), which is not recommended for security")
                # Extract domain after userinfo
                domain_with_port = authority.split("@")[-1]
            else:
                domain_with_port = authority
            
            # Check for port
            if ":" in domain_with_port and domain_with_port != "localhost":
                domain, port_str = domain_with_port.rsplit(":", 1)
                try:
                    port = int(port_str)
                    if port < 1 or port > 65535:
                        errors.append(f"Invalid port number: {port}")
                except ValueError:
                    errors.append(f"Invalid port in authority: {port_str}")
                    domain = domain_with_port
            else:
                domain = domain_with_port
            
            # Validate domain format
            if not self.DOMAIN_PATTERN.match(domain):
                errors.append(f"Invalid authority (domain): '{domain}'. Must be a valid domain or 'localhost'")

        # Validate path
        path = parsed.path
        if not path:
            warnings.append("URI has no path component")
        elif not path.startswith("/"):
            errors.append(f"Path must start with '/': {path}")
        elif not self.PATH_PATTERN.match(path):
            errors.append(f"Invalid characters in path: {path}")

        # Validate query (optional)
        if parsed.query:
            warnings.append(f"Query parameters present: {parsed.query}")

        # Validate fragment (optional)
        if parsed.fragment:
            if not self.FRAGMENT_PATTERN.match(parsed.fragment):
                errors.append(f"Invalid characters in fragment: {parsed.fragment}")

        is_valid = len(errors) == 0

        return URIValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            uri=uri,
            parsed=parsed_data,
        )

    def to_https(self, uri: str) -> str:
        """
        Transform ajson:// URI to HTTPS well-known URI.

        Args:
            uri: ajson:// URI

        Returns:
            Corresponding HTTPS URL

        Example:
            ajson://example.com/agents/router
            -> https://example.com/.well-known/agents/router.agents.json
        """
        result = self.validate(uri)
        if not result.is_valid:
            raise ValueError(f"Invalid ajson:// URI: {', '.join(result.errors)}")

        parsed = result.parsed
        authority = parsed["authority"]
        path = parsed["path"].lstrip("/")
        
        # Add .agents.json extension if not present
        if not path.endswith(".agents.json"):
            path = f"{path}.agents.json"

        # Build HTTPS URL - path already includes everything we need
        https_url = f"https://{authority}/.well-known/{path}"
        
        if parsed["fragment"]:
            https_url += f"#{parsed['fragment']}"

        return https_url
