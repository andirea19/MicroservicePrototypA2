# Architektur & Datenfluss - PetCare Hub

Dieses Dokument beschreibt die Zielarchitektur, die Kommunikationswege sowie die Datenflüsse der Microservices im Rahmen des akademischen Projekts.

## 1. Business-Prozesse
* **Haustier- & Allergie-Management:** Verwaltung von Haustieren (Hunde, Katzen) inklusive rassespezifischer Unverträglichkeiten (z. B. Rind, Getreide, Laktose).
* **Wunschlisten- & Geschenk-Management:** Führen von Wunschlisten pro Tier, damit Freunde und Familie Geschenke einsehen und als „gekauft“ markieren können.
* **Kalender- & Geburtstags-Tracking:** Überwachung anstehender Geburtstage und Altersberechnung.
* **Inspiration & Shop-Empfehlungen:** Bereitstellung von Zufallsbildern (über externe APIs) und passenden Produkt-/Shop-Empfehlungen basierend auf den Allergien.

## 2. Architekturdiagramm (Target Architecture)

Das folgende Diagramm zeigt die lose gekoppelte Microservice-Architektur mit dem Frontend als Aggregator:

```mermaid
graph TD
    User([Anwender / Browser]) -->|HTTP / Port 8000| Frontend[Frontend Service<br/>FastAPI + Jinja2]

    subgraph Docker Network (pet-network)
        Frontend -->|HTTPX REST / JSON| PetService[Pet-Service<br/>Haustiere, Allergien, Wunschlisten]
        Frontend -->|HTTPX REST / JSON| CalendarService[Calendar-Service<br/>Geburtstage & Termine]
        Frontend -->|HTTPX REST / JSON| APIService[Pet-API-Service<br/>Bilder & Shop-Empfehlungen]
    end

    APIService -->|External REST Call| ExternalAPI[Dog CEO API & The Cat API]
    PetService -->|Data Persistence| DB[(In-Memory / SQLite)]

    # Architektur & Datenfluss - PetCare Hub

## Datenflussdiagramm (Sequence Diagram)
Das folgende Sequenzdiagramm veranschaulicht den parallelen und fehlertoleranten Datenabruf beim Aufruf der Startseite:

