
import openai
import os
import socket
import speech_recognition as sr
import json
import requests

from dotenv import load_dotenv
 
load_dotenv()

CURRENT_DAY_MONTH_BEGIN_AS_STRING = "01052023"
TODAY_AS_STRING = "22052023"
USER_SESSION_ID = os.environ.get("USER_SESSION_ID")

print(f"OpenAI API Key: {os.environ.get('OPENAI_API_KEY')}")
print(f"User Session ID: {USER_SESSION_ID}")

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9000
VOICE_PORT = 9001
FILENAME = "output.wav"
API_URL = f"https://www.enel.it/bin/areaclienti/auth/aggregateConsumption?pod=IT001E68430672&userNumber=104389955&validityFrom={CURRENT_DAY_MONTH_BEGIN_AS_STRING}&validityTo={TODAY_AS_STRING}"

def month_to_string(month):
    if month == "01":
        return "Gennaio"
    elif month == "02":
        return "Febbraio"
    elif month == "03":
        return "Marzo"
    elif month == "04":
        return "Aprile"
    elif month == "05":
        return "Maggio"
    elif month == "06":
        return "Giugno"
    elif month == "07":
        return "Luglio"
    elif month == "08":
        return "Agosto"
    elif month == "09":
        return "Settembre"
    elif month == "10":
        return "Ottobre"
    elif month == "11":
        return "Novembre"
    elif month == "12":
        return "Dicembre"

def stt():
    # Initialize recognizer
    r = sr.Recognizer()
    r.pause_threshold = 1
    # Record audio
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source, 0.5)
        audio = r.listen(source, phrase_time_limit=5,
                         snowboy_configuration=None)
    # Save audio to file
    with open(FILENAME, "wb") as f:
        f.write(audio.get_wav_data())

    audio_file = open(FILENAME, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]


def main():
    json_data = None

    req = requests.get(API_URL, headers={"cookie": f"USERSESSIONID={USER_SESSION_ID}"})
    json_data = req.json()

    max_consumption = 0
    max_consumption_day = 0
    max_consumption_month = 0
    max_consumption_hour = 0

    for x in range(0, len(json_data["data"]["aggregationResult"]["aggregations"][1]["results"])):
        if json_data["data"]["aggregationResult"]["aggregations"][1]["results"][x]["binValues"][0]["value"] > max_consumption:
            max_consumption = json_data["data"]["aggregationResult"]["aggregations"][1]["results"][x]["binValues"][0]["value"]
            max_consumption_day = x
            max_consumption_month = json_data["data"]["aggregationResult"]["aggregations"][1]["results"][x]["date"][2]+json_data["data"]["aggregationResult"]["aggregations"][1]["results"][x]["date"][3]
            
            for y in range(0, 24):
                if json_data["data"]["aggregationResult"]["aggregations"][0]["results"][x]["binValues"][y]["value"] > max_consumption_hour:
                    max_consumption_hour = y
            
    print(f"Max consumption: {max_consumption} kWh on day {max_consumption_day} of month {month_to_string((max_consumption_month))} on hour {max_consumption_hour}.")
    
    API_KEY = os.environ.get("OPENAI_API_KEY")
    openai.api_key = API_KEY

    '''
    v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    v.bind((HOST, VOICE_PORT))
    v.listen()

    print(f"Listening for Voice on {HOST}:{VOICE_PORT}...")

    connv, addrv = v.accept()
    message = connv.recv(1024)
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    print(f"Listening for NAO on {HOST}:{PORT}...")

    conn, addr = s.accept()
    message = conn.recv(1024)

    print("Received " + message.decode("utf-8"))
    conn.send("Dimmi qualcosa!".encode("utf-8"))

    messages = []
    messages.append(
        {
            "role": "system",
            "content": f"\
                Sei un assistente che aiuta le persone a consumare meno energia. Ti chiami NAO. Parli solo Italiano. \
                L'utente, generalmente, lavora dal lunedì a venerdì dalle 8 alle 17 e torna a casa per le 18. Al ritorno gioca al PC oppure guarda la TV fino alle 19.30 circa. \
                Fa la lavatrice il venerdì di ogni settimana. Dati i consumi di un determinato giorno, fornisci all'utente opinioni e consigli su come consumare energia elettrica responsabilmente. \
                Chiedi a lui cosa ha fatto durante la giornata e rispondi con un consiglio. \
                L'utente ha avuto il suo massimo consumo il giorno {max_consumption_day} del mese di {month_to_string(max_consumption_month)} con un consumo di {max_consumption} kilowatt all'ora {max_consumption_hour}. \
                L'orario di massimo consumo è alle 18.00. \
                Se ti rendi conto di non avere nulla di utile da dire durante la conversazione, utilizza questi dati per formulare dei suggerimenti. \
                Nel testo prodotto, non utilizzare segni di punteggiatura, a meno che non siano necessari per la sintassi. \
                Se ricevi un messaggio contenuto in parentesi quadre, significa che ti sono stati inviati dati utili al miglioramento della risposta. \
            "
        },
    )
    '''
    messages.append(
        {
            "role": "user",
            "content": "\
                Sei un assistente che aiuta le persone a consumare meno energia. \
                L'utente lavora dal lunedì a venerdì dalle 8 alle 17 e torna a casa per le 18. Al ritorno gioca al PC oppure guarda la TV fino alle 19.30 circa. \
                Fa la lavatrice il venerdì di ogni settimana. Dati i consumi di un determinato giorno, fornisci all'utente opinioni e consigli su come consumare energia elettrica responsabilmente.
            "
        },
    )
    '''
    with conn:
        print(f"Connected to {addr[0]}:{addr[1]}")

        i = 0
        j = 3
        
        while True:
            message = conn.recv(1024).decode("utf-8")

            if message == "listen now":
                data = stt()
                print(data)

                if not data:
                    pass
                else:
                    i = i + 1

                    messages.append(
                        {
                            "role": "user",
                            "content": data
                        }
                    )
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )

                    openai_response = response["choices"][0]["message"]["content"]
                    print(f"\n{openai_response}\n")
                    if i == j:
                        messages.pop(1)
                        i = 0

                    conn.send(openai_response.encode("utf-8"))


if __name__ == "__main__":
    main()
