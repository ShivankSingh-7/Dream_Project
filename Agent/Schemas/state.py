from typing import TypedDict

class Character(TypedDict):
    id: str
    name: str
    gender: str
    age: int
    hair: str
    eyes: str
    clothes: str
    style: str
    
class Scene(TypedDict):
    scene_no: int
    scene_story: str
    characters: list[str]
    
class VideoPrompt(TypedDict):
    scene_no: int
    video_prompt: str

class StoryState(TypedDict):
    story: str
    genre: str
    clean_story: str
    characters: list[Character]
    scenes: list[Scene]
    video_prompts: list[VideoPrompt]