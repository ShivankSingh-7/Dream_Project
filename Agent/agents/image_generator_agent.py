from dotenv import load_dotenv
load_dotenv()

import os
from huggingface_hub import InferenceClient
from Schemas.state import StoryState

client = InferenceClient(
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)


def characterImageNode(state: StoryState):

    characters = state["characters"]
    updated_characters = []
    os.makedirs("generated_images", exist_ok=True)

    for character in characters:

       
        positive_prompt = (
            
            "masterpiece, best quality, ultra-detailed, highres, "
            "8k wallpaper, sharp focus, "

            
            "anime style, 2D anime illustration, "
            "studio ghibli lighting, vibrant colors, "

           
            "1 character, solo, full body, front view, "
            "standing, looking at viewer, neutral expression, "

            f"{character['gender'].lower()} character, "
            f"{character['hair']} hair, "
            f"{character['eyes']} eyes, "
            f"wearing {character['clothes']}, "

            "simple white background, white bg, "
            "centered composition"
        )
        negative_prompt = (
            "lowres, bad anatomy, bad hands, missing fingers, "
            "extra fingers, fused fingers, too many fingers, "
            "extra limbs, missing limbs, floating limbs, "
            "disconnected limbs, malformed limbs, "
            "ugly, duplicate, morbid, mutilated, "
            "out of frame, extra arms, extra legs, "
            "disfigured, deformed, cross-eyed, "
            "blurry, bad art, bad proportions, "
            "gross proportions, cloned face, "
            "multiple people, crowd, group, "
            "nsfw, watermark, signature, text"
        )

        
        full_prompt = f"{positive_prompt} | negative: {negative_prompt}"

        try:
            image = client.text_to_image(
                positive_prompt,
                model="Qwen/Qwen-Image-2512",
                negative_prompt=negative_prompt, 
                guidance_scale=7.5,                
                num_inference_steps=50,           
                width=768,
                height=1024,                       
            )

            image_name = character["name"].replace(" ", "_")
            image_path = f"generated_images/{image_name}.png"
            image.save(image_path)

            character["image_path"] = image_path
            print(f"✅ Generated: {image_path}")

        except Exception as e:
            print(f"❌ Failed for {character['name']}: {e}")
            character["image_path"] = None

        updated_characters.append(character)

    return {"characters": updated_characters}