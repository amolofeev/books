import factory
import msgspec


class CreateBookDTO(msgspec.Struct, kw_only=True):
    title: str
    filename: str
    cover: str
    file: str


class BookDTO(CreateBookDTO):
    id: int


class CreateBookFactory(factory.Factory):
    class Meta:
        model = CreateBookDTO
    title = factory.Sequence(str)
    filename = factory.Sequence(str)
    cover = factory.Sequence(str)
    file = factory.Sequence(str)
