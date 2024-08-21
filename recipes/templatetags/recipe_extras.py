from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def duration_in_minutes(duration: timedelta) -> str:
    total_seconds = int(duration.total_seconds())
    minutes = total_seconds // 60
    return f"{minutes} minutes"
