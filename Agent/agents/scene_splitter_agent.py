from langchain_groq import ChatGroq
from Schemas.state import StoryState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

parser = JsonOutputParser()


def storySplitterNode(state: StoryState):

    story = state["clean_story"]
    characters = state["characters"]
    genre = state["genre"]
    max_clips = state["max_clips"]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a scene splitting assistant.

                Rules:

                - Split story into logical visual scenes
                - Maximum number of scenes = {max_clips}
                - If story has more events, merge related events
                - Preserve original story events exactly
                - Do not add new characters
                - Do not add new events
                - Do not remove important details
                - Keep timeline order exactly
                - Each scene should represent a visually separate moment
                - Attach characters appearing in scene
                - Add environment
                - Keep scene descriptions concise
                - Use genre only for atmosphere
                - Return only valid JSON

                Return:

                {{
                    "scenes":[
                        {{
                            "scene_no":1,
                            "scene_story":"",
                            "characters":[],
                            "environment":""
                        }}
                    ]
                }}
                """
            ),
            (
                "human",
                """
                Genre:
                {genre}

                Characters:
                {characters}

                Story:
                {story}
                """
            )
        ]
    )

    chain = prompt | llm | parser

    result = chain.invoke(
        {
            "genre": genre,
            "characters": characters,
            "story": story,
            "max_clips": max_clips
        }
    )

    return {
        "scenes": result["scenes"]
    }