def abstractmethod(_: callable):
    def wrapper(*_, **__):
        raise NotImplementedError

    return wrapper


class OsEntity:
    @abstractmethod
    def __init__(self, *_, **__):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        return self.__repr__()

    def __getattr__(self, item: str):
        if "_" + item in self.__dict__:
            return self.__dict__["_" + item]

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )


class Folder(OsEntity):
    def __init__(self, name: str, subtree: list, parent=None):
        self._name = name
        self._subtree = subtree
        self._parent = parent

    def __repr__(self) -> str:
        return f" - {self._name} (folder, size={self.size})"

    def append(self, entity: OsEntity):
        self._subtree.append(entity)

    def cd(self, name: str):
        for entity in self._subtree:
            if entity.name == name:
                return entity

        raise FileNotFoundError(f"Could not find {name}")

    @property
    def size(self):
        return sum([entity.size for entity in self._subtree])


class File(OsEntity):
    def __init__(self, name: str, size: str, parent: Folder = None):
        self._name = name
        self._size = size
        self._parent = parent

    def __repr__(self) -> str:
        return f" - {self._name} (file, size={self.size})"


class Command(OsEntity):
    def __init__(self, command: str, output: list[str]):
        args = command.split(" ")
        self._command = args[0]
        self._args = args[1:]
        self._output = output

    def __repr__(self) -> str:
        return f"{self._command}, {self._args} -> {self._output}"
