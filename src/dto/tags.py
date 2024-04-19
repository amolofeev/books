import msgspec


class TagDTO(msgspec.Struct):
    id: int
    name: str
    parent_id: int | None


class TagWithActiveDTO(TagDTO):
    is_active: bool = False
