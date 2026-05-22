from langchain_groq import ChatGroq
from Schemas.state import StoryState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatGroq(
    model= "llama-3.3-70b-versatile"
)

parser = JsonOutputParser()


def storySplitterNode(state: StoryState):
    
    story = state['clean_story']
    characters = state["characters"]
    genre = state["genre"]
    
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a scene splitting assistant.

                Rules:
                - Split the story into logical visual scenes
                - Preserve original story events exactly
                - Do not add new characters
                - Do not add new events
                - Do not remove important details
                - Keep scene order exactly the same as story timeline
                - Each scene should represent a visually separate moment
                - Attach characters appearing in that scene
                - Keep scene descriptions concise and visual
                - Use genre only for visual atmosphere, not for changing events
                - Return only valid JSON

                Return JSON in this exact format:

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
            "genre":genre,
            "characters": characters,
            "story": story           
            
        }
    )
    
    return {
        "scenes": result["scenes"]
    }
