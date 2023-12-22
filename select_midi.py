import os
import midi_to_list
import player
import mido
import tempfile
import csv

if __name__ == '__main__':
    input_folder = input("Please enter the path to the input folder: ")


    print("When you give a score, the music stops")
    output_record = []
    output_score = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            path = os.path.join(root, file)
            midi = mido.MidiFile(path)
            part = midi_to_list.MidiToList(midi)
            part = midi_to_list.ListSelect(part)
            if part == None:
                continue
            tmpfilename = tempfile.mktemp()
            player.ConvertToMidi(tmpfilename, part, 240)
            player.PlayMidi(tmpfilename, False)
            print("This is {}", file)
            score : float = float(input("Score 0~1(other wise it will be discarded, -1 to quit):"))
            os.remove(tmpfilename)
            player.mixer.music.stop()
            if score == -1.0: break
            if score >= 0 and score < 1.0:
                output_record.append(part)
                output_score.append(score)
    
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Record', 'Score'])  # Write the header
        for record, score in zip(output_record, output_score):
            writer.writerow([record, score])  # Write the data
