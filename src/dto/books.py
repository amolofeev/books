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
    title = None
    filename = factory.Sequence(lambda x: str(x))
    cover = factory.Sequence(lambda x: str(x))
    file = factory.Sequence(lambda x: str(x))
