from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from typing import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

parser = JsonOutputParser()

class Character(TypedDict):
    id: str
    name: str
    gender: str
    age: int
    hair: str
    eyes: str
    clothes: str
    style: str
    
class CharacterState(TypedDict):
    genre: str
    rephrased_story: str
    Characters: list[Character]
    
def characterExtractorNode(state: CharacterState):
    
    story = state['rephrased_story']
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",
            """
            You are a character extraction assistant.
            
            Rules
            -Extract all important characters
            -Generate missing character attributes
            -keep anime consistency
            -Return only valid JSON
            
            Output: {
                "characters":[
                    {
                        "id":"",
                            "name":"",
                            "gender":"",
                            "age":"",
                            "hair":"",
                            "eyes":"",
                            "clothes":"",
                            "style":"Anime"
                    }
                ]
            }
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
    
    
    response = chain.invoke(prompt)
    
    return {
        "characters": response["characters"]
    }