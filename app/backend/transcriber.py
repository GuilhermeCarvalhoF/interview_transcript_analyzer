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

def transcriptor(file_path):
    result = model.transcribe(file_path)
    return result["text"]
