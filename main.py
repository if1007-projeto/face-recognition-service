import argparse
import face_recognition
from kafka import KafkaConsumer
from recognize import Recognize
from tempfile import NamedTemporaryFile
import time

max_attempts = 1000

def get_command_line_arguments():
    parser = argparse.ArgumentParser(
        description='Recognize faces from images.')
    
    parser.add_argument('-k', '--known-faces-path', dest='known_faces_path', metavar='<path>', required=True, type=str,
                        help='path to known faces. Example: ./known/faces')

    parser.add_argument('-i', '--unknown-face-input', dest='unknown_face', metavar='<path>', required=False, type=str,
                        help='path to unknown face image. Example: ./unknown/faces/face1.png')

    parser.add_argument('-b', '--unknown-faces-batch', dest='unknown_faces_batch', metavar='<path>', required=False, type=str,
                        help='path to unknown faces batch. Example: ./unknown/faces')

    parser.add_argument('-s', '--faces-source', dest='faces_source', metavar='<origin>', required=True, type=str,
                        help='kafka url to read faces. Example: localhost:9092')

    parser.add_argument('-t', '--kafka-topic', dest='kafka_topic', metavar='<kafka topic>', required=True, type=str,
                        help='kafka topic to subscribe and read frames')

    args = parser.parse_args()

    return args

def process_face(face):
    with NamedTemporaryFile(suffix='.jpg') as face_file:
        face_file.write(face)
        face_file.seek(0)
        recognize.recognize_face(face_file.name)

def try_connect_kafka():
    print('Trying to connect to Kafka - url: %s, topic %s' % (args.faces_source, args.kafka_topic))
    for attempt in range(max_attempts):
        print('Attempt to connect to Kafka - %d tries' % attempt)
        try:
            consumer = KafkaConsumer(args.kafka_topic, bootstrap_servers=[args.faces_source])
            for msg in consumer:
                process_face(msg.value)
        except:
            print('Error connecting')
        
        time.sleep(1)

if __name__ == '__main__':
    args = get_command_line_arguments()

    recognize = Recognize(args.known_faces_path)

    if args.unknown_faces_batch:
        recognize.recognize_face_batch(args.unknown_faces_batch)
    elif args.unknown_face:
        recognize.recognize_face(args.unknown_face)

    try_connect_kafka()