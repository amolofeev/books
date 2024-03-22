import msgspec


class TagDTO(msgspec.Struct):
    id: int
    name: str
