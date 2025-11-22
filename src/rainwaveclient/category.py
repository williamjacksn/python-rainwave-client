import typing

if typing.TYPE_CHECKING:
    from . import RainwaveChannel


class RainwaveCategory:
    def __init__(self, channel: "RainwaveChannel", category_id: int, name: str) -> None:
        self._channel = channel
        self.category_id = category_id
        self.name = name

    def __repr__(self) -> str:
        return f"<RainwaveCategory [{self}]>"

    def __str__(self) -> str:
        return self.name
