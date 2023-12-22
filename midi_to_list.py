from main import MELODY_MAX, MELODY_MIN
from random import randint
import music21
import math
LENGTH = 64

# if confineQ, the note out of [MELODY_MAX, MELODY_MIN] will be mute
def MidiToList(stream, confineQ : bool = False) -> list:
    notes = stream.parts[0].flatten().notes
    now = 0
    ret = []
    for note in notes:
        if not isinstance(note, music21.note.Note): continue
        interval = note.duration.quarterLength
        next = now + interval
        cnt : int = 0
        while now + cnt * 0.25 < next:
            ret.append(int(note.pitch.ps))
            cnt += 1
        now = next
    return ret
            

# May return None if lenght < LENGTH
def ListSelect(midi_list : list) -> list:
    if len(midi_list) < LENGTH:
        return None
    length = len(midi_list)
    max_pos : int = length - LENGTH
    start_pos = randint(0, max_pos)
    notes = midi_list[start_pos : start_pos + LENGTH]
    return notes

if __name__ == '__main__':
    midi =  music21.converter.parse("tmp/sample.mid")
    notes = MidiToList(midi)
    notes = ListSelect(notes)
    print(notes)