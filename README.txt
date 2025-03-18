Technologies used: Python, Python Flask, Postman, VS Code
Description: Developing a REST API application to easily manage both the books in a library and its users, and the interaction between users and the library.
The functionalities that the library has are performed by users with Admin or Simple User roles, who, depending on permissions, can add or remove books, view books, view transactions and their history, borrow books, extend the term of a borrowed book or return borrowed books. Users can also receive penalties for exceeding the return deadline. The application also allows adding reviews and ratings for books.

Fisiere .txt:
B_users.txt: first_name;last_name;email;password;type(1-admin, 0-simple user)
B_tokens: email;password;auth_token
B_books.txt: book_id;book_name;book_author;book_description;book_status(imprumutata/disponibila/blocata)
B_tranzactii.txt: transaction_id;email;book_id;borrow_date;borrow_time;transaction_status(in desfasurare/incheiata/in intarziere);number_extensions(este 0 la generarea unei tranzactii noi)
B_reviews.txt: book_id;rating(1-5);review;author(first_name + last_name)
B_returnReq.txt: return_id;transaction_id;email;status_request(1-activa/0-incheiata)
B_abateri: email;data_abatere;numar_abateri (0/1/2/3/4)
B_logs.txt: log_id;log_date;log_task;alte informatii in functie de operatia rulata in aplicatie


1. Inregistrare si autentificare

1.1. POST /register 
Cu datele primite pentru un utilizator nou, am verificat daca acest utilizator este deja inregistrat in Bibliotech. Am facut o validare a datelor, lungimea first_name sa fie >= 5 si lungimea password sa fie >= 7. Apoi utilizatorul validat a fost inregistrat in B_users.txt.

1.2. POST /login 
Am facut o validare a datelor primite (email si password) si am generat un auth_token dupa un pattern stabilit de mine:
auth_token = str(randrange(11,90)+7) + email[0:3] + str(randrange(311,600)) + password[0:4].
Auth_token l-am scris in fisierul B_tokens.txt. In acest fisier inregistrez toate auth_token generate, impreuna cu email si password. 
La autentificarea utilizatorilor in metodele aplicatiei verific existenta token-ului respectiv in fisierul B_tokens.txt si returnez tipul utilizatorului din fisierul B_users.txt. La un login urmator adaug noul auth_token in fisierul B_tokens.txt si pentru autentificare il caut in acest fisier.


2. Gestionarea cartilor 

2.1. POST /book 
Validarea utilizatorului dupa auth_token si rol de Admin, apoi am verificat existenta cartii in biblioteca, dupa book_name si book_author.
Daca trece de toate validarile, cartea este inregistrata in B_books.txt, aici adaug si un identificator unic al cartii book_id si book_status 'disponibila'.

2.2. POST /books 
Dupa validarea utilizatorului cu rol de Admin, am verificat daca exista cartile in biblioteca, dupa book_name si book_author, si daca nu, le-am adaugat in B_books.txt. 
Apoi am generat raspunsul cu cartile inregistrate. 


2.3. GET /book 
Am validat utilizatorul, ca Admin sau Simple user sau None - daca utilizatorul nu este trimis.
Am identificat cartea dupa book_id, apoi am extras datele de raspuns pentru obiectul JSON din fisierul B_books.txt si din fisierul B_reviews.txt. 
Pentru campul reviews am creat o lista de dictionare din fisierul B_reviews.txt. 
Pentru calcularea ratingului total am calculat media ratingurilor acordate de utilizatori pentru cartea respectiva (dupa book_id), cu o functie in UtilsBooks.py.
In cazul in care auth_token este 'null' nu am afisat si autorul fiecarui review.
Daca nu a fost identificata cartea am returnat un mesaj si codul 404.

2.4. GET /books 
Pentru generarea raspunsului am folosit date din B_books si functia de calcul pentru ratingul pe fiecare carte. Am creat o lista de dictionare, iar daca in biblioteca nu exista nicio carte, am returnat un mesaj cu status code 404.


3. Interactiunea cu Bibliotech 

3.1. POST /transaction 
Metoda adauga o tranzactie in fisierul B_tranzactii.txt. Am facut validari pentru user, book_id, book_status (sa fie 'disponibila') si numar de tranzactii pe utilizator (sa fie <5). Daca validarile au fost ok, am generat un numar unic de tranzactie, apoi tranzactia am adaugat-o in B_tranzactii.txt (cu status 'in desfasurare'), iar statusul cartii in B_books.txt l-am modificat in 'imprumutata'.
Pentru fiecare conditie de validare, daca nu a fost indeplinita am returnat un raspuns cu campul 'error'.

3.2. GET /transaction
Am facut validare pe user, care poate fi atat Admin cat si Simple User (intrucat nu se specifica in cerinta, am considerat ca si un utilizator cu rol de Admin poate imprumuta carti de la biblioteca), apoi am validat existenta numarului tranzactiei trimis ca parametru. Am facut si o validare a numarului tranzactiei cu utilizatorul, intrucat am considerat ca un utilizator are acces doar la propriile sale tranzactii.
Pentru raspuns am folosit date din B_tranzactii.txt, iar remaining_time l-am calculat printr-o functie folosind data imprumutului, durata imprumutului si data curenta. Pentru durata imprumutului am folosit durata la momentul calculului (inclusiv extinderile daca au existat).

3.3. GET /transactions
Am validat utilizatorul Simple user si am generat o lista cu tranzactiile lui folosind informatii din B_tranzactii.txt si B_books.txt. Apoi am validat utilizatorul Admin si am generat raspunsul cu toate trnazactiile din Bibliotech, folosind aceleasi fisiere pentru date. Am returnat un raspuns de eroare daca nu exista nicio tranzactie in biblioteca.

3.4. POST /extend
Am validat utilizatorul (Admin sau Simple user), numarul tranzactiei, statusul tranzactiei (sa fie 'in desfasurare' sau 'in intarziere') si timpul de extindere primit ca parametru sa fie intre 1 si 5. Apoi am verificat numarul de extinderi deja inregistrate pe utilizator, iar daca sunt <2, am adaugat o extindere in B_tranzactii.txt si am transmis raspuns cu numarul de zile de extindere (cel solicitat de utilizator). Daca numarul de extinderi este >=2 am returnat mesaj de eroare. Pentru fiecare conditie nevalidata, am returnat un mesaj corespunzator.

3.5. POST /return
Am facut validare pe utilizator, numarul tranzactiei si de asemenea am verificat ca utilizatorul tranzactiei sa fie acelasi cu utilizatorul identificat prin auth_token, pentru a nu permite unui utilizator sa solicite o cerere de returnare pentru o tranzactie a altui utilizator. Apoi am verificat ca statusul tranzactiei sa fie 'in desfasurare' sau 'in intarziere', pentru a nu permite cererea unui retur pe o tranzactie deja incheiata.
Daca numarul de zile pana la data de returnare este <0 (adica a fost depasit termenul de returnare), am modificat statusul tranzactiei in 'in intarziere', si daca utilizatorul nu are nicio abatere, am creat cererea de returnare in B_returnReq.txt, am creat prima abatere pentru utilizator in B_abateri.txt si am returnat raspuns cu 'succes' si mesaj privind tipul de abatere. Aici amfacut si o verificare a numarului de zile de la prima abatere pana la zi si daca este mai mare decat 30, am decrementat numarul de abateri.
Apoi pentru cazurile in care numarul de abateri ale utilizatorului este 1, 2 sau 3, am creat cererea de returnare si am incrementat numarul de abateri, si am trimis raspuns cu 'succes' si mesaj privind tipul de abatere.
Daca numarul de zile pana la data de returnare este >0, am creat cererea de returnare, fara nicio abatere.

3.6. GET /returns
Am validat utilizatorul cu rol de Admin si am generat o lista cu cererile de returnare active (status_request = 1) folosind date din B_returnReq.txt. Daca nu exista nicio cerere de returnare am returnat un mesaj adecvat.

3.7. POST /return/end
Am validat utilizatorul cu rol de Admin si statusul cererii de returnare sa fie 1 - activa.
Daca validarile au fost ok, am modificat statusul cererii de returnare in 0 - incheiata, statusul tranzactiei in 'incheiata' si statusul cartii in 'disponibila'.


3.8. POST /review
Am validat utilizatorul care vrea sa adauge un review, apoi am validat id-ul cartii si ratingul (sa fie intre 1 si 5). Daca validarile sunt ok, am adaugat review-ul in fisier si am trimis raspuns cu campul 'success'si codul 200.
In cazul in care cartea nu a fost gasita sau ratingul nu corespunde, se intoarce raspuns cu codul 404, iar daca user-ul nu a fost validat se intoarce raspuns cu codul 403.
Pentru autorul review-ului am folosit first_name si last_name ale utilizatorului.


*In metodele in care nu se specifica ca se aplica unui singur tip de utilizator, am considerat atat Admin cat si Simple User, adica am considerat ca si Admin poate efectua tranzactii ca un Simple User.

5. Pentru pastrarea datelor intre rulari consecutive am facut un fisier de loguri B_logs.txt in care sa inregistrez toate operatiile pe care le fac in aplicatie, cu un numar unic de identificare si data operatiei: inregistrarile de utilizatori, logarile in aplicatie, adaugarea cartilor, solicitarea informatiilor despre o carte sau toate cartile, crearea unei cereri de imprumut, solicitarea informatiilor despre o tranzactie sau toate tranzactiile, inregistrarea unei extinderi, inregistrarea unei cereri de returnare sau a tuturor cererilor de returnare, incheierea unei cereri de returnare si inregistrarea unei recenzii. 
Am dezvoltat acest punct doar pentru punctele 1.1. si 1.2.


