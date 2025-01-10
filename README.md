# **QuizLand- Django Quiz Application**

QuizLand è un'applicazione web basata su Django che offre una piattaforma interattiva per la creazione, la gestione e la partecipazione a quiz su vari argomenti. Progettata con un'interfaccia user-friendly e funzionalità avanzate, QuizLandè perfetta per studenti, insegnanti e amministratori.

## **Caratteristiche principali**

### **Utenti Registrati**

- **Partecipazione ai quiz**:
  Gli utenti registrati possono partecipare a quiz su diversi argomenti, rispondendo a domande a scelta multipla.

- **Visualizzazione risultati**:
  Alla fine del quiz, gli utenti possono visualizzare un riepilogo dettagliato con il punteggio, le risposte corrette, errate e quelle non tentate.

- **Sistema di autenticazione**:
  Gli utenti possono registrarsi, accedere e disconnettersi in modo sicuro. Le password sono protette tramite hashing.

### **Amministratori**

- **Gestione dei quiz**:
  Gli amministratori possono aggiungere, aggiornare ed eliminare quiz.
- **Gestione delle domande**:
  Possono aggiungere, modificare o rimuovere domande associate a ciascun quiz.
- **Pannello di amministrazione Django**:
  Accesso a funzionalità avanzate per la gestione di utenti, quiz e dati attraverso il pannello admin predefinito di Django..

------

## **Prerequisiti**

Dopo aver scaricato lo zip o clonato il progetto, segui questi passaggi.

### **Installazione di base**

1. **Installare pip**:
   - **Linux**: `python3 -m pip install --user --upgrade pip`
   - **Windows**: `pip install --upgrade pip`
2. **Installare Virtualenv**(consiglio):
   - **Linux**: `python3 -m pip install --user virtualenv`
   - **Windows**: `pip install --user virtualenv`
3. **Creare un ambiente virtuale**:
   - **Linux**: `python3 -m venv venv`
   - **Windows**: `py -m venv env`
4. **Attivare l'ambiente virtuale**:
   - **Linux**: `source venv/bin/activate`
   - **Windows**: `.\venv\Scripts\activate`
5. **Installare le dipendenze**:
   - **Linux**: `python3 -m pip install -r requirements.txt`
   - **Windows**: `pip install -r requirements.txt`

## **Setup dell'applicazione**

1. **Applica le migrazioni**

   ```bash
   cd smartquiz
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
   Accedi con le credenziali del superuser creato in precedenza.

------

## **Istruzioni di utilizzo**

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

*(Inserisci screenshot delle pagine più significative, ad esempio: pagina del quiz, pagina dei risultati, gestione quiz da admin.)*
