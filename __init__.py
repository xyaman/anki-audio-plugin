# import the main window object (mw) from aqt
from aqt import mw, gui_hooks 

# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect

# import all of the Qt GUI library
from aqt.qt import *

import subprocess, os

def testFunction(reviewer, menu) -> None:

    current_note = reviewer.card.note()
    sentenceaudio_field = "SentenceAudio"


    # Example: [sound:A_Konosuba_S01_E04_1_0.01.02.169-0.01.05.630.mp3]
    print(current_note[sentenceaudio_field])

    action = QAction("test", mw)
    qconnect(action.triggered, lambda: print("here"))
    menu.addAction(action)

def didShowCard(card):
    current_note = card.note()
    sentenceaudio_field = "SentenceAudio"
    field_value = current_note[sentenceaudio_field]

    if not field_value:
        return
    
    is_ogg = field_value[-4:-1] == "ogg"
    if is_ogg:
        showInfo("Audio file is .ogg, it will be changed to .mp3")
        
        old_path = field_value[7:-1]
        new_path = old_path.replace(".ogg", ".mp3")

        col_dir = mw.col.media.dir() 
        command = f"ffmpeg -i {os.path.join(col_dir, old_path)} -acodec libmp3lame {os.path.join(col_dir, new_path)}".split(" ")
        subprocess.run(command)
        
        current_note[sentenceaudio_field] = f"[sound:{new_path}]"
        mw.col.update_note(current_note)



action = QAction("test", mw)
qconnect(action.triggered, testFunction)
mw.form.menuTools.addAction(action)

gui_hooks.reviewer_will_show_context_menu.append(testFunction)
gui_hooks.reviewer_did_show_question.append(didShowCard)
