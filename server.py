import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import socket
import numpy as np
import tflearn
from tensorflow.python.framework import ops
import random
import json
import pickle
from datetime import datetime
from search_api import search

def read_data():
    with open("intents.json") as file:
        data = json.load(file)

    try:
        with open("data.pickle", "rd") as f:
            words, labels, training, output = pickle.load(f)
    except:
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                w = nltk.word_tokenize(pattern)
                words.extend(w)
                docs_x.append(w)
                docs_y.append(intent["tag"])

                if intent["tag"] not in labels:
                    labels.append(intent["tag"])

        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        words = list(set(words)) # remove duplication
        words = sorted(words)

        print(len(words))

        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = []
            wrds = [stemmer.stem(w.lower()) for w in doc]
            for word in words:
                if word in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            out = out_empty[:]
            out[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(out)

        training = np.array(training)
        output = np.array(output)

        with open("data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)
    finally:
        return words, labels, training, output, data



def create_model(training, output):
    ops.reset_default_graph()
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    model.load("model.tflearn")
    # model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    # model.save("model.tflearn")

    return model



def bag_of_words(s, words):
    bag = []
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(w.lower()) for w in s_words]

    for word in words:
        if word in s_words:
            bag.append(1)
        else:
            bag.append(0)
        
    return np.array(bag)

if __name__ == "__main__":
    # Read data and create model
    print("Starting...")
    words, labels, training, output, data = read_data()
    print("Data read...")
    model = create_model(training, output)
    print("Model created...")

    # Create socket connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 6969

    # Bind socket to port
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Waiting for connections...")

    # Accept connection
    client_socket, addr = server_socket.accept()
    print("Got a connection from %s" % str(addr))

    while True:
        inp = client_socket.recv(1024).decode("utf-8")
        if inp.lower() == "exit":
            client_socket.send("exit".encode("utf-8"))
            break

        result = model.predict([bag_of_words(inp, words)])
        tag = labels[np.argmax(result)]
        ans = ""

        if tag == "time":
            ans = datetime.now().time()
        elif tag == "date":
            ans = datetime.now().date()
        else:
            if tag == "game":
                client_socket.sendall(tag.encode("utf-8"))
                client_socket.recv(1024).decode("utf-8")
            for intent in data["intents"]:
                if intent["tag"] == tag:
                    ans = random.choice(intent["responses"])
                    if tag == "search":
                        client_socket.send(ans.encode("utf-8"))
                        query = client_socket.recv(1024).decode("utf-8")
                        results = search(query)
                        cnt = min(5, len(results))
                        ans = "Here are the top " + str(cnt) + " results:"
                        client_socket.sendall(ans.encode("utf-8"))
                        for result in results:
                            if cnt == 0:
                                break
                            ans = result["title"]
                            client_socket.sendall(ans.encode("utf-8"))
                            client_socket.recv(1024).decode("utf-8")
                            ans = result["link"]
                            client_socket.sendall(ans.encode("utf-8"))
                            client_socket.recv(1024).decode("utf-8")
                            cnt -= 1

                        ans = "Searching is performed by google search engine!"
                    break
        client_socket.send(ans.encode("utf-8"))
    
    client_socket.close()


