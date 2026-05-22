from langgraph.graph import StateGraph, START, END

from agents.cleaner_agent import storyCleanerNode
from agents.character_extractor_agent import characterExtractorNode
from agents.scene_splitter_agent import storySplitterNode
from agents.prompt_generator import sceneGeneratorNode
from agents.video_generator_agent import videoGeneratorNode
from Schemas.state import StoryState


    
graph = StateGraph(StoryState)

graph.add_node('cleaner', storyCleanerNode)
graph.add_node('character_extractor', characterExtractorNode)
graph.add_node('scene_splitter', storySplitterNode)
graph.add_node('prompt_generator', sceneGeneratorNode)
graph.add_node('video_generator', videoGeneratorNode)


graph.add_edge(START, "cleaner")
graph.add_edge('cleaner','character_extractor')
graph.add_edge('character_extractor', 'scene_splitter')
graph.add_edge('scene_splitter', 'prompt_generator')
# graph.add_edge('prompt_generator', END)
graph.add_edge('prompt_generator', 'video_generator')
graph.add_edge('video_generator', END)


app = graph.compile()

result = app.invoke(
    {
        "story": "A dog happyily jumping in the ground",
        "genre": "Romance",
        "total_duration":1,
        "max_clips":1
    }
)

print(result)