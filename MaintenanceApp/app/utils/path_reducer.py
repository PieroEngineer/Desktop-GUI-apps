import os

def abbreviate_path(path: str) -> str:
        # Normalize the path to use consistent separators
        path = os.path.normpath(path)
        parts = path.split(os.sep)

        if len(parts) < 3:
            return path  # Not enough parts to abbreviate

        return f"{parts[0]}/.../{parts[-2]}/{parts[-1]}"