
import xml.etree.ElementTree as ET
import argparse

SCORE_TEMPLATE = '''
<score-partwise>
  <part-list>
    <score-part id="P1">
      <part-name>Music</part-name>
    </score-part>
    </part-list>
  <part id="P1">
  </part>
</score-partwise>
'''

MEASURE_TEMPLATE = '''
<measure>
  <attributes>
    <divisions>24</divisions>
    <key>
      <fifths>0</fifths>
      </key>
    <time>
      <beats>4</beats>
      <beat-type>4</beat-type>
      </time>
    <clef>
      <sign>G</sign>
      <line>2</line>
      </clef>
    </attributes>
</measure>
'''

NOTE_TEMPLATE = '''
<note>
    <duration></duration>
  </note>
'''

PITCH_TEMPLATE = '''
    <pitch>
      <step></step>
      <octave></octave>
      <alter></alter>
    </pitch>
'''

def un_map(dic):
    return {v: k for k, v in dic.items()}

class Untranslator(object):
    un_step_map = un_map({
        'C' : 0,
        'D' : 2,
        'E' : 4,
        'F' : 5,
        'G' : 7,
        'A' : 9,
        'B' : 11
    })
    un_type_to_time_map = un_map({
        '16th' : 1,
        'eighth' : 2,
        'quarter' : 4,
        'half' : 8,
        'whole' : 16
    })

    def text_to_chords(self, text_path):
        with open(text_path,'r') as f:
            music = f.read()
        return music.split(' ')

    def chord_to_notes(self, chord):
        return chord.split(chr(253))

    def is_rest(self, note):
        return 79 - ord(note[0]) == -175

    def note_pitch(self, note):
        pitch = 79 - ord(note[0])
        octave = pitch//12 + 4
        tone = pitch % 12
        step_count = max([step for step in Untranslator.un_step_map if step <= tone])
        alter = tone - step_count
        step = Untranslator.un_step_map[step_count]
        return octave, step, alter

    def note_duration(self, note):
        return ord(note[1]) - 127

    def note_to_xml(self, note):
        note_xml = ET.fromstring(NOTE_TEMPLATE)
        if self.is_rest(note):
            ET.SubElement(note_xml, 'rest')
        else:
            pitch = ET.fromstring(PITCH_TEMPLATE)
            pitch.find('octave').text, pitch.find('step').text, pitch.find('alter').text = map(str, self.note_pitch(note))
            note_xml.append(pitch)

        note_xml.find('duration').text = str(self.note_duration(note))
        return note_xml
        
    # returns a list, since the root is the measure
    def chord_to_xml(self, chord):
        notes = list(map(self.note_to_xml, self.chord_to_notes(chord)))
        for note in notes[1:]:
            ET.SubElement(note, 'chord')
        return notes

    def text_to_xml(self, text_path):
        measure = ET.fromstring(MEASURE_TEMPLATE)
        chords = list(map(self.chord_to_xml, self.text_to_chords(text_path)))
        for chord in chords:
            for note in chord:
                measure.append(note)
        return measure
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script translates music xml to plaintext')
    # Add arguments
    parser.add_argument('-i', '--input', type=str, help='Path to text file', required=True)
    parser.add_argument('-o', '--output', type=str, help='Path to output file', required=True)

    args = parser.parse_args()

    score = ET.fromstring(SCORE_TEMPLATE)
    score.find('part').append(Untranslator().text_to_xml(args.input))
    ET.ElementTree(score).write(args.output)
