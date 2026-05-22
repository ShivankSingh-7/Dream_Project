from typing import TypedDict


class Character(TypedDict):
    id: str
    name: str
    gender: str
    age: int | None
    hair: str
    eyes: str
    clothes: str
    style: str


class Scene(TypedDict):
    scene_no: int
    scene_story: str
    characters: list[str]
    environment: str


class VideoPrompt(TypedDict):
    scene_no: int
    prompt: str


class StoryState(TypedDict):
    story: str
    genre: str
    total_duration: int
    max_clips: int

    clean_story: str

    characters: list[Character]

    scenes: list[Scene]

    video_prompts: list[VideoPrompt]