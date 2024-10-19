import mido
import re

def parse_text_to_midi(text_data, output_midi_file):
    # Initialize a new MIDI file and track
    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(track)
    
    # Use regular expressions to extract tempo, ticks per beat, and note events
    tempo_regex = r'Tempo: (\d+\.\d+) BPM'
    ppq_regex = r'Ticks per beat: (\d+)'
    note_on_regex = r'Note_on - Note: (.+?) \(MIDI (\d+)\), Velocity: (\d+), Time \(ticks\): (\d+)'
    note_off_regex = r'Note_off - Note: (.+?) \(MIDI (\d+)\), Velocity: (\d+), Time \(ticks\): (\d+)'
    
    current_time = 0
    
    # Extract tempo
    tempo_match = re.search(tempo_regex, text_data)
    if tempo_match:
        bpm = float(tempo_match.group(1))
        tempo = mido.bpm2tempo(bpm)  # Convert BPM to microseconds per quarter note
        track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    # Extract ticks per beat (PPQ)
    ppq_match = re.search(ppq_regex, text_data)
    if ppq_match:
        ticks_per_beat = int(ppq_match.group(1))
        midi.ticks_per_beat = ticks_per_beat
    else:
        midi.ticks_per_beat = 480  # Default value if PPQ is not found

    # Extract all note events
    for line in text_data.splitlines():
        # Handle Note On events
        note_on_match = re.search(note_on_regex, line)
        if note_on_match:
            midi_note = int(note_on_match.group(2))
            velocity = int(note_on_match.group(3))
            event_time = int(note_on_match.group(4))

            delta_time = event_time - current_time  # Calculate delta time in ticks
            current_time = event_time

            # Add the note_on event to the track
            track.append(mido.Message('note_on', note=midi_note, velocity=velocity, time=delta_time))
        
        # Handle Note Off events
        note_off_match = re.search(note_off_regex, line)
        if note_off_match:
            midi_note = int(note_off_match.group(2))
            velocity = int(note_off_match.group(3))  # This is usually 0 for note_off events
            event_time = int(note_off_match.group(4))

            delta_time = event_time - current_time  # Calculate delta time in ticks
            current_time = event_time

            # Add the note_off event to the track
            track.append(mido.Message('note_off', note=midi_note, velocity=velocity, time=delta_time))

    # Save the constructed MIDI file
    midi.save(output_midi_file)
    print(f"Saved MIDI file to {output_midi_file}")

# Example usage
text_data = """Tempo: 80.00 BPM
Ticks per beat: 15360
Note_on - Note: 0, Velocity: 0, Time (ticks): 0
Note_on - Note: A4 (MIDI 69), Velocity: 110, Time (ticks): 3840
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 7680
Note_on - Note: E5 (MIDI 76), Velocity: 110, Time (ticks): 11520
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 15360
Note_on - Note: C5 (MIDI 72), Velocity: 110, Time (ticks): 19200
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 23040
Note_on - Note: A4 (MIDI 69), Velocity: 110, Time (ticks): 26880
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 30720
Note_on - Note: F4 (MIDI 65), Velocity: 110, Time (ticks): 34560
Note_off - Note: F4 (MIDI 65), Velocity: 0, Time (ticks): 38400
Note_on - Note: D4 (MIDI 62), Velocity: 110, Time (ticks): 42240
Note_off - Note: D4 (MIDI 62), Velocity: 0, Time (ticks): 46080
Note_on - Note: C4 (MIDI 60), Velocity: 110, Time (ticks): 49920
Note_off - Note: C4 (MIDI 60), Velocity: 0, Time (ticks): 53760
Note_on - Note: A3 (MIDI 57), Velocity: 110, Time (ticks): 57600
Note_off - Note: A3 (MIDI 57), Velocity: 0, Time (ticks): 61440
Note_on - Note: C4 (MIDI 60), Velocity: 110, Time (ticks): 65280
Note_off - Note: C4 (MIDI 60), Velocity: 0, Time (ticks): 69120
Note_on - Note: 0, Velocity: 0, Time (ticks): 72960
Note_on - Note: A4 (MIDI 69), Velocity: 110, Time (ticks): 76800
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 80640
Note_on - Note: E5 (MIDI 76), Velocity: 110, Time (ticks): 84480
Note_off - Note: E5 (MIDI 76), Velocity: 0, Time (ticks): 88320
Note_on - Note: C5 (MIDI 72), Velocity: 110, Time (ticks): 92160
Note_off - Note: C5 (MIDI 72), Velocity: 0, Time (ticks): 96000
Note_on - Note: A4 (MIDI 69), Velocity: 110, Time (ticks): 99840
Note_off - Note: A4 (MIDI 69), Velocity: 0, Time (ticks): 103680
Note_on - Note: F4 (MIDI 65), Velocity: 110, Time (ticks): 107520
Note_off - Note: F4 (MIDI 65), Velocity: 0, Time (ticks): 111360
Note_on - Note: D4 (MIDI 62), Velocity: 110, Time (ticks): 115200
Note_off - Note: D4 (MIDI 62), Velocity: 0, Time (ticks): 119040
Note_on - Note: C4 (MIDI 60), Velocity: 110, Time (ticks): 122880
Note_off - Note: C4 (MIDI 60), Velocity: 0, Time (ticks): 126720
Note_on - Note: A3 (MIDI 57), Velocity: 110, Time (ticks): 130560
Note_off - Note: A3 (MIDI 57), Velocity: 0, Time (ticks): 134400
Note_on - Note: C4 (MIDI 60), Velocity: 110, Time (ticks): 138240
Note_off - Note: C4 (MIDI 60), Velocity: 0, Time (ticks): 142080
Note_on - Note: 0, Velocity: 0, Time (ticks): 145920
"""
# The full text data would be here

# Output MIDI file
output_midi_file = '/Users/syrusaslam1/code_projects/backend/midi_parse/unparsed_midi_output.mid'

# Parse the text data and save as MIDI
parse_text_to_midi(text_data, output_midi_file)