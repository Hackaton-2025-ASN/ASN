

class User:
    def __init__(self, id: str, name: str):
        self.id: str = id
        self.name: str = name

    def __str__(self) -> str:
        return f"User(id={self.id}, name={self.name})"
