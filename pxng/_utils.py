def resource(resource):
    from pathlib import Path
    font_path = Path(__file__).parent / 'resources' / resource
    return str(font_path)
