import typing


Position = typing.NamedTuple(
    "Position",
    [
        ("latitude", float),
        ("longitude", float),
        ("altitude", float),
        ("transponder", int)
    ]
)
