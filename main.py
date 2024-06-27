import json
import logging
import uuid
from abc import ABC
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Iterable, List, Union

import backoff
import requests


@dataclass(frozen=True)
class Character:
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    origin: dict
    location: dict
    image: str
    episode: list[str]
    url: str
    created: str


@dataclass(frozen=True)
class Location:
    id: int
    name: str
    type: str
    dimension: str
    residents: List[str]
    url: str
    created: str


@dataclass(frozen=True)
class Episode:
    id: int
    name: str
    air_date: str
    episode: str
    characters: str
    url: str
    created: str


class APILoader(ABC):
    """Iterate over pages."""

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
    def get(self, url):
        return requests.get(url).json()

    def __init__(self):
        self.request_url = Request(self.endpoint)

    def __iter__(self):
        while self.request_url:
            result = self.get(self.request_url)
            self.request_url = result["info"]["next"]
            yield from Page(**result, record_factory=self.record_factory)


class CharacterAPILoader(APILoader):
    endpoint = "character"
    record_factory = Character


class EpisodeAPILoader(APILoader):
    endpoint = "episode"
    record_factory = Episode


class LocationAPILoader(APILoader):
    endpoint = "location"
    record_factory = Location


class Page:
    "Represent page of API response"

    def __init__(self, info: dict, results: List[dict], record_factory: Callable):
        self.info = info
        self.results = [record_factory(**record_kwargs) for record_kwargs in results]

    def __iter__(self):
        return iter(self.results)


class Request:
    def __init__(self, endpoint: str, page: int = 0):
        self.page = page
        page_part = f"/?page={page}"
        self.url = f"https://rickandmortyapi.com/api/{endpoint}{page_part}"

    def __str__(self):
        return self.url


class JSONFileWriter(ABC):
    root = Path("")

    def path(self, record: Union[Episode, Character, Location]):
        directory = self.root / self.directory
        directory.mkdir(exist_ok=True)
        path = directory / (record.name + ".json")
        return path

    def metadata(self, record):
        return record.name

    def uuid(self):
        return str(uuid.uuid4())

    def __call__(self, record):
        dictionary = {
            "Id": self.uuid(),
            "Metadata": self.metadata(record),
            "RawData": asdict(record),
        }
        with open(self.path(record), "w+") as file:
            json.dump(dictionary, file)
        return record


class EpisodeWriter(JSONFileWriter):
    directory = "episode"


class LocationWriter(JSONFileWriter):
    directory = "location"


class CharacterWriter(JSONFileWriter):
    directory = "character"


def pipe(producer: Iterable, consumer: Callable):
    for element in producer:
        yield consumer(element)


if __name__ == "__main__":
    # Load episodes
    for episode in pipe(EpisodeAPILoader(), EpisodeWriter()):
        air_date = datetime.strptime(episode.air_date, "%B %d, %Y").date()
        name = episode.name
        if date(2017, 1, 1) <= air_date <= date(2021, 12, 31) and len(name) > 3:
            print(episode)

    # Load locations
    all(pipe(LocationAPILoader(), LocationWriter()))

    # Load characters
    for character in pipe(CharacterAPILoader(), CharacterWriter()):
        if all(int(episode[-1]) % 2 == 1 for episode in character.episode):
            print(character)
