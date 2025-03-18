from datetime import date
from UtilsUsers import userEmail

def numarTranzactiiUser(user):
    """
    Functia calculeaza numarul de tranzactii pe user, si este folosita in script pentru a determina 
    daca un user poate sa faca o noua tranzactie (maxim 5).
    """
    countTranzactii = 0
    lines = []
    with open("B_tranzactii.txt", 'r') as dbase:
        lines = dbase.readlines()    
    
    for line in lines:
        if line.split(";")[1] == user and (line.split(";")[5].strip() == "in desfasurare" or 
                                                 line.split(";")[5].strip() == "in intarziere"):
            countTranzactii += 1

    return countTranzactii


def transactionId():
    """
    Functia genereaza un identificator unic pentru o tranzactie.
    """    
    lines = []
    maxId = 0

    with open("B_tranzactii.txt", 'r') as dbase:
        lines = dbase.readlines()     
    
    for line in lines:
        if int(line.split(";")[0]) > maxId:
            maxId = int(line.split(";")[0])

    return maxId + 1


def validareTransactionId(transaction_id):
    """
    Functia identifica o tranzactie dupa transaction_id primit.
    """
    lines = []
    with open("B_tranzactii.txt", 'r') as dbase:
        lines = dbase.readlines()
    
    for line in lines:
        if line.split(";")[0] == transaction_id:
            return True
        
    return False


def transactionStatus(transaction_id):
    """
    Functia returneaza statusul unei tranzactii (in desfasurare/incheiata/in intarziere).
    """
    lines = []
    with open("B_tranzactii.txt", 'r') as dbase:
        lines = dbase.readlines()
    
    for line in lines:
        if line.split(";")[0] == transaction_id:
            return line.split(";")[5]
        
    return None


def remainingTime(borrow_time, borrow_date):
    """
    Functia calculeaza numarul de zile pana la data de returnare in functie de durata imprumutului, data imprumutului 
    si data curenta. Rezultatul poate fi negativ in cazul in care durata impumutului a fost depasita.
    """
    year = int(borrow_date.split("-")[0])
    month = int(borrow_date.split("-")[1])
    day = int(borrow_date.split("-")[2])

    borrowDaysToPresent = date.today() - date(year, month, day)
    zile = borrowDaysToPresent.days      

    return int(borrow_time) - zile


def numarExtinderi(transaction_id):
    """
    Functia returneaza numarul de extinderi pentru o tranzactie.
    """
    lines = []
    with open("B_tranzactii.txt", 'r') as dbase:
        lines = dbase.readlines()    
    
    for line in lines:
        if line.split(";")[0] == transaction_id:
            return line.split(";")[6].strip()

    return None


def adaugExtindere(transaction_id, extend_time):
    """
    Functia adauga extinderi in fisierul B_tranzactii.txt.
    """
    lines = []
    with open("B_tranzactii.txt", 'r') as dbase:
        lines = dbase.readlines()    

    with open("B_tranzactii.txt", 'w') as dbase:        
        for line in lines:
            if line.split(";")[0] == transaction_id:
                newBorrowTime = int(line.split(";")[4]) + int(extend_time)
                newNumberExtensions = int(line.split(";")[6]) + 1
                dbase.write(line.split(";")[0] + ";" + line.split(";")[1] + ";" + line.split(";")[2] + ";" + line.split(";")[3] + 
                            ";" + str(newBorrowTime) + ";" + "in desfasurare" + ";" + str(newNumberExtensions) + "\n")
                
            else:
                dbase.write(line)


def createId(fisier):
    """
    Functia genereaza un identificator unic. Am folosit-o in functia urmatoare.
    """
    lines = []
    maxId = 0

    with open(fisier, 'r') as dbase:
        lines = dbase.readlines()     
    
    for line in lines:
        if int(line.split(";")[0]) > maxId:
            maxId = int(line.split(";")[0])

    return maxId + 1


def createReturnRequest(auth_token, transaction_id):
    """
    Functia genereaza o cerere de returnare pe care o adauga in fisierul B_returnReq.txt.
    """
    with open("B_returnReq.txt", "a") as dbase:             
        dbase.write(str(createId("B_returnReq.txt")) + ";" + transaction_id + ";" + 
                    userEmail(auth_token) + ";" + "1" + "\n")
        

def numarAbateri(user):
    """
    Functia returneaza numarul de abateri ale unui utilizator.    
    """
    lines = []
    with open("B_abateri.txt", 'r') as dbase:
        lines = dbase.readlines()     
    
    for line in lines:
        if line.split(";")[0] == user:
            return line.split(";")[2].strip()
        
    return None


def createAbatere(user, numar):
    """
    Functia genereaza prima abatere pentru un user, in fisierul B_abateri.txt.
    """
    with open("B_abateri.txt", "a") as dbase:             
        dbase.write(user + ";" + str(date.today()) + ";" + str(numar) + "\n")


def addAbatere(user, numar):
    """
    Functia modifica numar de abateri pentru un user, in fisierul B_abateri.txt.
    """
    lines = []
    with open("B_abateri.txt", 'r') as dbase:
        lines = dbase.readlines()    

    with open("B_abateri.txt", 'w') as dbase:        
        for line in lines:
            if line.split(";")[0] == user:
                dbase.write(user + ";" + line.split(";")[1] + ";" + str(numar) + "\n")
                
            else:
                dbase.write(line)


def modificTransactionStatus(transaction_id, newStatus):
    """
    Functia modifica statusul unei tranzactii (in desfasurare/incheiata/in intarziere).
    """
    lines = []
    with open("B_tranzactii.txt", 'r') as dbase:
        lines = dbase.readlines()    

    with open("B_tranzactii.txt", 'w') as dbase:        
        for line in lines:
            if line.split(";")[0] == transaction_id:
                dbase.write(line.split(";")[0] + ";" + line.split(";")[1] + ";" + line.split(";")[2] + ";" + 
                                    line.split(";")[3] + ";" + line.split(";")[4] + ";" + newStatus + ";" + line.split(";")[6])
                
            else:
                dbase.write(line)


def returnRequestStatus(return_id):
    """
    Functia returneaza statusul unei cereri de returnare (1-activa, 0-incheiata).
    """
    lines = []
    with open("B_returnReq.txt", 'r') as dbase:
        lines = dbase.readlines()
    
    for line in lines:
        if line.split(";")[0] == return_id:
            return line.split(";")[3].strip()            
        
    return False


def endReturnRequest(return_id):
    """
    Functia modifica statusul unei cereri de returnare la incheierea unei tranzactii (status 0).
    """
    lines = []
    with open("B_returnReq.txt", 'r') as dbase:
        lines = dbase.readlines()    

    with open("B_returnReq.txt", 'w') as dbase:        
        for line in lines:
            if line.split(";")[0] == return_id:
                dbase.write(line.split(";")[0] + ";" + line.split(";")[1] + ";" + 
                    line.split(";")[2] + ";" + "0" + "\n")
                
            else:
                dbase.write(line)


def returnRequestTransactionId(return_id):
    """
    Functia returneaza numarul unei tranzactii asociata unei cereri de returnare.
    """
    lines = []
    with open("B_returnReq.txt", 'r') as dbase:
        lines = dbase.readlines()
    
    for line in lines:
        if line.split(";")[0] == return_id:
            return line.split(";")[1]            
        
    return False


def returnRequestTransactionBookId(return_id):
    """
    Functia returneaza numarul unei carti asociata unei cereri de returnare.
    """
    lines = []
    with open("B_tranzactii.txt", 'r') as dbase:
        lines = dbase.readlines()
    
    for line in lines:
        if line.split(";")[0] == returnRequestTransactionId(return_id):
            return line.split(";")[2]            
        
    return False


def decrementareNumarAbateri(user):
    """
    Functia decrementeaza numarul de abateri, dupa 30 de zile de la data primei abateri, in functie de data curenta.
    """
    lines = []
    with open("B_abateri.txt", 'r') as dbase:
        lines = dbase.readlines()
    numarZileAbatere = 0
    for line in lines:
        if line.split(";")[0] == user:
            year = int(line.split(";")[1].split("-")[0])
            month = int(line.split(";")[1].split("-")[1])
            day = int(line.split(";")[1].split("-")[2])

            numarZileAbatere = (date.today() - date(year, month, day)).days
            numarAbateri = int(line.split(";")[2])

            while numarAbateri != 0:
                if numarZileAbatere > 30:
                    numarAbateri -= 1
                    numarZileAbatere -= 30
            
            


                





