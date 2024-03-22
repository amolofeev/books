import msgspec


class BookDTO(msgspec.Struct):
    id: int
    title: str
    filename: str | None = None
    cover: str | None = None
    file: str | None = None
