from dotenv import load_dotenv
load_dotenv()

import os
import uuid
from huggingface_hub import InferenceClient
from Schemas.state import StoryState


client = InferenceClient(
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)


def videoGeneratorNode(state: StoryState):

    prompts = state["video_prompts"]

    generated_videos=[]

    os.makedirs(
        "generated_videos",
        exist_ok=True
    )


    for scene in prompts:
        
        duration = scene['duration']

        try:

            final_prompt = f"""
            {scene["prompt"]}

            Generate exactly {duration} second video.
            Very short clip.
            Single action only.
            """

            video = client.text_to_video(

                final_prompt,

                model="Wan-AI/Wan2.2-T2V-A14B",

            )

            random_id = str(
                uuid.uuid4()
            )[:8]

            video_path = (
                f"generated_videos/"
                f"scene_{scene['scene_no']}_{random_id}.mp4"
            )

            with open(
                video_path,
                "wb"
            ) as f:

                # save directly
                if hasattr(video, "read"):
                    f.write(video.read())
                else:
                    f.write(video)


            generated_videos.append(
                {
                    "scene_no":
                    scene["scene_no"],
                    "video_path":
                    video_path
                }
            )

            print(
                f"✅ Generated: {video_path}"
            )


        except Exception as e:

            print(
                f"❌ Failed scene "
                f"{scene['scene_no']}: {e}"
            )

            generated_videos.append(
                {
                    "scene_no":
                    scene["scene_no"],
                    "video_path":None
                }
            )


    return{
        "videos":generated_videos
    }