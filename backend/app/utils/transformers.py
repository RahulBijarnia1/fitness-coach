"""
Data transformation utilities for FitCoach AI.

Provides helper functions for data conversion, formatting,
and transformation across the application.
"""

from typing import Any, Dict, List, Optional, TypeVar, Union
from datetime import date, datetime, timedelta
from decimal import Decimal


T = TypeVar("T")


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to float.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value or default
    """
    try:
        if value is None:
            return default
        if isinstance(value, Decimal):
            return float(value)
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to integer.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Integer value or default
    """
    try:
        if value is None:
            return default
        return int(value)
    except (ValueError, TypeError):
        return default


def format_weight(kg: float, unit: str = "kg") -> str:
    """
    Format weight with unit.
    
    Args:
        kg: Weight in kilograms
        unit: Target unit ('kg' or 'lb')
        
    Returns:
        Formatted weight string
    """
    if unit == "lb":
        lb = kg * 2.20462
        return f"{lb:.1f} lb"
    return f"{kg:.1f} kg"


def kg_to_lb(kg: float) -> float:
    """Convert kilograms to pounds."""
    return round(kg * 2.20462, 2)


def lb_to_kg(lb: float) -> float:
    """Convert pounds to kilograms."""
    return round(lb / 2.20462, 2)


def cm_to_inches(cm: float) -> float:
    """Convert centimeters to inches."""
    return round(cm / 2.54, 2)


def inches_to_cm(inches: float) -> float:
    """Convert inches to centimeters."""
    return round(inches * 2.54, 2)


def format_date(d: Union[date, datetime], format: str = "%Y-%m-%d") -> str:
    """
    Format date to string.
    
    Args:
        d: Date or datetime object
        format: Output format
        
    Returns:
        Formatted date string
    """
    if d is None:
        return ""
    return d.strftime(format)


def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string.
    
    Args:
        dt: Datetime object
        format: Output format
        
    Returns:
        Formatted datetime string
    """
    if dt is None:
        return ""
    return dt.strftime(format)


def parse_date(date_str: str, format: str = "%Y-%m-%d") -> Optional[date]:
    """
    Parse date string to date object.
    
    Args:
        date_str: Date string
        format: Input format
        
    Returns:
        Date object or None
    """
    try:
        return datetime.strptime(date_str, format).date()
    except (ValueError, TypeError):
        return None


def get_date_range(days: int) -> tuple[date, date]:
    """
    Get date range from today going back N days.
    
    Args:
        days: Number of days to go back
        
    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def get_week_start(d: date) -> date:
    """
    Get the start of the week (Monday) for a given date.
    
    Args:
        d: Any date
        
    Returns:
        Monday of that week
    """
    return d - timedelta(days=d.weekday())


def calculate_percentage_change(old: float, new: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        old: Original value
        new: New value
        
    Returns:
        Percentage change (positive for increase, negative for decrease)
    """
    if old == 0:
        return 0.0
    return round(((new - old) / old) * 100, 2)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def round_to_nearest(value: float, nearest: float = 0.5) -> float:
    """
    Round to nearest specified value.
    
    Args:
        value: Value to round
        nearest: Round to this increment
        
    Returns:
        Rounded value
    """
    return round(value / nearest) * nearest


def dict_to_object(data: dict, cls: type[T]) -> T:
    """
    Convert dictionary to object using constructor.
    
    Args:
        data: Dictionary with object data
        cls: Target class
        
    Returns:
        Instance of cls
    """
    return cls(**data)


def object_to_dict(obj: Any, exclude: List[str] = None) -> dict:
    """
    Convert object to dictionary.
    
    Args:
        obj: Object with __dict__
        exclude: Fields to exclude
        
    Returns:
        Dictionary representation
    """
    exclude = exclude or []
    
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() 
                if not k.startswith("_") and k not in exclude}
    
    return {}


def flatten_dict(
    d: Dict[str, Any],
    parent_key: str = "",
    sep: str = "_",
) -> Dict[str, Any]:
    """
    Flatten nested dictionary.
    
    Args:
        d: Nested dictionary
        parent_key: Parent key prefix
        sep: Key separator
        
    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def group_by(items: List[T], key: str) -> Dict[Any, List[T]]:
    """
    Group list items by a key.
    
    Args:
        items: List of objects
        key: Attribute name to group by
        
    Returns:
        Dictionary with groups
    """
    groups = {}
    for item in items:
        group_key = getattr(item, key, None) if hasattr(item, key) else item.get(key)
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(item)
    return groups


def chunk_list(lst: List[T], size: int) -> List[List[T]]:
    """
    Split list into chunks of specified size.
    
    Args:
        lst: List to split
        size: Chunk size
        
    Returns:
        List of chunks
    """
    return [lst[i:i + size] for i in range(0, len(lst), size)]
