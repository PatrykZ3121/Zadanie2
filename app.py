from flask import Flask, request, render_template
import datetime
import logging

# Konfiguracja loggera do rejestrowania informacji w konsoliiiii
logging.basicConfig(level=logging.INFO)

# Utworzenie loggera z nazwą aplikacji
logger = logging.getLogger("WeatherApp")
start_time = datetime.datetime.now()  # Pobranie aktualnego czasu uruchomienia aplikacji
logger.info(f"App started at: {start_time}")
logger.info("Author: Patryk Zygmunt")  # Informacja o autorze aplikacji

app = Flask(__name__)  # Inicjalizacja obiektu aplikacji Flask

# Definicja lokalizacji: kraje, miasta i ich pogoda
LOCATIONS = {
    "Poland": {"Warsaw": "Sunny", "Krakow": "Rainy"},
    "Germany": {"Berlin": "Cloudy", "Munich": "Snowy"},
    "France": {"Paris": "Windy", "Lyon": "Foggy"}
}

# Główna trasa aplikacji
@app.route('/', methods=['GET', 'POST'])
def home():
    # Lista dostępnych krajów
    countries = list(LOCATIONS.keys())
    selected_country = None  # Wybrany kraj przez użytkownika
    filtered_cities = []  # Lista miast dla wybranego kraju
    selected_city = None  # Wybrane miasto przez użytkownika
    weather = None  # Informacja o pogodzie dla wybranego miasta
    error = None  # Informacja o błędach, jeśli wystąpią

    if request.method == 'POST':  # Jeśli użytkownik przesłał formularz
        selected_country = request.form.get('country')  # Pobranie wybranego kraju z formularza
        selected_city = request.form.get('city')  # Pobranie wybranego miasta z formularza

        if selected_country:  # Jeśli wybrano kraj
            # Pobranie listy miast dla wybranego kraju
            filtered_cities = list(LOCATIONS.get(selected_country, {}).keys())

        if selected_country and selected_city:  # Jeśli wybrano zarówno kraj, jak i miasto
            # Pobranie pogody dla wybranego miasta
            weather = LOCATIONS.get(selected_country, {}).get(selected_city)
            if not weather:  # Jeśli nie znaleziono danych o pogodzie
                error = "Weather data for the selected city is not available."

    # Przekazanie danych do interfejsu
    return render_template(
        "index.html",
        countries=countries,
        selected_country=selected_country,
        filtered_cities=filtered_cities,
        selected_city=selected_city,
        weather=weather,
        error=error
    )

if __name__ == '__main__':
    PORT = 5000  # Port, na którym aplikacja będzie działać
    logger.info(f"App listening on port {PORT}")  # Logowanie informacji o porcie
    app.run(host='0.0.0.0', port=PORT)  # Uruchomienie aplikacji Flask