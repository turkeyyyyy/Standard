#!/usr/bin/env python3
"""Simple test script for the validator."""

import sys
import json
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

from jsonagents import validate_manifest

def test_examples():
    """Test validator against Standard repo examples."""
    # From validators/python/ go up to repo root
    standard_path = Path(__file__).parent.parent.parent
    examples_dir = standard_path / "examples"
    
    if not examples_dir.exists():
        print(f"❌ Examples directory not found: {examples_dir}")
        return False
    
    examples = list(examples_dir.glob("*.json"))
    if not examples:
        print(f"❌ No example files found in {examples_dir}")
        return False
    
    print(f"🧪 Testing {len(examples)} example manifest(s)...\n")
    
    all_valid = True
    for example in examples:
        print(f"Testing: {example.name}")
        result = validate_manifest(str(example))
        
        if result.is_valid:
            print(f"  ✅ Valid\n")
        else:
            print(f"  ❌ Invalid")
            for error in result.errors:
                print(f"     • {error}")
            print()
            all_valid = False
    
    return all_valid


if __name__ == "__main__":
    success = test_examples()
    sys.exit(0 if success else 1)
