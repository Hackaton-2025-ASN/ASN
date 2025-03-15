import re
from typing import Dict, Optional


def extract_placeholders(template: str, string_to_match: str) -> Optional[Dict[str, str]]:
    escaped_template = re.escape(template)

    # Replace the placeholders with named capturing groups
    pattern = re.sub(r'\\{(\w+)\\}', r'(?P<\1>.+?)', escaped_template)
    pattern = f'^{pattern}$'

    match = re.match(pattern, string_to_match)

    return match.groupdict() if match else None
