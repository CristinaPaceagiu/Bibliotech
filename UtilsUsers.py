from random import randrange


def checkCredentials(email, password):
    """
    Functia verifica daca un utilizator este inregistrat pentru a primi permisiunea de login.
    """
    lines = []
    with open("B_users.txt", 'r') as dbase:
        lines = dbase.readlines()

    for line in lines:
        if line.split(";")[2] == email and line.split(";")[3] == password:    
            return True
                
    return False


def createAuthToken(email, password):
    """
    Functia genereaza un auth_token dupa un pattern stabilit, pentru login.
    """
    auth_token = str(randrange(11,90)+7) + email[0:3] + str(randrange(311,600)) + password[0:4]
    with open("B_tokens.txt", 'a') as dbase:
        dbase.write(email + ";" + password + ";" + auth_token + "\n")

    return auth_token


def userEmail(auth_token):
    """
    Functia returneaza email-ul utilizatorului in functie de auth_token primit la login.
    """
    lines = []
    with open("B_tokens.txt", 'r') as dbase:
        lines = dbase.readlines()

    for line in lines:
        if line.split(";")[2].strip() == auth_token:            
            return line.split(";")[0]
    
    return None


def autentificareUser(auth_token):
    """
    Functia identifica un utilizator dupa auth_token si returneaza tipul acestuia 1-Admin, 0-Simple User.
    """    
    lines = []
    with open("B_users.txt", 'r') as dbase:
        lines = dbase.readlines()

    for line in lines:
        if line.split(";")[2] == userEmail(auth_token):
            return line.split(";")[4].strip()

    return None  


