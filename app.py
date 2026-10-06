import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from ai_helper import describe_image


app = Flask(__name__)


UPLOAD_FOLDER = os.path.join("static", "uploads")

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8MB max upload

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS




def clean_ai_response(text):
    """
    Remove reasoning output and clean formatting.
    """

    # Remove Qwen thinking output if present
    if "<think>" in text and "</think>" in text:
        text = text.split("</think>")[-1]


    cleaned_lines = []


    for line in text.splitlines():

        line = line.strip()


        # Remove empty lines
        if line:
            cleaned_lines.append(line)



    return "\n".join(cleaned_lines).strip()







def split_description(text):

    sections = {
        "Scene": "",
        "Objects": "",
        "Safety": "",
        "Suggested Action": ""
    }

    keywords = [
        ("suggested action", "Suggested Action"),
        ("action", "Suggested Action"),
        ("scene", "Scene"),
        ("objects", "Objects"),
        ("safety", "Safety"),
    ]

    current = None

    for line in text.splitlines():
        line = line.strip().replace("**", "")
        if not line:
            continue

        lower = line.lower()
        matched = False

        for key, section in keywords:
            if lower.startswith(key):
                current = section
                content = line.split(":", 1)
                if len(content) > 1 and content[1].strip():
                    sections[current] += content[1].strip() + " "
                matched = True
                break

        if not matched and current:
            sections[current] += line + " "

    for key in sections:
        sections[key] = sections[key].strip()

    return sections








@app.route("/")
def home():

    return render_template(
        "index.html"
    )









@app.route("/describe", methods=["POST"])
def describe():


    if "image" not in request.files:

        return redirect(
            url_for("home")
        )



    image = request.files["image"]



    if image.filename == "" or not allowed_file(image.filename):
        return redirect(url_for("home"))

    ext = image.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(image_path)






    description = describe_image(
        image_path
    )



    print("\n========== RAW AI RESPONSE ==========")

    print(description)

    print("=====================================\n")





    description = clean_ai_response(
        description
    )



    print("\n========== CLEAN AI RESPONSE ==========")

    print(description)

    print("=======================================\n")






    try:
        sections = split_description(description)
    except Exception as e:
        print("PARSE ERROR:", e)
        sections = {
            "Scene": description,
            "Objects": "",
            "Safety": "",
            "Suggested Action": ""
        }



    print("SCENE:", sections["Scene"])

    print("OBJECTS:", sections["Objects"])

    print("SAFETY:", sections["Safety"])

    print("ACTION:", sections["Suggested Action"])








    return render_template(

        "result.html",

        filename=filename,

        image_path=image_path,

        description=description,

        scene=sections["Scene"],

        objects=sections["Objects"],

        safety=sections["Safety"],

        action=sections["Suggested Action"]

    )









if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=int(os.environ.get("PORT", 5000)),

        debug=False

    )
