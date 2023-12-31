from mido import MidiFile, MidiTrack, Message, MetaMessage
from pygame import mixer
from itertools import groupby

import time
def ConvertToMidi(filename : str, pitches : list, BPM : int = 240) :

    # Create a new MIDI file and a track
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Add a note on and note off message for each pitch
    track.append(MetaMessage('set_tempo', 60000000 / BPM))
    factor : float = 120 / float(BPM)
    
    pitches = [(k, len(list(g))) for k, g in groupby(pitches)]
    
    for pair in pitches:
        vel = 96
        if pair[0] == 0:
            vel = 0
        track.append(Message('note_on', note=pair[0], velocity = vel, time= int(480 * factor * pair[1])))
    # Save the MIDI file
    mid.save(filename)
    
def PlayMidi(filename : str, sleepQ : bool = True):
    midi = MidiFile(filename)
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    if sleepQ : time.sleep(midi.length)
    
if __name__ == '__main__':
    pitches = range(100)
    filename = "song.midi"
    ConvertToMidi(filename, pitches)
    PlayMidi(filename)
