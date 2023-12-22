from mido import MidiFile
from main import MELODY_MAX, MELODY_MIN
from random import randint
LENGTH = 64

def MidiToList(midi : MidiFile) -> list:
    notes = []
    for track in midi.tracks:
        for msg in track:  # Assuming the main track is the first track
            if msg.type != 'note_on' or msg.velocity <= 0:
                continue
            note = msg.note
            notes.append(note)
    return notes

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
    midi =  MidiFile("tmp/sample.mid")
    notes = MidiToList(midi)
    notes = ListSelect(notes)
    print(notes)