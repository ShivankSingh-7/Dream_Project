from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict

llm = ChatGroq(
    model ="llama-3.3-70b-versatile"
)

class StoryState(TypedDict):
    
    story: str
    clean_story: str
    

def storyCleanerNode(state: StoryState):
    
    story = state['story']
    
    prompt = ChatPromptTemplate.from_template(
        """
        You are a story cleaning assistant.
        
        Rules:
        - Correct grammar mistakes
        - Improve sentence structure
        - Preserve Original meaninig 
        - Do not change story flow
        - Return only cleaned story text
        
        Story:
        {story}
        """
    )
    
    chain = prompt | llm
    
    response = chain.invoke({
        "story": story
    })
    
    return{
        "clean_story": response.content
    }
    
Input_data = {
    "story": "There is a boy who fell in lov ewith a cute girl in class 6th. he proposed her in class 10th now they are living happily in a relationship."
}

result = storyCleanerNode(Input_data)

print(result["clean_story"])
    
    