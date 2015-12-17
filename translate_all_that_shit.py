from translate import Translator
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script translates all the music xmls")
    parser.add_argument('--base_path', type=str, help="the base path", required=True)
    parser.add_argument('--fuckit', action='store_true')
    args = parser.parse_args()
    for i in range(1, 2):
        the_input = os.path.join(args.base_path, "xml-clean", str(i) + ".xml")
        the_output = os.path.join(args.base_path, "translated-music", str(i) + ".txt")
        if args.fuckit:
            try:
                trans = Translator(the_input)
                f = open(the_output, "w")
                f.write(trans.translate())
                f.close()
            except:
                pass
        else:
            trans = Translator(the_input)
            f = open(the_output, "w")
            f.write(trans.translate())
            f.close()



