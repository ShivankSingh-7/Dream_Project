from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from Schemas.state import StoryState

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

parser = JsonOutputParser()

    

    
def characterExtractorNode(state: StoryState):
    
    story = state['clean_story']
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                    """
                    You are a character extraction assistant.

                    Rules:
                    - Extract all important characters
                    - Generate missing visual attributes
                    - Keep anime consistency
                    - Return only valid JSON
                    - If names are not provided, use generic names like Boy, Girl
                    - Do not invent names unnecessarily
                    - If age is not explicitly mentioned or cannot be confidently inferred, set age to null
                    - Do not leave hair empty
                    - Do not leave eyes empty
                    - Do not leave clothes empty
                    - Generate consistent appearance details for missing visual attributes
                    - Keep generated appearance realistic and suitable for anime characters

                    Return JSON in this exact format:

                    {{
                        "characters":[
                            {{
                                "id":"",
                                "name":"",
                                "gender":"",
                                "age": null,
                                "hair":"",
                                "eyes":"",
                                "clothes":"",
                                "style":"Anime"
                            }}
                        ]
                    }}
                    """
            ),

            (
                "human",
                """
                Story:
                {story}
                """
            )
        ]
        )
    
    chain = prompt | llm | parser
    
    
    response = chain.invoke({
        "story": story
    })
    
    
    return {
        "characters": response["characters"]
    }