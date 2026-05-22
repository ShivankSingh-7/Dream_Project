from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from Schemas.state import StoryState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

parser = JsonOutputParser()


def sceneGenrtorNode(state: StoryState):

    scenes = state["scenes"]
    characters = state["characters"]
    genre = state["genre"]

    # Create character -> image path mapping
    character_map = {
        c["name"]: c["image_path"]
        for c in characters
    }

    video_prompts = []

    for scene in scenes:

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a cinematic video prompt generation assistant.

                    Rules:
                    - Convert scene into visual video prompt
                    - Preserve scene exactly
                    - Do not add new events
                    - Do not add characters
                    - Keep environment consistent
                    - Keep anime style
                    - Focus on:
                        * character appearance
                        * environment
                        * camera angle
                        * lighting
                        * atmosphere
                    - Keep prompt concise
                    - Return valid JSON only

                    Return:

                    {{
                        "prompt":""
                    }}
                    """
                ),
                (
                    "human",
                    """
                    Genre:
                    {genre}

                    Scene:
                    {scene_story}

                    Environment:
                    {environment}

                    Characters:
                    {characters}
                    """
                )
            ]
        )

        chain = prompt | llm | parser

        response = chain.invoke(
            {
                "genre": genre,
                "scene_story": scene["scene_story"],
                "environment": scene["environment"],
                "characters": scene["characters"]
            }
        )

        image_paths = []

        for character_name in scene["characters"]:

            if character_name in character_map:

                image_paths.append(
                    character_map[character_name]
                )

        video_prompts.append(
            {
                "scene_no": scene["scene_no"],
                "prompt": response["prompt"],
                "character_images": image_paths,
                "duration": 5
            }
        )

    return {
        "video_prompts": video_prompts
    }