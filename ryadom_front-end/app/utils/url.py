#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urlencode, parse_qsl, urlparse
from datetime import datetime

def update_query_params(url: str, **kwargs) -> str:
    """
    Обновляет query-параметры в URL.
    Работает с любым URL, не требует объекта request.
    
    Пример:
        update_query_params("/?category=old", category="new") -> "/?category=new"
    """
    path = url.split('?')[0]
    current_params = dict(parse_qsl(url.split('?')[1])) if '?' in url else {}
    
    current_params.update(kwargs)
    current_params = {k: v for k, v in current_params.items() if v is not None}
    
    if "date" in current_params and isinstance(current_params["date"], datetime):
        current_params["date"] = current_params["date"].strftime("%Y-%m-%d")
    
    query_string = urlencode(current_params)
    return f"{path}?{query_string}" if query_string else path