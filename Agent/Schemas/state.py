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
    image_path: str | None


class Scene(TypedDict):
    scene_no: int
    scene_story: str
    characters: list[str]
    environment: str


class VideoPrompt(TypedDict):
    scene_no: int
    prompt: str
    character_images: list[str]
    duration: int


class StoryState(TypedDict):
    story: str
    genre: str
    total_duration: int

    clean_story: str

    characters: list[Character]

    scenes: list[Scene]

    video_prompts: list[VideoPrompt]