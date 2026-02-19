"""
Enumeration Definitions

This module defines all enumeration types used in the complaint management system.

Enums:
    - Priority: Complaint priority levels
    - Status: Complaint status types
"""

from enum import Enum


class Priority(str, Enum):
    """
    Complaint priority levels.
    
    Values:
        LOW: Low priority complaint
        MEDIUM: Medium priority complaint (default)
        HIGH: High priority complaint
        CRITICAL: Critical priority requiring immediate attention
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Status(str, Enum):
    """
    Complaint status types.
    
    Values:
        OPEN: Newly registered complaint (default)
        IN_PROGRESS: Complaint being worked on
        RESOLVED: Complaint has been resolved
        CLOSED: Complaint is closed
    """
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
