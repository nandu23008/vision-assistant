import os
import time
import base64
import requests
from dotenv import load_dotenv


load_dotenv(override=True)


GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()


BUSY_MESSAGE = (
    "The AI service is currently busy or rate-limited. "
    "Please wait a few seconds and try again."
)


MODEL = "qwen/qwen3.6-27b"


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"




def remove_thinking(text):

    """
    Remove reasoning output if the model accidentally returns it.
    """

    if "<think>" in text and "</think>" in text:

        text = text.split("</think>")[-1]


    return text.strip()







def describe_image(image_path):


    if not GROQ_API_KEY:

        print("ERROR: Missing GROQ_API_KEY")

        return BUSY_MESSAGE






    prompt = """

You are VisionGuide AI, a real-time navigation assistant for a blind or visually impaired person.

Your response will be converted into speech, so keep it short, clear, and useful.

STRICT RULES:
- Do NOT reveal reasoning.
- Do NOT output internal thoughts.
- Do NOT use <think> tags.
- Only provide the final answer.

NAVIGATION RULES:
1. Describe only what is clearly visible.
2. Never guess hidden information.
3. Never describe where the camera is located.
4. Never mention how the image was captured.
5. Never say the user is holding, sitting, standing, or wearing something unless clearly visible.
6. Never invent obstacles or dangers.
7. Do not describe irrelevant body parts or camera artifacts unless they are important for safety.
8. Prioritize the environment over the person taking the image.
9. If something is unclear, say "unclear".
10. Do not estimate exact distances.
11. Never describe a person's appearance, identity, age, gender, or clothing.

Focus on:
- Room/environment type
- People present (count only, no description)
- Important objects
- Possible obstacles or navigation risks
- Safe next action

Return ONLY this format:

Scene:
One short sentence describing the environment.

People:
Approximate number of visible people, if any.
If none:
No people visible.

Objects:
Only important visible objects relevant to the user.

Safety:
Only clearly visible obstacles or navigation hazards.
Examples:
- A staircase is visible ahead and may require caution.
- A narrow pathway appears obstructed by furniture.
- A bed or large object is blocking part of the walking area.
Do not call something a hazard unless it visibly affects movement.
If none:
No visible hazards.

Suggested Action:
One short practical instruction based only on visible information.
If none needed:
Continue carefully.

No markdown.
No explanations.
No extra text.
"""







    try:

        with open(image_path, "rb") as image_file:

            encoded_image = base64.b64encode(
                image_file.read()
            ).decode("utf-8")


    except Exception as e:

        print("Image error:", e)

        return "Unable to read image."







    payload = {

        "model": MODEL,


        "messages": [

            {

                "role": "user",

                "content": [

                    {

                        "type": "text",

                        "text": prompt

                    },

                    {

                        "type": "image_url",

                        "image_url": {

                            "url":
                            f"data:image/jpeg;base64,{encoded_image}"

                        }

                    }

                ]

            }

        ],


        "reasoning_effort": "none"

    }







    headers = {

        "Authorization":
        f"Bearer {GROQ_API_KEY}",

        "Content-Type":
        "application/json"

    }







    MAX_ATTEMPTS = 3

    RETRY_DELAY_SECONDS = 5



    for attempt in range(1, MAX_ATTEMPTS + 1):


        print(
            f"Attempt {attempt}/{MAX_ATTEMPTS} | "
            f"Calling Groq with model '{MODEL}'..."
        )



        try:


            response = requests.post(

                GROQ_URL,

                headers=headers,

                json=payload,

                timeout=30

            )



            data = response.json()






            if response.status_code == 200 and "choices" in data:


                text = (
                    data["choices"][0]
                    ["message"]
                    ["content"]
                )


                text = remove_thinking(text)



                print("\n========== AI RESPONSE ==========")

                print(text)

                print("=================================\n")



                return text.strip()







            elif response.status_code == 429:


                print(
                    f"Rate limited. Retrying in {RETRY_DELAY_SECONDS}s..."
                )


                if attempt < MAX_ATTEMPTS:

                    time.sleep(RETRY_DELAY_SECONDS)






            else:


                print(
                    "Groq error:",
                    data
                )

                break







        except Exception as e:


            print(
                "Request failed:",
                e
            )






    return BUSY_MESSAGE