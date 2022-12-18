from numpy import asarray, expand_dims
from mtcnn import MTCNN
from keras.models import load_model
from keras import models
from keras import layers
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
import numpy as np
import pandas as pd
import banco as bd
import os
from PIL import Image
import cv2

matrix=list()
listaFinal,listaL= list(),list()
validaFinal= list()
nomes, valNomes= list(), list()

model_path = 'facenet_keras.h5'
model = load_model(model_path)
detector = MTCNN()


def embaralhamento(trainX, trainY,cnpj):
    trainY=binariza(trainY)
    X, Y = shuffle(trainX, trainY, random_state=0)
    #embaralha
    trainX, valX, trainY, valY = train_test_split(X, Y, test_size=0.20, random_state=42)
    norm = Normalizer(norm="l2")
    trainX = norm.transform(trainX)
    valX = norm.transform(valX)
    trainY = np.unique(trainY)
    classes = len(np.unique(trainY))
    return criaRede(trainX,trainY,classes,valX,valY,cnpj)

def binariza(trainY):
    out_encoder = LabelEncoder()
    out_encoder.fit(trainY)
    Y = out_encoder.transform(trainY)
    #transforma os nomes em numeros
    Y = np.unique(Y)
    return Y

def criaRede(trainX, trainY,classes,valX,valY,cnpj):
    loop=True
    try:
        while loop==True :
            if deletaInteligen(cnpj) == True:
                loop=False
    except:
        return False

    caminhoFinal = os.path.join(os.getcwd(), "inteligen")
    cnpj=str(cnpj)+".h5"
    cnpj = os.path.join(caminhoFinal,cnpj)
    modelo = models.Sequential()
    modelo.add(layers.Dense(128, activation="relu", input_shape=(128,)))
    modelo.add(layers.Dense(classes, activation="softmax"))
    modelo.summary()
    modelo.compile(optimizer="adam",
                   loss="categorical_crossentropy",
                   metrics=['accuracy'])

    modelo.fit(trainX, trainY, epochs=40,validation_data = (valX,valY), batch_size=8)
    modelo.save(cnpj)
    bd.updatCriacao(cnpj)
    return True

def uniDados(cnpj):
    confirmador=bd.comparacao(cnpj)
    if confirmador == False:
        cpfs=bd.buscaInf(cnpj)
        if cpfs == False:
            return False
        else:
            caminhoFinal = os.path.join(os.getcwd(), "face")
            df_desconhecidos = pd.read_csv("faces_desconhecidos.csv")
            df_faces = df_desconhecidos
            for cpf in cpfs:
                nome = str(cpf) + ".csv"
                for filename in os.listdir(caminhoFinal):
                    if filename == nome:
                        nome = os.path.join(caminhoFinal, nome)
                        try:
                            face = pd.read_csv(nome)
                        except:
                            pass
                        face.drop(columns=['Unnamed: 0'])
                        df_faces = pd.concat(df_faces,face)
            X = np.array(df_faces.drop("target", axis=1))
            y = np.array(df_faces.target)
            return embaralhamento(X,y,cnpj)




def paroniza(face_pixels):
    face_pixels=face_pixels
    std = np.std(face_pixels)
    mean = np.mean(face_pixels)
    face_pixels = (face_pixels - mean) / std
    embe = get_embedding(face_pixels)
    return embe

def get_embedding(face_pixels):
    samples = expand_dims(face_pixels,axis=0)
    yhat = model.predict(samples)
    return yhat[0]

def extrair_face(arquivo, size=(160, 160)):

        array = asarray(arquivo)

        results = detector.detect_faces(array)

        x1, y1, width, height = results[0]['box']

        x2 = x1 + width

        y2 = y1 + height

        face = array[y1:y2 , x1:x2]

        image = Image.fromarray(face)
        image = image.resize(size)
        image=get_embedding(image)

        return image

def load_face(filename, required_size=(160,160)):
    image=Image.open(filename)
    image=image.convert("RGB")
    image=asarray(image)
    return image

def pegaRosto(image):
    image=detector.detect_faces(image)
    return image

def salvaRosto():
    caminho = os.path.join(os.getcwd(), "rostos")
    return caminho

def load_faces(directory_src,numeros,cpf):
    faces=list()
    numero=1
    for filename in os.listdir(directory_src):
        contador = numero
        nome=str(cpf)+str(contador)+".jpeg"
        if filename == nome:
            path = os.path.join(directory_src, filename)
            try:
                faces.append(load_face(path))
            except:
                print("erro na imagem {}".format(nome))
        if numero != numeros:
            numero = numero + 1

    return faces

def load_fotos(directory_src,cpf,numero):
    x,y = list(),list()
    faces=load_faces(directory_src,numero,cpf)
    labels=[cpf for _ in range(len(faces))]
    print('>Carregadas %d faces da classe: %s' % (len(faces),cpf))
    x.extend(faces)
    y.extend(labels)
    return asarray(x),asarray(y)

def extrair_rostos(arquivo, size=(160, 160)):
        img = Image.open(arquivo)

        img = img.convert('RGB')

        array = asarray(img)

        results = detector.detect_faces(array)

        x1, y1, width, height = results[0]['box']

        x2 = x1 + width

        y2 = y1 + height

        face = array[y1:y2, x1:x2]

        image = Image.fromarray(face)
        image = image.resize(size)

        return image

def trataFotos(cpf,numeros):
    caminhoInicio = os.path.join(os.getcwd(), "fotos")
    caminhoFinal = os.path.join(os.getcwd(), "rostos")
    numero = 1
    for filename in os.listdir(caminhoInicio):
        contador = numero
        nome = str(cpf) + str(contador) + ".jpeg"
        if filename == nome:
            path = os.path.join(caminhoInicio, filename)
            pathFinal = os.path.join(caminhoFinal, filename)
            try:
                foto=extrair_rostos(path)
                foto.save(pathFinal, quality=100, optimize=True, progressive=True)
                print(filename + " foi salva")
                os.remove(path)
                print(filename + " na pasta "+ path+" foi deletado ")

            except:
                print("erro na imagem {}".format(nome))
        if numero != numeros:
            numero = numero + 1
    return

def fotos(cpf,numero):
    trataFotos(cpf,numero)
    nome=str(cpf)+".csv"
    caminho=os.path.join(os.getcwd(),"rostos")
    caminhoFace = os.path.join(os.getcwd(), "face")
    trainx, trainy = load_fotos(caminho,cpf,numero)
    newTrainX = list()
    for face in trainx:
        embedding = paroniza(face)
        newTrainX.append(embedding)
    newTrainX = asarray(newTrainX)
    newTrainX.shape
    print(newTrainX)
    df = pd.DataFrame(data=newTrainX)
    df['target'] = trainy
    nome= os.path.join(caminhoFace,nome)
    df.to_csv(nome)
    deletaFace(cpf,numero)
    deletaRosto(cpf,numero)
    return "criado"


#deletando
def deletaFace(cpf,numeros):
    caminhoFinal = os.path.join(os.getcwd(), "face")
    numero = 1
    for filename in os.listdir(caminhoFinal):
        contador = numero
        nome = str(cpf) + str(contador) + ".jpeg"
        if filename == nome:
            path = os.path.join(caminhoFinal, filename)
            try:
                os.remove(path)
                print(filename + " na pasta " + path + " foi deletado ")
            except:
                print("erro na imagem {}".format(nome))
        if numero != numeros:
            numero = numero + 1
    return

def deletaRosto(cpf,numeros):
    caminhoFinal = os.path.join(os.getcwd(), "rostos")
    numero = 1
    for filename in os.listdir(caminhoFinal):
        contador = numero
        nome = str(cpf) + str(contador) + ".jpeg"
        if filename == nome:
            path = os.path.join(caminhoFinal, filename)
            try:
                os.remove(path)
                print(filename + " na pasta " + path + " foi deletado ")
            except:
                print("erro na imagem {}".format(nome))
        if numero != numeros:
            numero = numero + 1
    return

def deletaInteligen(cnpj):
    caminhoFinal = os.path.join(os.getcwd(), "inteligen")
    nome=str(cnpj)+".h5"
    for filename in os.listdir(caminhoFinal):
        if filename==nome:
            path = os.path.join(caminhoFinal, filename)
            try:
                os.remove(path)
                print(filename + " na pasta " + path + " foi deletado ")
                return True
            except:
                print("erro na imagem {}".format(nome))
                return False
#-------------------------


#invertendo Imagem
def flip_image(image):
        img = image.transpose(Image.FILP_LEFT_RIGHT)
        return img
#-------------------------

#reconhecimento
def compara(frame,ModeloTreinado,pessoas):
    print(frame)
    print("comparando")
    faces = detector.detect_faces(frame)
    print("loop faces")
    for face in faces:
        print("ola")
        confidence = face['confidence'] * 100
        print(confidence)
        print(face['box'])
        if confidence >= 98:
            x1, y1, w, h = face['box']
            print(face['box'])
            y2 = y1 + h
            x2 = x1 + w
            face = extrair_face_reconhecimento(frame,face['box'])
            print("face:")

            face = face.astype("float32") / 255
            print("face")

            emb = get_embedding_reconhecimento(model,face)
            print("emb")
            tensor = np.expand_dims(emb, axis=0)
            print("tensor")
            norm = Normalizer(norm="l2")
            tensor = norm.transform(tensor)
            print(tensor)
            classe = ModeloTreinado.predict_classes(tensor)[0]
            print(classe)
            prob = ModeloTreinado.predict_proba(tensor)
            print(prob)
            prob = prob[0][classe] * 100
            print(classe)
            print(prob)
            user = str(pessoas[classe]).upper()
            print(user)
            if prob >= 98:

                if classe == 1:
                    color = (0, 0, 255)
                else:
                    color = (192, 0, 0)  # bgr

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                font = cv2.FONT_HERSHEY_SIMPLEX
                fonte_scale = 0.5

                cv2.putText(frame, user, (x1, y1 - 10), font, fonte_scale, color, thickness=1)
    return frame

def extrair_face_reconhecimento(image, box, size=(160, 160)):

    pixels = np.asarray(image)

    x1, y1, width, height = box

    x2 = x1 + width

    y2 = y1 + height

    face = pixels[y1:y2, x1:x2]

    image = Image.fromarray(face)
    image = image.resize(size)
    return np.asarray(image)

def get_embedding_reconhecimento(facenet, face_pixels):

    face_pixels=face_pixels.astype('float32')
    std = np.std(face_pixels)
    mean = np.mean(face_pixels)
    face_pixels = (face_pixels - mean) / std

    samples = np.expand_dims(face_pixels, axis=0)
    yhat=facenet.predict(samples)
    return yhat[0]
#-------------------------