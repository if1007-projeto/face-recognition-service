import face_recognition
import glob
import numpy as np
import traceback

class Recognize:

    def __init__(self, known_faces_path):
        self.__known_faces_list = glob.glob(known_faces_path + "/*.*")
        self.__faces_encoding = []
        self.__add_known_faces_batch()

    def __add_known_faces_batch(self):
        for known_face in self.__known_faces_list:
            self.add_known_face(known_face)

    def __get_face_encoding(self, face_path):
        try:
            known_face_image = face_recognition.load_image_file(face_path)
            known_face_enconding = face_recognition.face_encodings(known_face_image)
            if (len(known_face_enconding) != 1):
                print('Invalid number of faces in this image: %s' % face_path)
                return None
            else:
                return known_face_enconding
        except:
            print('%s is not a valid image file!' % face_path)
            return None

    def add_known_face(self, known_face_path):
        face_enconding = self.__get_face_encoding(known_face_path)
        if face_enconding != None:
            self.__faces_encoding.append(face_enconding[0])

    def recognize_face(self, face_path):
        unknown_face_enconding = self.__get_face_encoding(face_path)
        if unknown_face_enconding == None:
            return
        
        results = face_recognition.compare_faces(self.__faces_encoding, unknown_face_enconding[0])
        results_size = len(results)
        for i in range(results_size):
            if results[i] == True:
                print('Face match: %s <-> %s' % (face_path, self.__known_faces_list[i]))
                break

    def recognize_face_batch(self, face_batch_path):
        unknown_faces_list = glob.glob(face_batch_path + "/*.*")
        for unknown_face in unknown_faces_list:
            self.recognize_face(unknown_face)