# Użycie nowszego obrazu Python 3.11
FROM python:3.11-slim AS builder

# Informacja o autorze obrazu
LABEL org.opencontainers.image.authors="Patryk Zygmunt"

# Aktualizacja repozytoriów i instalacja niezbędnych pakietów
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Ustawienie katalogu roboczego na /app
WORKDIR /app

# Kopiowanie pliku requirements.txt do katalogu roboczego
COPY requirements.txt .

# Instalacja najnowszych zależności Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Użycie nowszego obrazu Python 3.11
FROM python:3.11-slim

# Informacja o autorze obrazu
LABEL org.opencontainers.image.authors="Patryk Zygmunt"

# Instalacja curl dla healthcheck i aktualizacja systemu
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Ustawienie katalogu roboczego na /app
WORKDIR /app

# Kopiowanie zainstalowanych pakietów Python z etapu budowania
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Kopiowanie wszystkich plików projektu do katalogu roboczego
COPY . .

# Eksponowanie portu 5000, na którym działa aplikacja
EXPOSE 5000

# Konfiguracja healthcheck, sprawdzająca dostępność aplikacji co 30 sekund
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl -f http://localhost:5000/ || exit 1

# Domyślna komenda uruchamiająca aplikację
CMD ["python", "app.py"]
