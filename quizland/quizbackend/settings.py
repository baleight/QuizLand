"""
Impostazioni del progetto Django per l'applicazione QuizApp.
"""

from pathlib import Path

# Definizione del percorso base del progetto.
# Questo percorso è utilizzato come riferimento per definire altre directory all'interno del progetto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Definizione del percorso per i template personalizzati.
# I template sono file HTML che definiscono la struttura delle pagine web.
TEMPLATES_DIRS = BASE_DIR / "templates"

# Chiave segreta per la sicurezza dell'applicazione.
# IMPORTANTE: in un ambiente di produzione, questa chiave deve essere mantenuta segreta e sicura.
SECRET_KEY = "django-insecure-xwp91dhxvuox#8v7-s60@i#p#7$o8nuq2&d1r@7+k^68j4ka9r"

# Modalità di debug.
# Quando DEBUG è impostato su True, Django mostra messaggi di errore dettagliati.
# Questa impostazione deve essere False in produzione per evitare di esporre dettagli sensibili.
DEBUG = True

# Host consentiti per accedere all'applicazione.
# In produzione, qui devono essere elencati i domini autorizzati.
ALLOWED_HOSTS = []

# Definizione delle applicazioni Django installate.
# Ogni applicazione rappresenta un modulo funzionale dell'intero progetto.
INSTALLED_APPS = [
    "django.contrib.admin",  # Amministrazione del progetto.
    "django.contrib.auth",  # Sistema di autenticazione e gestione degli utenti.
    "django.contrib.contenttypes",  # Gestione dei tipi di contenuto.
    "django.contrib.sessions",  # Gestione delle sessioni degli utenti.
    "django.contrib.messages",  # Sistema di messaggistica.
    "django.contrib.staticfiles",  # Gestione dei file statici (CSS, JS, immagini).
    "quizapp",  # Applicazione principale per la gestione dei quiz.
    "users",  # Applicazione per la gestione degli utenti e autenticazione.
]

# Middleware: componenti che gestiscono le richieste HTTP prima che arrivino alle view.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Aggiunge protezioni di sicurezza.
    "django.contrib.sessions.middleware.SessionMiddleware",  # Gestione delle sessioni utente.
    "django.middleware.common.CommonMiddleware",  # Gestione delle richieste generiche.
    "django.middleware.csrf.CsrfViewMiddleware",  # Protezione contro attacchi CSRF.
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Gestione dell'autenticazione.
    "django.contrib.messages.middleware.MessageMiddleware",  # Gestione dei messaggi flash.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Protezione contro attacchi clickjacking.
]

# File di configurazione delle URL.
# ROOT_URLCONF definisce il modulo principale per il routing delle URL.
ROOT_URLCONF = "quizbackend.urls"

# Configurazione dei template.
# I template vengono utilizzati per generare le pagine web dinamiche.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Backend per la gestione dei template.
        "DIRS": [TEMPLATES_DIRS],  # Directory personalizzata per i template.
        "APP_DIRS": True,  # Abilita la ricerca di template nelle app installate.
        "OPTIONS": {
            "context_processors": [  # Processori di contesto per arricchire i dati nei template.
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Configurazione dell'applicazione WSGI.
# Questo modulo è responsabile di gestire le richieste HTTP in produzione.
WSGI_APPLICATION = "quizbackend.wsgi.application"

# Configurazione del database.
# Per lo sviluppo, viene utilizzato SQLite, un database leggero e integrato.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Motore del database.
        "NAME": BASE_DIR / "db.sqlite3",  # Percorso del file di database.
    }
}

# Validatori delle password.
# Garantiscono che le password rispettino determinati requisiti di sicurezza.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},  # Lunghezza minima.
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},  # Controlla password comuni.
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},  # Evita password numeriche semplici.
]

# Impostazioni di internazionalizzazione.
# Queste configurazioni gestiscono lingua, fuso orario e formato dei dati.
LANGUAGE_CODE = "en-us"  # Lingua predefinita.
TIME_ZONE = "UTC"  # Fuso orario predefinito.
USE_I18N = True  # Abilita la traduzione del testo.
USE_TZ = True  # Abilita la gestione del fuso orario.

# Configurazione dei file statici.
# I file statici includono CSS, JavaScript e immagini.
STATIC_URL = "static/"  # URL pubblico per accedere ai file statici.
STATIC_ROOT = BASE_DIR / "staticfiles"  # Percorso per i file statici in produzione.
STATICFILES_DIRS = [BASE_DIR / "static"]  # Percorso per i file statici durante lo sviluppo.

# Impostazione del tipo di chiave primaria predefinita per i modelli.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configurazioni di autenticazione.
# URL di reindirizzamento dopo il login o logout.
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
