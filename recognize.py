import json
import sys

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer

from dejavu.GrpcServer import serve

with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)


def main():
    djv = Dejavu(config)

    if sys.argv[1] == "learn":
        djv.fingerprint_file(sys.argv[2])
    elif sys.argv[1] == "recognize":
        print(djv.recognize(FileRecognizer, sys.argv[2]))
    elif sys.argv[1] == "recognize_object":
        print(djv.recognize(MicrophoneRecognizer, seconds=sys.argv[2]))
    elif sys.argv[1] == "delete":
        filtered_songs = list(filter(lambda i: i["song_name"] in sys.argv[2], djv.get_fingerprinted_songs()))
        filtered_ids = [i["song_id"] for i in filtered_songs]
        print(djv.delete_songs_by_id(filtered_ids))
    elif sys.argv[1] == "serve":
        serve(djv)


if __name__ == "__main__":
    main()
