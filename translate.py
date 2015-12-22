import xml.etree.ElementTree as ET
import argparse

class Translator(object):
    step_map = {
        'C' : 0,
        'D' : 2,
        'E' : 4,
        'F' : 5,
        'G' : 7,
        'A' : 9,
        'B' : 11
    }
    type_to_time_map = {
        '16th' : 1,
        'eighth' : 2,
        'quarter' : 4,
        'half' : 8,
        'whole' : 16
    }
    def __init__(self, input_path):
        self.timekeeper = 0
        self.tree = ET.parse(input_path)

        attributes = self.tree.find('.//measure').find('attributes')
        self.divisions = int(attributes.find('divisions').text) #per quarter note
        self.beats = int(attributes.find('time').find('beat-type').text)

    #return a dict of lists of dicts, one big dict for the whole piece, with a list for each chord of little dicts for each note. each note dict looks like:
    # {note: piano_key_int (0 = middle c), duration: note duration}
    # chord dict:
    # {time_stamp: [note_dicts]}  
    def xml_to_notes(self, etree):
        chord_dict = {}
        measures = etree.findall('.//measure')
        previous_dur = 0
        for measure in measures:
            for child in measure:
                if child.tag == "note":

                    if child.find('chord') is None:
                        self.timekeeper += previous_dur

                    if self.timekeeper not in chord_dict:
                        chord_dict[self.timekeeper] = [] 
                    try:
                        duration = int(child.find('duration').text)
                    except:
                        duration = Translator.type_to_time_map[child.find('type').text] * self.divisions / 4
                    previous_dur = duration
                    # possibly a note
                    pitch = child.find('pitch')
                    rest = child.find('rest')
                    if pitch is not None:
                        step = pitch.find('step').text
                        octave = int(pitch.find('octave').text)
                        alter = int(pitch.find('alter').text) if pitch.find('alter') is not None else 0
                        chord_dict[self.timekeeper].append({
                            'note': self.translate_note(step, octave, alter),
                            'duration': duration
                        })        
                    # possibly a rest
                    elif rest is not None:
                        chord_dict[self.timekeeper].append({
                            'note': self.translate_rest(),
                            'duration': duration
                        }) 

                if child.tag == "backup":
                    self.timekeeper    -= int(child.find('duration').text)    
        return chord_dict    
   
    def translate_rest(self):
        return 100

    def translate_note(self, step, alter, octave):
        return Translator.step_map[step] + 12*(octave - 4) + alter

    # the duration needs to be translated to parts of 48.  This allows us to represent whole notes and triplets of 16th notes.  Code these starting at ascii 33 up through 48... the note needs to be translated to a char from 128 to 254 somehow... code middle c as ascii 192... code a rest as chr(92)
    def note_to_text(self, note):
        divs_per_beat = self.divisions * 4
        to_48parts = 48 / divs_per_beat
        return chr(192 - note['note']) + chr(33 + to_48parts * note['duration'])

    def chords_to_text(self, chord_dict):
        chords = []
        for time in sorted(chord_dict):
            chords.append(''.join(map(self.note_to_text, chord_dict[time])))
        return ' '.join(chords)
 
    def translate(self):
        notes = self.xml_to_notes(self.tree)
        return self.chords_to_text(notes)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script translates music xml to plaintext')
    # Add arguments
    parser.add_argument('-i', '--input', type=str, help='Path to xml file', required=True)
    parser.add_argument('-o', '--output', type=str, help='Path to output file', required=True)

    args = parser.parse_args()

    trans = Translator(args.input)
    f = open(args.output, 'w')
    f.write(trans.translate())
    f.close()
