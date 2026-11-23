"""A shared, serializable evidence format used by every scanner and AI stage."""
from dataclasses import asdict, dataclass
from typing import Optional

@dataclass
class Finding:
    target: str
    scanner: str
    category: str
    description: str
    evidence: str
    severity: str = "informational"
    source_type: str = "live"
    advisory: Optional[str] = None

    def to_dict(self):
        return asdict(self)
