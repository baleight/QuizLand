<<<<<<< HEAD
> # **QuizLand- Django Quiz Application**
>
=======
# **QuizLand- Django Quiz Application**
>>>>>>> 03931fc3a4d03c4f81848b0abcf9c6350b30398c

QuizLand è un'applicazione web basata su Django che offre una piattaforma interattiva per la creazione, la gestione e la partecipazione a quiz su vari argomenti. Progettata con un'interfaccia user-friendly e funzionalità avanzate, QuizLandè perfetta per studenti, insegnanti e amministratori.

## **Caratteristiche principali**

### **Utenti Registrati**

- **Partecipazione ai quiz**:
<<<<<<< HEAD
   Gli utenti registrati possono partecipare a quiz su diversi argomenti, rispondendo a domande a scelta multipla.

- **Visualizzazione risultati**:
   Alla fine del quiz, gli utenti possono visualizzare un riepilogo dettagliato con il punteggio, le risposte corrette, errate e quelle non tentate.

- **Sistema di autenticazione**:
   Gli utenti possono registrarsi, accedere e disconnettersi in modo sicuro. Le password sono protette tramite hashing.

- Dashboard personale

  (feature futura)

  - Gli utenti potranno vedere i propri risultati passati, quiz completati e performance aggregate.
=======
  Gli utenti registrati possono partecipare a quiz su diversi argomenti, rispondendo a domande a scelta multipla.

- **Visualizzazione risultati**:
  Alla fine del quiz, gli utenti possono visualizzare un riepilogo dettagliato con il punteggio, le risposte corrette, errate e quelle non tentate.

- **Sistema di autenticazione**:
  Gli utenti possono registrarsi, accedere e disconnettersi in modo sicuro. Le password sono protette tramite hashing.
>>>>>>> 03931fc3a4d03c4f81848b0abcf9c6350b30398c

### **Amministratori**

- **Gestione dei quiz**:
<<<<<<< HEAD
   Gli amministratori possono aggiungere, aggiornare ed eliminare quiz.
- **Gestione delle domande**:
   Possono aggiungere, modificare o rimuovere domande associate a ciascun quiz.
- **Pannello di amministrazione Django**:
   Accesso a funzionalità avanzate per la gestione di utenti, quiz e dati attraverso il pannello admin predefinito di Django.

------

## **Feature aggiuntive (future)**

1. **Quiz personalizzati**:
    Gli utenti potranno creare quiz personalizzati e condividerli con altri utenti.
2. **Sistema di raccomandazione**:
    Suggerimenti di quiz basati sui risultati e sugli interessi degli utenti.
3. **Statistiche avanzate**:
    Dashboard per amministratori con dati dettagliati sulle performance degli utenti.
4. **Supporto multilingua**:
    Localizzazione dell'applicazione in più lingue.
=======
  Gli amministratori possono aggiungere, aggiornare ed eliminare quiz.
- **Gestione delle domande**:
  Possono aggiungere, modificare o rimuovere domande associate a ciascun quiz.
- **Pannello di amministrazione Django**:
  Accesso a funzionalità avanzate per la gestione di utenti, quiz e dati attraverso il pannello admin predefinito di Django..
>>>>>>> 03931fc3a4d03c4f81848b0abcf9c6350b30398c

------

## **Prerequisiti**

<<<<<<< HEAD
=======
Dopo aver scaricato lo zip o clonato il progetto, segui questi passaggi.

>>>>>>> 03931fc3a4d03c4f81848b0abcf9c6350b30398c
### **Installazione di base**

1. **Installare pip**:
   - **Linux**: `python3 -m pip install --user --upgrade pip`
<<<<<<< HEAD
   - **Windows**: `py -m pip install --upgrade pip`
2. **Installare Virtualenv**:
   - **Linux**: `python3 -m pip install --user virtualenv`
   - **Windows**: `py -m pip install --user virtualenv`
=======
   - **Windows**: `pip install --upgrade pip`
2. **Installare Virtualenv**(consiglio):
   - **Linux**: `python3 -m pip install --user virtualenv`
   - **Windows**: `pip install --user virtualenv`
>>>>>>> 03931fc3a4d03c4f81848b0abcf9c6350b30398c
3. **Creare un ambiente virtuale**:
   - **Linux**: `python3 -m venv venv`
   - **Windows**: `py -m venv env`
4. **Attivare l'ambiente virtuale**:
   - **Linux**: `source venv/bin/activate`
   - **Windows**: `.\venv\Scripts\activate`
<<<<<<< HEAD
5. **Installare le dipendenze**(`cd quizland`):
   - **Linux**: `python3 -m pip install -r requirements.txt`
   - **Windows**: `pip install -r requirements.txt`

------

=======
5. **Installare le dipendenze**:
   - **Linux**: `python3 -m pip install -r requirements.txt`
   - **Windows**: `pip install -r requirements.txt`

>>>>>>> 03931fc3a4d03c4f81848b0abcf9c6350b30398c
## **Setup dell'applicazione**

1. **Applica le migrazioni**

   ```bash
<<<<<<< HEAD
=======
   cd smartquiz
>>>>>>> 03931fc3a4d03c4f81848b0abcf9c6350b30398c
   python manage.py migrate
   ```

   Questo comando crea il database SQLite predefinito e tutte le tabelle necessarie.

2. **Crea un superuser**

   ```bash
   python manage.py createsuperuser
   ```

   Inserisci username, email e password per l'accesso amministrativo.

3. **Avvia il server di sviluppo**

   ```bash
   python manage.py runserver
   ```

   Accedi all'applicazione all'indirizzo: http://127.0.0.1:8000/

4. **Accedi al pannello amministrativo** Vai su: http://127.0.0.1:8000/admin/
<<<<<<< HEAD
    Accedi con le credenziali del superuser creato in precedenza.

5. Se hai bisogno gia' di un progetto funzionante, settiamo un template con utente e quiz gia' creati da me nel file setup_demo.py

    ```shell
    rm db.sqlite3 #cancelliamo le tabelle del database
    python manage.py makemigrations #assicuriamo di avere le migrazioni necessarie
    python manage.py migrate #applichiamo le migrazioni
    python manage.py createsuperuser #creiamo un admin user
    python manage.py shell
    >>> from setup_demo import setup_demo_data
    >>> setup_demo_data()
    ```
    
    Login: **teacher1** e **student1**, la password e': `nome_utente+'password'`

------

## **Utilizzo**
=======
   Accedi con le credenziali del superuser creato in precedenza.

------

## **Istruzioni di utilizzo**
>>>>>>> 03931fc3a4d03c4f81848b0abcf9c6350b30398c

### **Registrazione e Login**

- Gli utenti possono registrarsi con un nome utente, email e password.
- Una volta registrati, possono accedere e iniziare a partecipare ai quiz.

### **Partecipazione al Quiz**

- Dopo il login, gli utenti possono:
  - Selezionare un quiz da un elenco.
  - Rispondere alle domande a scelta multipla.
  - Inviare le risposte e visualizzare i risultati.

### **Gestione per Amministratori**

- Gli amministratori possono:
  - Aggiungere nuovi quiz e domande.
  - Modificare quiz e domande esistenti.
  - Eliminare quiz e domande non più necessari.

------

## **Tecnologie Utilizzate**

- **Backend**: Django
- **Database**: SQLite (configurazione predefinita)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Librerie principali**: Django Auth, Bootstrap

---

## **Screenshot**

<<<<<<< HEAD
### Lato Professore:

![image-20250202002747826](img\image-20250202002747826.png)

---

![image-20250202003457381](img\image-20250202003949589.png)

---

![image-20250202003627114](img\image-20250202003627114.png)

![image-20250202003608179](img\image-20250202003608179.png)

### Lato studente:![image-20250202022733585](img\image-20250202022733585.png)

---

![image-20250202004232508](img\image-20250202004232508.png)

---

![image-20250202022853069](img\image-20250202022853069.png)
=======
*(Inserisci screenshot delle pagine più significative, ad esempio: pagina del quiz, pagina dei risultati, gestione quiz da admin.)*
>>>>>>> 03931fc3a4d03c4f81848b0abcf9c6350b30398c
