from mido import MidiFile, MidiTrack, Message, MetaMessage
from pygame import mixer
import time
def ConvertToMidi(filename : str, pitches : list, BPM : int = 120) :

    # Create a new MIDI file and a track
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Add a note on and note off message for each pitch
    cnt : int = 0
    track.append(MetaMessage('set_tempo', 60000000 / BPM))
    for pitch in pitches:
        cnt += 1
        track.append(Message('note_on', note=pitch, velocity=96, time= 0))
        track.append(Message('note_off', note=pitch, velocity=96, time = 480))
    # Save the MIDI file
    mid.save(filename)
    
def PlayMidi(filename : str):
    midi = MidiFile(filename)
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    time.sleep(midi.length)
    
if __name__ == '__main__':
    pitches = [72, 77, 54, 66, 54, 59, 71, 59, 54, 68, 75, 70, 55, 71, 71, 76, 64, 64, 76, 69, 54, 79, 58, 63, 58, 65, 60, 78, 53, 66, 59, 54, 69, 55, 60, 60, 76, 54, 67, 72, 67, 62, 76, 57, 69, 76, 57, 62, 57, 79, 67, 55, 75, 60, 55, 72, 59, 77, 54, 77, 59, 71, 57, 62]
    filename = "song.midi"
    ConvertToMidi(filename, pitches)
    PlayMidi(filename)
