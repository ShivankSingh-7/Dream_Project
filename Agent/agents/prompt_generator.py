from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from Schemas.state import StoryState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

parser = JsonOutputParser()

def sceneGenrtorNode(state: StoryState):
    scenes = state['scenes']
    characters = state['characters']
    genre = ['genre']
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a video prompt generation assistant.

                Rules:
                - Generate a detailed video prompt for each scene
                - Preserve scene events exactly
                - Do not add new characters
                - Do not add new story events
                - Use provided character information exactly
                - Maintain character appearance consistency across scenes
                - Use genre only for atmosphere and visual styling
                - Add environment details if missing
                - Add lighting information
                - Add camera perspective if suitable
                - Keep anime style consistent
                - Keep prompts concise to reduce token usage
                - Return only valid JSON

                Return JSON in this exact format:

                {{
                    "video_prompts":[
                        {{
                            "scene_no":1,
                            "video_prompt":""
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

                Scenes:
                {scenes}
                """
            )
        ]
    )
    
    chain = prompt | llm | parser
    
    result = chain.invoke(
        {
            'genre': genre,
            'characters': characters,
            'scenes': scenes
            
        }
    )
    
    return{
        "video_prompts" : result["video_prompts"]
    }
