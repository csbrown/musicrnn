from translate import Translator
import argparse
import os

def counter():
    i = 0
    while True:
        i += 1
        yield i

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script translates all the music xmls")
    parser.add_argument('--base_path', type=str, help="the base path", required=True)
    parser.add_argument('--fuckit', action='store_true')
    parser.add_argument('--min', type=int, help="the minimum value", required=True)
    parser.add_argument('--max', type=int, help="the maximum value", required=True)
    args = parser.parse_args()
    count = counter()
    for i in range(args.min, args.max + 1):
        the_input = os.path.join(args.base_path, "xml-clean", str(i) + ".xml")
        the_output = os.path.join(args.base_path, "translated-music", str(i) + ".txt")
        if args.fuckit:
            try:
                trans = Translator(the_input)
                f = open(the_output, "w")
                f.write(trans.translate())
                f.close()
            except:
                print('fuckit! ' + str(next(count)))
                pass
        else:
            trans = Translator(the_input)
            f = open(the_output, "w")
            f.write(trans.translate())
            f.close()



