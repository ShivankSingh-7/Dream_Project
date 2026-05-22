from langgraph.graph import StateGraph, START, END

from agents.cleaner_agent import storyCleanerNode
from agents.character_extractor_agent import characterExtractorNode
from agents.scene_splitter_agent import storySplitterNode
from agents.prompt_generator import sceneGenrtorNode
from agents.image_generator_agent import characterImageNode
from agents.video_generator_agent import videoGeneratorNode
from Schemas.state import StoryState


    
graph = StateGraph(StoryState)

graph.add_node('cleaner', storyCleanerNode)
graph.add_node('character_extractor', characterExtractorNode)
graph.add_node('scene_splitter', storySplitterNode)
graph.add_node('prompt_generator', sceneGenrtorNode)
graph.add_node('character_image_generator', characterImageNode)
graph.add_node('video_generator', videoGeneratorNode)


graph.add_edge(START, "cleaner")
graph.add_edge('cleaner','character_extractor')
graph.add_edge('character_extractor','character_image_generator')
graph.add_edge('character_image_generator', 'scene_splitter')
graph.add_edge('scene_splitter', 'prompt_generator')
graph.add_edge('prompt_generator', 'video_generator')
graph.add_edge('video_generator', END)


app = graph.compile()

result = app.invoke(
    {
        "story": "A boy met a girl in class 6th class the boys uniform color was white shirt and mustard pant and girls uniform colour was white sirt and mustard tuning, the girl dont know that boy had already fell in love after 4 years the boy proposed the girl in class 10th she took one day but then said yes and now they are living happily",
        "genre": "Roomance",
        "total_duration":60
    }
)

print(result)