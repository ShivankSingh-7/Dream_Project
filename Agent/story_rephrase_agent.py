from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from typing import TypedDict
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(
    model = "llama-3.3-70b-versatile"
)

class StoryRephraseState(TypedDict):
    
    story: str
    genre: str
    rephrased_story: str
    
    
def rephraseNode(state: StoryRephraseState):
    
    story = state['story']
    genre = state['genre']
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a story rewriting assistant.

                Rules:
                - Rewrite according to selected genre
                - Preserve original story flow
                - Keep descriptions visually clear
                - Focus on actions and environments
                - Avoid poetic language
                - Avoid excessive emotions
                - Make story suitable for scene splitting and AI video generation
                - Return only rewritten story
                """
            ),

            (
                "human",
                """
                Genre: {genre}

                Story:
                {story}
                """
            )
        ]
    )
    
    chain = prompt | llm
    
    response = chain.invoke({
        "story": story,
        "genre": genre
    })
    
    return {
        "rephrased_story": response.content
    }
    
input_data = {
    "story": "There is a boy who fell in lov ewith a cute girl in class 6th. he proposed her in class 10th now they are living happily in a relationship.",
    "genre": "romantic"
}

result = rephraseNode(input_data)

print(result['rephrased_story'])