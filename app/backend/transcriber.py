###########
## imports
###########

import whisper
import tempfile
import os

############
## model
############
model = whisper.load_model("small")

###########
## functions
###########

def transcriptor(file):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(file.read())
        temp.flush()
        temp_path = temp.name
    result = model.transcribe(temp_path)
    os.remove(temp_path)
    return result["text"]
