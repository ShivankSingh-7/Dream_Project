from langgraph.graph import StateGraph, START, END

from agents.cleaner_agent import storyCleanerNode
from agents.story_rephrase_agent import rephraseNode
from agents.character_extractor import characterExtractorNode
from Schemas.state import StoryState


    
graph = StateGraph(StoryState)

graph.add_node('cleaner', storyCleanerNode)
graph.add_node('rephraser', rephraseNode)
graph.add_node('character_extractor', characterExtractorNode)

graph.add_edge(START, "cleaner")
graph.add_edge('cleaner', 'rephraser')
graph.add_edge('rephraser','character_extractor')
graph.add_edge('character_extractor',END)

app = graph.compile()

result = app.invoke(
    {
        "story": "A boy met a girl in class 6th class the boys uniform color was white shirt and mustard pant and girls uniform colour was white sirt and mustard tuning, the girl dont know that boy had already fell in love after 4 years the boy proposed the girl in class 10th she took one day but then said yes and now they are living happily",
        "genre": "Roomance"
    }
)

print(result)