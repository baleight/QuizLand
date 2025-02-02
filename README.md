# **QuizLand - Django Quiz Application**

QuizLand è un'applicazione web basata su Django che offre una piattaforma interattiva per la creazione, gestione e partecipazione ai quiz. Grazie a un'interfaccia user-friendly e funzionalità avanzate, è ideale per studenti, insegnanti e amministratori.

## **Caratteristiche principali**

### **Utenti Registrati**

- **Partecipazione ai quiz**: Gli utenti registrati possono rispondere a quiz su diversi argomenti.
- **Visualizzazione risultati**: Al termine del quiz, è disponibile un riepilogo dettagliato con punteggio, risposte corrette ed errate.
- **Sistema di autenticazione**: Registrazione, login e logout sicuri con protezione delle password tramite hashing.
- **Dashboard personale** *(in sviluppo)*: Mostrerà i risultati passati, quiz completati e statistiche di performance.

### **Amministratori**

- **Gestione dei quiz**: Creazione, modifica ed eliminazione di quiz.
- **Gestione delle domande**: Possibilità di aggiungere, modificare o rimuovere domande.
- **Pannello di amministrazione Django**: Accesso avanzato per la gestione di utenti, quiz e dati.

## **Feature aggiuntive (future)**

- **Quiz personalizzati**: Creazione e condivisione di quiz personalizzati tra utenti.
- **Sistema di raccomandazione**: Suggerimenti basati sui risultati e interessi degli utenti.
- **Statistiche avanzate**: Dashboard con dati dettagliati sulle performance.
- **Supporto multilingua**: Localizzazione in più lingue.

## **Prerequisiti**

Dopo aver scaricato o clonato il progetto, segui questi passaggi:

### **Installazione di base**

1. **Installare pip**:
   - **Linux**: `python3 -m pip install --user --upgrade pip`
   - **Windows**: `py -m pip install --upgrade pip`
2. **Installare Virtualenv**:
   - **Linux**: `python3 -m pip install --user virtualenv`
   - **Windows**: `pip install --user virtualenv`
3. **Creare un ambiente virtuale**:
   - **Linux**: `python3 -m venv venv`
   - **Windows**: `py -m venv env`
4. **Attivare l'ambiente virtuale**:
   - **Linux**: `source venv/bin/activate`
   - **Windows**: `.env\Scripts\activate`
5. **Installare le dipendenze**:
   - **Linux**: `python3 -m pip install -r requirements.txt`
   - **Windows**: `pip install -r requirements.txt`

## **Setup dell'applicazione**

1. **Applica le migrazioni**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

   Questo comando crea il database SQLite e tutte le tabelle necessarie.

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

4. **Accedi al pannello amministrativo** http://127.0.0.1:8000/admin/

5. **Caricare dati demo** *(opzionale)*:

   ```bash
   rm db.sqlite3  # Rimuove il database (se esiste)
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py shell
   >>> from setup_demo import setup_demo_data
   >>> setup_demo_data()
   ```

   Credenziali demo: **teacher1** e **student1** (password: `nome_utente+'password'`)

## **Utilizzo**

### **Registrazione e Login**

Gli utenti possono registrarsi e accedere alla piattaforma con un nome utente, email e password.

### **Partecipazione al Quiz**

Dopo il login, possono selezionare un quiz, rispondere alle domande e visualizzare i risultati.

### **Gestione per Amministratori**

Gli amministratori possono creare, modificare ed eliminare quiz e domande.

## **Tecnologie Utilizzate**

- **Backend**: Django
- **Database**: SQLite (predefinito)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Librerie principali**: Django Auth, Bootstrap

------

## **Screenshot**

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
