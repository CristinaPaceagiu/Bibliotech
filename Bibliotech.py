from flask import Flask, request, Response
from datetime import date
from random import randrange
import json
from UtilsUsers import checkCredentials, createAuthToken, autentificareUser, userEmail 
from UtilsBooks import book_id, identificareBookId, bookStatus, modificBookStatus, authorReview, validareRating, calculRating
from UtilsTransactions import numarTranzactiiUser, transactionId, validareTransactionId, remainingTime, transactionStatus, createId
from UtilsTransactions import numarExtinderi, adaugExtindere, createReturnRequest, numarAbateri, createAbatere, addAbatere, modificTransactionStatus
from UtilsTransactions import returnRequestStatus, endReturnRequest, returnRequestTransactionId, returnRequestTransactionBookId, decrementareNumarAbateri


app = Flask(__name__)


# 1.Autentificare si inregistrare 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route("/")
def homepage():
    with open("B_logs.txt", "a") as dbase:
        dbase.write(str(createId("B_logs.txt")) + ";" + str(date.today()) + ";" + "visitor in Bibliotech" + "\n")
    
    return Response(response="Welcome to Bibliotech!", status=200)    


# 1.1.POST/register
@app.route("/register", methods = ["POST"])
def register():
    data = request.get_json("http://localhost:5000/register")

    lines = []
    with open("B_users.txt", 'r') as dbase:
        lines = dbase.readlines()
    
    for line in lines:
        if line.split(";")[2] == data['email']:
            respDict = {}
            respDict["error"] = "User already registered."
            return Response(json.dumps(respDict, indent=4), 409)
    
    if len(data['first_name']) < 5 or len(data['password']) < 7:
        respDict = {}
        respDict["error"] = "Invalid length for first_name or password."
        return Response(json.dumps(respDict, indent=4), 411)
        
    else:
        with open("B_logs.txt", 'a+') as dbase:                  
            dbase.write(str(createId("B_logs.txt")) + ";" + str(date.today()) + ";" + "register user" + ";" + 
                        data['first_name'] + ";" + data['last_name'] + ";" + 
                        data['email'] + ";" + data['password'] + ";" + data['type'] + "\n")
        
        with open("B_users.txt", 'a+') as dbase:                  
            dbase.write(data['first_name'] + ";" + data['last_name'] + ";" + data['email'] + ";" + 
                        data['password'] + ";" + data['type'] + "\n")

        respDict = {}
        respDict["first_name"] = data['first_name']
        respDict["last_name"] = data['last_name']
        respDict["email"] = data['email']
        respDict["type"] = data['type']

        return Response(json.dumps(respDict, indent=4), 200)
    

# 1.2.POST/login
@app.route("/login", methods = ["POST"])
def login():    
    data = request.get_json("http://localhost:5000/login")

    if checkCredentials(data['email'], data['password']):
        with open("B_logs.txt", 'a+') as dbase:
            dbase.write(str(createId("B_logs.txt")) + ";" + str(date.today()) + ";" + "create auth_token" + ";" + 
                        data['email'] + ";" + data['password'] + ";" + createAuthToken(data['email'], data['password']) + "\n")

        respDict = {}
        respDict['auth_token'] = createAuthToken(data['email'], data['password'])
        return Response(json.dumps(respDict, indent=4), 200)
    else:
        respDict = {}
        respDict["error"] = "User not found. Email or password incorrect."
        return Response(json.dumps(respDict, indent=4), 401)     
    

# 2.Gestionarea cartilor 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
# 2.1.POST/book   
@app.route("/add/book", methods = ["POST"])
def addBook():
    data = request.get_json("http://localhost:5000/add/book")

    if autentificareUser(data['auth_token']) == "1":        
        lines = []
        with open("B_books.txt", 'r') as dbase:
            lines = dbase.readlines()

        for line in lines:
            if line.split(";")[1] == data['book_name'] and line.split(";")[2] == data['book_author']:        
                respDict = {}
                respDict["error"] = "Book already in Bibliotech."
            
                return Response(json.dumps(respDict, indent=4), 403)
          
        with open("B_books.txt", "a") as dbase:   
            bookId = book_id()       
            dbase.write(str(bookId) + ";" + data['book_name'] + ";" + data['book_author'] + ";" + 
                        data['book_description'] + ";" + "disponibila" + "\n")

            respDict = {}
            respDict["id"] = str(bookId)
            respDict["book_name"] = data['book_name']
            respDict["book_author"] = data['book_author']
            respDict["book_description"] = data['book_description']

            return Response(json.dumps(respDict, indent=4), 200)
        
    else:
        respDict = {}
        respDict["error"] = "Invalid user or admin role."
            
        return Response(json.dumps(respDict, indent=4), 403)


# 2.2.POST/books
@app.route("/add/books", methods = ["POST"])
def addBooks():
    data = request.get_json("http://localhost:5000/add/books")

    if autentificareUser(data['auth_token']) == "1":     
        dataList = []
        dataList = data['books']
        respDict = {}
        listaDict = []

        for item in dataList:
            lines = []
            with open("B_books.txt", 'r') as dbase:
                lines = dbase.readlines()
            for line in lines:
                if line.split(";")[1] == item["book_name"] and line.split(";")[2] == item["book_author"]:
                    respDict = {}
                    respDict["error"] = "Book already in Bibliotech."
            
                    return Response(json.dumps(respDict, indent=4), 403)                
            
            with open("B_books.txt", "a") as dbase:   
                bookId = book_id()       
                dbase.write(str(bookId) + ";" + item['book_name'] + ";" + item['book_author'] + ";" + 
                            item['book_description'] + ";" + "disponibila" + "\n")              
                
            dict = {}                        
            dict["id"] = bookId
            dict["book_name"] = item['book_name']
            dict["book_author"] = item['book_author']
            dict["book_description"] = item['book_description']            
            listaDict.append(dict)
            
        respDict["books"] = listaDict
                
        return Response(json.dumps(respDict, indent=4), 200)

    else:
        respDict = {}
        respDict["error"] = "Invalid user or admin role."
            
        return Response(json.dumps(respDict, indent=4), 403)


# 2.3.GET/book
@app.route("/get/book", methods = ["GET"])
def getBook():
    data = request.get_json("http://localhost:5000/get/book")
    
    if autentificareUser(data['auth_token']) == "1" or autentificareUser(data['auth_token']) == "0" or autentificareUser(data['auth_token']) == None:
        if identificareBookId(data['book_id']):        
            respDict = {}
            respDict["id"] = data['book_id']

            lines1 = []
            with open("B_books.txt", 'r') as dbase1:
                lines1 = dbase1.readlines()
                
            for line in lines1:
                if line.split(";")[0] == data['book_id']:
                    respDict["title"] = line.split(";")[1]
                    respDict["author"] = line.split(";")[2]
                    respDict["book_description"] = line.split(";")[3]
                    respDict["status"] = line.split(";")[4].strip()

            respDict["rating"] = calculRating(data['book_id'])
            
            lines2 = []
            with open("B_reviews.txt", 'r') as dbase2:
                lines2 = dbase2.readlines()

            listaDict = []
            for line in lines2:
                dict = {}
                if line.split(";")[0] == data['book_id']:                    
                    dict["rating"] = line.split(";")[1]
                    dict["review"] = line.split(";")[2]
                    if data['auth_token'] != None:
                        dict["author"] = line.split(";")[3].strip()
                    listaDict.append(dict)

            respDict["reviews"] = listaDict
                
            return Response(json.dumps(respDict, indent=4), 200)          
                
        else:
                respDict = {}
                respDict["error"] = "Invalid book_id."
                
                return Response(json.dumps(respDict, indent=4), 404)           

# 2.4.GET/books
@app.route("/get/books", methods = ["GET"])
def getBooks():
    #data = request.get_json("http://localhost:5000/get/books")

    respDict = {}
    lines = []
    with open("B_books.txt", 'r') as dbase:
        lines = dbase.readlines()

    listaDict = []
    for line in lines:
        dict = {}                        
        dict["id"] = line.split(";")[0]
        dict["title"] = line.split(";")[1]
        dict["author"] = line.split(";")[2]
        dict["description"] = line.split(";")[3]
        dict["status"] = line.split(";")[4].strip()   
        dict["rating"] = calculRating(line.split(";")[0])   
        listaDict.append(dict)

    if not listaDict:
        respDict = {}
        respDict["error"] = "No book in Bibliotech."
            
        return Response(json.dumps(respDict, indent=4), 404)

    else:       
        respDict["books"] = listaDict
                
        return Response(json.dumps(respDict, indent=4), 200)


# 3.Interactiunea cu Bibliotech
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3.1.POST/transaction
@app.route("/add/transaction", methods = ["POST"])
def addTransaction():
    data = request.get_json("http://localhost:5000/add/transaction")   

    if autentificareUser(data['auth_token']) == "1" or autentificareUser(data['auth_token']) == "0":
        if identificareBookId(data['book_id']):
            if bookStatus(data['book_id']) == "disponibila":
                if numarTranzactiiUser(userEmail(data['auth_token'])) < 5:
                    transId = transactionId()
                    with open("B_tranzactii.txt", "a") as dbase:             
                        dbase.write(str(transId) + ";" + userEmail(data['auth_token']) + ";" + data['book_id'] + ";" + 
                                    str(date.today()) + ";" + data['borrow_time'] + ";" + "in desfasurare" + ";" + "0" + "\n")

                    modificBookStatus(data['book_id'], "imprumutata")

                    respDict = {}
                    respDict["success"] = "Ai imprumutat cartea solicitata."
                    respDict["transaction_id"] = str(transId)
                    
                    return Response(json.dumps(respDict, indent=4), 200)               

                else:
                    respDict = {}
                    respDict["error"] = "Numarul maxim de 5 tranzactii a fost atins. Poti imprumuta o alta carte dupa un retur."
            
                    return Response(json.dumps(respDict, indent=4), 403)

            else:
                respDict = {}
                respDict["error"] = "Cartea este indisponibila momentan."
            
                return Response(json.dumps(respDict, indent=4), 404)        

        else:
            respDict = {}
            respDict["error"] = "Cartea nu exista in Bibliotech."
            
            return Response(json.dumps(respDict, indent=4), 404)

    else:
        respDict = {}
        respDict["error"] = "Invalid user."
            
        return Response(json.dumps(respDict, indent=4), 403)


# 3.2.GET/transaction
@app.route("/get/transaction", methods = ["GET"])
def getTransaction():
    data = request.get_json("http://localhost:5000/get/transaction")

    if autentificareUser(data['auth_token']) == "1" or autentificareUser(data['auth_token']) == "0":
        if validareTransactionId(data['transaction_id']):
            lines = []
            with open("B_tranzactii.txt", 'r') as dbase:
                lines = dbase.readlines()

            for line in lines:
                if line.split(";")[0] == data['transaction_id']:
                    if line.split(";")[1] == userEmail(data['auth_token']):
                        respDict = {}   
                        respDict["book_id"] = int(line.split(";")[2])
                        respDict["borrow_time"] = line.split(";")[4]
                        respDict["remaining_time"] = remainingTime(line.split(";")[4], line.split(";")[3])
                        respDict["number_of_extensions"] = line.split(";")[6].strip()
                        respDict["status"] = line.split(";")[5]

                        return Response(json.dumps(respDict, indent=4), 200)
                    
                    else:
                        respDict = {}
                        respDict["error"] = "Nu aveti acces la tranzactia altui user."
            
                        return Response(json.dumps(respDict, indent=4), 403)                   
                      
        else:
            respDict = {}
            respDict["error"] = "Invalid transaction_id."
            
            return Response(json.dumps(respDict, indent=4), 404)

    else:
        respDict = {}
        respDict["error"] = "Invalid user."
            
        return Response(json.dumps(respDict, indent=4), 403)
    

# 3.3.GET/transactions
@app.route("/get/transactions", methods = ["GET"])
def getTransactions():
    data = request.get_json("http://localhost:5000/get/transactions")

    if autentificareUser(data['auth_token']) == "0":
        respDict = {}
        lines = []
        with open("B_tranzactii.txt", 'r') as dbase:
            lines = dbase.readlines()

        listaDict = []
        for line in lines:
            dict = {}
            if line.split(";")[1] == userEmail(data['auth_token']):                    
                dict["transaction_id"] = line.split(";")[0]
                dict["book_id"] = line.split(";")[2]
                bookId = line.split(";")[2]

                lines2 = []
                with open("B_books.txt", 'r') as dbase2:
                    lines2 = dbase2.readlines()
                for line2 in lines2:
                    if line2.split(";")[0] == bookId:
                        dict["book_name"] = line2.split(";")[1]
                
                dict["status"] = line.split(";")[5].strip()
                listaDict.append(dict)

        if not listaDict:
            respDict = {}
            respDict["error"] = "No transaction for this user."
            
            return Response(json.dumps(respDict, indent=4), 404)

        else:       
            respDict["transactions"] = listaDict
                
            return Response(json.dumps(respDict, indent=4), 200)


    elif autentificareUser(data['auth_token']) == "1":
        respDict = {}
        lines = []
        with open("B_tranzactii.txt", 'r') as dbase:
            lines = dbase.readlines()

        listaDict = []
        for line in lines:
            dict = {}
                          
            dict["transaction_id"] = line.split(";")[0]
            dict["book_id"] = line.split(";")[2]
            bookId = line.split(";")[2]

            lines2 = []
            with open("B_books.txt", 'r') as dbase2:
                lines2 = dbase2.readlines()
            for line2 in lines2:
                if line2.split(";")[0] == bookId:
                    dict["book_name"] = line2.split(";")[1]
                
            dict["status"] = line.split(";")[5].strip()
            listaDict.append(dict)

        if not listaDict:
            respDict = {}
            respDict["error"] = "No transactions in Bibliotech."
            
            return Response(json.dumps(respDict, indent=4), 404)

        else:       
            respDict["transactions"] = listaDict
                
            return Response(json.dumps(respDict, indent=4), 200)

    else:
        respDict = {}
        respDict["error"] = "Invalid user."
            
        return Response(json.dumps(respDict, indent=4), 403)

                
# 3.4.POST/extend
@app.route("/extend", methods = ["POST"])
def extendBorrowTime():
    data = request.get_json("http://localhost:5000/extend")

    if autentificareUser(data['auth_token']) == "1" or autentificareUser(data['auth_token']) == "0":
        if validareTransactionId(data['transaction_id']):
            if transactionStatus(data['transaction_id']) == "in desfasurare" or transactionStatus(data['transaction_id']) == "in intarziere":
                if int(data['extend_time']) >=1 and int(data['extend_time']) <=5:
                    if int(numarExtinderi(data['transaction_id'])) < 2:
                        adaugExtindere(data['transaction_id'], data['extend_time'])
                        
                        respDict = {}
                        respDict["success"] = f"Timpul de imprumut a fost extins cu {int(data['extend_time'])} zile."
            
                        return Response(json.dumps(respDict, indent=4), 200)

                    else:
                        respDict = {}
                        respDict["error"] = "Numarul maxim de extinderi a fost atins."
            
                        return Response(json.dumps(respDict, indent=4), 403)

                else:
                    respDict = {}
                    respDict["error"] = "Timpul de extindere trebuie sa fie intre 1 si 5 inclusiv."
            
                    return Response(json.dumps(respDict, indent=4), 403)

            else:
                respDict = {}
                respDict["error"] = "Tranzactie incheiata. Durata nu poate fi extinsa."
            
                return Response(json.dumps(respDict, indent=4), 403)

        else:
            respDict = {}
            respDict["error"] = "Invalid transaction_id."
            
            return Response(json.dumps(respDict, indent=4), 404)

    else:
        respDict = {}
        respDict["error"] = "Invalid user."
            
        return Response(json.dumps(respDict, indent=4), 403)
    

# 3.5.POST/return
@app.route("/add/return", methods = ["POST"])
def addReturn():
    data = request.get_json("http://localhost:5000/add/return") 

    if autentificareUser(data['auth_token']) == "1" or autentificareUser(data['auth_token']) == "0":
        if validareTransactionId(data['transaction_id']):
            lines = []
            with open("B_tranzactii.txt", 'r') as dbase:
                lines = dbase.readlines()

            for line in lines:
                if line.split(";")[0] == data['transaction_id']:
                    if line.split(";")[1] == userEmail(data['auth_token']):
                    
                        if transactionStatus(data['transaction_id']) == "in desfasurare" or transactionStatus(data['transaction_id']) == "in intarziere":
                        
                            lines = []
                            with open("B_tranzactii.txt", 'r') as dbase:
                                lines = dbase.readlines()

                            for line in lines:
                                if line.split(";")[0] == data['transaction_id']:
                                    if remainingTime(line.split(";")[4], line.split(";")[3]) < 0: 
                                        modificTransactionStatus(data['transaction_id'], "in intarziere")                                        
                                        # decrementareNumarAbateri(userEmail(data['auth_token']))

                                        if numarAbateri(userEmail(data['auth_token'])) == '0' or numarAbateri(userEmail(data['auth_token'])) == None:
                                            createReturnRequest(data['auth_token'], data['transaction_id'])
                                            createAbatere(userEmail(data['auth_token']), 1)

                                            respDict = {}
                                            respDict["success"] = "Ai creat o cerere de returnare cu succes, insa ai depasit termenul de returnare. Fiind la prima abatere ai acumulat un punct de penalizare (atentionare), care va expira peste 30 de zile."
                
                                            return Response(json.dumps(respDict, indent=4), 200)
                                        
                                        elif numarAbateri(userEmail(data['auth_token'])) == '1':
                                            createReturnRequest(data['auth_token'], data['transaction_id'])
                                            addAbatere(userEmail(data['auth_token']), 2)

                                            respDict = {}
                                            respDict["success"] = "Ai creat o cerere de returnare cu succes, insa ai depasit termenul de returnare. Esti la a doua abatere si ai acumulat doua puncte de penalizare, ti-a fost redus numarul de extinderi, de la 2 la 1. Numarul de abateri va fi decrementat dupa 30 de zile."
                
                                            return Response(json.dumps(respDict, indent=4), 200)
                                        
                                        elif numarAbateri(userEmail(data['auth_token'])) == '2':
                                            createReturnRequest(data['auth_token'], data['transaction_id'])
                                            addAbatere(userEmail(data['auth_token']), 3)

                                            respDict = {}
                                            respDict["success"] = "Ai creat o cerere de returnare cu succes, insa ai depasit termenul de returnare. Esti la a treia abatere si ai acumulat trei puncte de penalizare, ti-a fost eliminat numarul de extinderi. Numarul de abateri va fi decrementat dupa 30 de zile."
                
                                            return Response(json.dumps(respDict, indent=4), 200)
                                        
                                        elif numarAbateri(userEmail(data['auth_token'])) == '3':
                                            createReturnRequest(data['auth_token'], data['transaction_id'])
                                            addAbatere(userEmail(data['auth_token']), 4)

                                            respDict = {}
                                            respDict["success"] = "Ai creat o cerere de returnare cu succes, insa ai depasit termenul de returnare. Esti la a patra abatere si ai acumulat patru puncte de penalizare, fiindu-ti blocata posibilitatea de a imprumuta carti pentru o perioada de 30 de zile. Numarul de abateri va fi decrementat dupa 30 de zile."
                
                                            return Response(json.dumps(respDict, indent=4), 200)     

                                        else:
                                            respDict = {}
                                            respDict["error"] = "Invalid request! Please contact the Bibliotech."
                
                                            return Response(json.dumps(respDict, indent=4), 400)                          

                                        
                                    else:
                                        createReturnRequest(data['auth_token'], data['transaction_id'])
                                        
                                        respDict = {}
                                        respDict["success"] = "Ai creat o cerere de returnare cu succes."
                
                                        return Response(json.dumps(respDict, indent=4), 200)                
                                        
                        else:
                            respDict = {}
                            respDict["error"] = "Tranzactie deja incheiata."
                
                            return Response(json.dumps(respDict, indent=4), 403)

                    else:
                        respDict = {}
                        respDict["error"] = "Nu aveti acces la tranzactia altui user."
                
                        return Response(json.dumps(respDict, indent=4), 403)   
                    
        else:
            respDict = {}
            respDict["error"] = "Invalid transaction_id."
            
            return Response(json.dumps(respDict, indent=4), 404)

    else:
        respDict = {}
        respDict["error"] = "Invalid user."
            
        return Response(json.dumps(respDict, indent=4), 403)
                    
                
# 3.6.GET/returns
@app.route("/get/returns", methods = ["GET"])
def getReturns():
    data = request.get_json("http://localhost:5000/get/returns")

    if autentificareUser(data['auth_token']) == "1":
        respDict = {}
        lines = []
        with open("B_returnReq.txt", 'r') as dbase:
            lines = dbase.readlines()

        listaDict = []
        for line in lines:
            if line.split(";")[3].strip() == '1':
                dict = {}
                dict["id"] = int(line.split(";")[0])
                dict["transaction_id"] = int(line.split(";")[1])
                listaDict.append(dict)

        if not listaDict:
            respDict = {}
            respDict["error"] = "Nicio cerere de returnare activa."
            
            return Response(json.dumps(respDict, indent=4), 404)

        else:       
            respDict["return_requests"] = listaDict
                
            return Response(json.dumps(respDict, indent=4), 200)

    else:
        respDict = {}
        respDict["error"] = "Invalid user Admin."
            
        return Response(json.dumps(respDict, indent=4), 403)


# 3.7.POST/return/end
@app.route("/return/end", methods = ["POST"])
def endReturn():
    data = request.get_json("http://localhost:5000/return/end") 

    if autentificareUser(data['auth_token']) == "1":
        if returnRequestStatus(data['return_id']) == "1":
            endReturnRequest(data['return_id'])
            modificTransactionStatus(returnRequestTransactionId(data['return_id']), "incheiata")
            modificBookStatus(returnRequestTransactionBookId(data['return_id']), "disponibila")

            respDict = {}
            respDict["success"] = "Cartea a fost inapoiata."
                
            return Response(json.dumps(respDict, indent=4), 200)

        else:
            respDict = {}
            respDict["error"] = "Tranzactia este deja incheiata."
            
            return Response(json.dumps(respDict, indent=4), 403)

    else:
        respDict = {}
        respDict["error"] = "Invalid user Admin."
            
        return Response(json.dumps(respDict, indent=4), 403)


# 3.8.POST/review
@app.route("/review", methods = ["POST"])
def review():
    data = request.get_json("http://localhost:5000/review")

    if autentificareUser(data['auth_token']) == "1" or autentificareUser(data['auth_token']) == "0":
        if identificareBookId(data['book_id']) and validareRating(int(data['rating'])):
            with open("B_reviews.txt", "a") as dbase:             
                dbase.write(data['book_id'] + ";" + data['rating'] + ";" + data['review'] + ";" + 
                            authorReview(data['auth_token']) + "\n")

            respDict = {}
            respDict["success"] = "Review adaugat cu succes."
            
            return Response(json.dumps(respDict, indent=4), 200)
        
        else:
            respDict = {}
            respDict["error"] = "Review-ul nu a fost adaugat (carte neidentificata sau rating invalid)."
            
            return Response(json.dumps(respDict, indent=4), 404)
    
    else:
        respDict = {}
        respDict["error"] = "Invalid user."
            
        return Response(json.dumps(respDict, indent=4), 403)




if __name__ == "__main__":
    app.run(debug=True)
