from UtilsUsers import userEmail

def book_id():    
    """
    Functia genereaza un identificator unic pentru o carte introdusa in Bibliotech.
    """
    lines = []
    maxId = 0

    with open("B_books.txt", 'r') as dbase:
        lines = dbase.readlines()     
    
    for line in lines:
        if int(line.split(";")[0]) > maxId:
            maxId = int(line.split(";")[0])

    return maxId + 1


def identificareBookId(book_id):
    """
    Functia identifica cartea dupa 'book_id' in 'B_books.txt'.
    """
    lines = []
    with open("B_books.txt", 'r') as dbase:
        lines = dbase.readlines()

    for line in lines:
        if line.split(";")[0] == book_id:
            return True
        
    return False


def bookStatus(book_id):
    """
    Functia extrage valoarea campului 'book_status' (imprumutata/disponibila/blocata).
    """
    lines = []
    with open("B_books.txt", 'r') as dbase:
        lines = dbase.readlines()     
    
    for line in lines:
        if line.split(";")[0] == book_id:
            return line.split(";")[4].strip()
        
    return None


def modificBookStatus(book_id, status): 
    """
    Functia modifica statusul cartii (imprumutata/disponibila/blocata) in fisierul B_books.txt.
    """   
    lines = []
    with open("B_books.txt", 'r') as dbase:
        lines = dbase.readlines()
    
    with open("B_books.txt", "w") as dbase:
        for line in lines:
            if line.split(";")[0] == book_id:
                dbase.write(line.split(";")[0] + ";" + line.split(";")[1] + ";" + line.split(";")[2] + ";" + line.split(";")[3] + 
                            ";" + status + "\n")

            else: 
                dbase.write(line)


def authorReview(auth_token):
    """
    Functia genereaza autorul unui review in functie de 'auth_token', prin concatenarea 'first_name' cu 'last_name'.
    """
    lines = []
    with open("B_users.txt", 'r') as dbase:
        lines = dbase.readlines()

    for line in lines:
        if line.split(";")[2] == userEmail(auth_token):
            return line.split(";")[0] + " " + line.split(";")[1]
        
    return "User not found"


def validareRating(rating):
    """
    Functia valideaza un rating, acordat unei carti printr-un review, care trebuie sa fie intre 1 si 5.
    """
    if rating >= 1 or rating <=5:
        return True
    
    return False


def calculRating(book_id): 
    """
    Functia calculeaza ratingul total al unei carti ca medie aritmetica a ratingurilor individuale primite de cartea respectiva.
    """   
    lines = []
    with open("B_reviews.txt", 'r') as dbase:
        lines = dbase.readlines()

    sumaRating = 0
    countRating = 0
    for line in lines:
        if line.split(";")[0] == book_id:
            sumaRating += int(line.split(";")[1])
            countRating += 1

    if sumaRating > 0:
            return sumaRating/countRating
    else:
            return 0
    