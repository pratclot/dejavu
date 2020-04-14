import logging
from concurrent import futures

import grpc

import AudioSamples_pb2
import AudioSamples_pb2_grpc

from dejavu.logic.recognizer.grpc_recognizer import GrpcRecognizer


class GrpcServer(AudioSamples_pb2_grpc.AudioSampleServicer):
    def __init__(self, dejavu):
        super().__init__()
        self.djv = dejavu
        self.data = []

    def searchSample(self, request_iterator, context):
        for i in request_iterator:
            print(i.audio_sample)
            self.data.append(i.audio_sample)
        # tune_name = self.djv.recognize(GrpcRecognizer, request_iterator)
        return AudioSamples_pb2.gTune(name="abc")

    def test(self, request, context):
        return AudioSamples_pb2.gTune(tuneName="dffdf")

    def play_remotely(self, request, context):
        GrpcRecognizer.play_audio(self.data)
        return ""

    def clean_remote(self, request, context):
        self.data = []
        return ""

    def recognize(self, request, context):
        result = self.djv.recognize(GrpcRecognizer, self.data)
        print(result)
        tune_name = result[0][0]["song_name"]
        self.data = []
        return AudioSamples_pb2.gTune(name=tune_name)


def serve(djv):
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_server = GrpcServer(djv)
    AudioSamples_pb2_grpc.add_AudioSampleServicer_to_server(grpc_server, server)

    with open("chief-CA.crt", "rb") as f:
        ca_cert = f.read()
    with open("msi.crt", "rb") as f:
        server_cert = f.read()
    with open("msi.pem", "rb") as f:
        server_key = f.read()

    creds = server_key, server_cert
    grpc_creds = grpc.ssl_server_credentials((creds,), root_certificates=ca_cert)
    server.add_secure_port('[::]:50051', grpc_creds)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
