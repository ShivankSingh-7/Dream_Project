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
                - Generate missing character attributes
                - Keep anime consistency
                - Return only valid JSON
                - If names are not provided, use generic names like Boy, Girl
                - Do not invent names unnecessarily
                

                Return JSON in this exact format:

                {{
                    "characters":[
                        {{
                            "id":"",
                            "name":"",
                            "gender":"",
                            "age":0,
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