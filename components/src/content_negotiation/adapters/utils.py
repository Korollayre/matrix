def parse_priorities(data: str) -> str:
    _mapping: dict[float, str] = {}
    for row in data.split(', '):
        try:
            name, priority = row.split(';q=')
        except ValueError:
            name, priority = row, 1.0
        else:
            priority = float(priority)

        _mapping[priority] = name

    return _mapping[max(_mapping)]
