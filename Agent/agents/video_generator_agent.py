from dotenv import load_dotenv
load_dotenv()

import os
from huggingface_hub import InferenceClient
from Schemas.state import StoryState


client = InferenceClient(
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)


def videoGeneratorNode(state: StoryState):

    prompts = state["video_prompts"]

    generated_videos = []

    os.makedirs(
        "generated_videos",
        exist_ok=True
    )

    for scene in prompts:

        try:

            # Build prompt
            video_prompt = f"""
            masterpiece, best quality,
            anime style,

            {scene["prompt"]}

            cinematic lighting,
            smooth motion,
            high detail,
            consistent character appearance,
            """

            # Use first character image as reference
            reference_image = None

            if scene["character_images"]:
                reference_image = scene["character_images"][0]


            with open(reference_image, "rb") as img:

                video = client.image_to_video(
                    image=img,
                    prompt=video_prompt,

                    model="Wan-AI/Wan2.1-I2V-14B",

                    num_frames=81,
                    guidance_scale=7.5
                )


            video_name = (
                f"scene_{scene['scene_no']}.mp4"
            )

            video_path = (
                f"generated_videos/{video_name}"
            )


            with open(
                video_path,
                "wb"
            ) as f:

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

                    "video_path":
                    None
                }
            )


    return {

        "videos":
        generated_videos
    }