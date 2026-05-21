from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from Schemas.state import StoryState

llm = ChatGroq(
    model ="llama-3.3-70b-versatile"
)

    

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
    

