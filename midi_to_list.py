from mido import MidiFile
from main import MELODY_MAX, MELODY_MIN
from random import randint
import math
LENGTH = 64

# if confineQ, the note out of [MELODY_MAX, MELODY_MIN] will be mute
def MidiToList(midi : MidiFile, confineQ : bool = False) -> list:
    notes = []
    ticks_per_beat = midi.ticks_per_beat
    for track in midi.tracks:
        for msg in track:  # Assuming the main track is the first track
            if msg.type != 'note_on':
                continue
            note = msg.note
            if confineQ and (note > MELODY_MAX or note < MELODY_MIN):
                note = 0
            if msg.velocity < 10:
                note = 0
            period = math.ceil(msg.time / ticks_per_beat)
            for _ in range(period):
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