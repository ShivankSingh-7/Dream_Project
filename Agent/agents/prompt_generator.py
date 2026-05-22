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


def sceneGeneratorNode(state: StoryState):

    scenes = state["scenes"]
    genre = state["genre"]

    max_clips = state["max_clips"]

    clip_duration = max(
        1,
        state["total_duration"] // max_clips
    )

    video_prompts = []

    for scene in scenes:

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a cinematic video prompt generation assistant.

                    Rules:

                    - Convert scene into a visual video prompt
                    - Preserve original scene exactly
                    - Do not add new events
                    - Keep environment consistent
                    - Keep anime style
                    - Include:
                        * environment
                        * camera angle
                        * lighting
                        * atmosphere
                    - Keep concise
                    - Return JSON only

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
                    """
                )
            ]
        )

        chain = prompt | llm | parser

        response = chain.invoke(
            {
                "genre": genre,
                "scene_story": scene["scene_story"],
                "environment": scene["environment"]
            }
        )

        video_prompts.append(
            {
                "scene_no": scene["scene_no"],
                "prompt": response["prompt"],
                "duration": clip_duration
            }
        )

    return {
        "video_prompts": video_prompts
    }