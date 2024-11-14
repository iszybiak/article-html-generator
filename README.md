# Article html generator

## Opis aplikacji
Aplikacja służy do przekształcania artykułów w formacie tekstowym do formatu HTML. 
Obejmuje kilka kluczowych kroków:

* Wczytanie artykułu z pliku – Aplikacja odczytuje treść artykułu z pliku tekstowego article.txt.
* Redagowanie i generowanie HTML – Za pomocą modelu GPT-4 artykuł jest redagowany, a następnie konwertowany do formatu HTML. Dodatkowo, w miejscach, w których warto umieścić obrazy, dodawane są tagi <'img src = "image_placeholder.jpg"'>. Każdy obrazek ma przypisany atrybut alt z odpowiednim promptem do wygenerowania obrazu.
* Czyszczenie Markdown – Po redakcji artykułu aplikacja je usuwa znaczniki składni Markdown, specyficzne dla ChatGPT.
* Zapis HTML do pliku –  Wygenerowany HTML jest zapisywany do pliku artykul.html.

## Funkcje
* read_article(file_path) – Funkcja do odczytu artykułu z pliku tekstowego.
* generate_html(article_text) – Funkcja, która wysyła artykuł do modelu OpenAI i generuje kod HTML.
* file_cleanup(text) – Funkcja, która oczyszcza artykuł z nadmiarowych elementów Markdown.
* save_html_to_file(content, output_file) – Funkcja zapisująca wygenerowany kod HTML do pliku.


## Instrukcje uruchomienia
Wymagania
Python – Wersja 3.8 lub wyższa.

Biblioteki:
* openai – do integracji z API OpenAI.
* torch – do użycia z biblioteką PyTorch w przypadku potrzeby pracy z modelami AI.
* logging – do logowania błędów.

Aby zainstalować niezbędne biblioteki, uruchom poniższą komendę:
```
pip install openai torch
```
Konfiguracja API OpenAI
1. Zarejestruj się na platformie OpenAI, jeśli jeszcze tego nie zrobiłeś, pod tym adresem: https://platform.openai.com.
2. Pobierz swój klucz API z sekcji API Keys.
3. Utwórz plik o nazwie API_KEY.txt w tym samym katalogu co skrypt i wklej swój klucz API do tego pliku. Plik powinien zawierać wyłącznie klucz API, np.:
```
sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
## Struktura repozytorium
W repozytorium znajdują się następujące pliki:
```
article-html-generator/
│
├── API_KEY.txt       # Plik zawierający Twój klucz API OpenAI.
├── article.txt       # Przykładowy plik z artykułem do przekształcenia (tekst).
├── szablon.html      # Szablon HTML strony, w który zostanie wstawiona zawartość artykułu.
├── main.py           # Główny skrypt aplikacji.
├── artykul.html      # Wygenerowany HTML z artykułu.
└── podglad.html      # Plik HTML z wstaionym już artykułuem do szablonu.
```

## Uruchomienie aplikacji
1. Zatąp artykuł, który chcesz przekształcić do formatu HTML, w pliku tekstowym o nazwie article.txt. 
2. Uruchom główny skrypt:
```
python main.py
```
3. Po uruchomieniu aplikacji, skrypt odczyta artykuł z pliku article.txt, przekształci go do formatu HTML, oczyszczając go z elementów Markdown, a następnie zapisze wynik do pliku artykul.html. Jeśli artykuł wymaga wstawienia obrazków, zostaną one oznaczone tagiem <'img src="image_placeholder.jpg"'> i będzie wygenerowany odpowiedni prompt w atrybucie alt.

## Obsługa błędów
Jeśli wystąpią jakiekolwiek błędy, aplikacja zaloguje je w konsoli i zapisze w logu. Możesz śledzić błędy za pomocą loggera w aplikacji.

## Przykładowe działanie
W pliku article.txt znajduje się przykładowy artykuł w formacie tekstowym.
Po uruchomieniu skryptu, artykuł został przekształcony do formatu HTML i zapisany w pliku artykul.html.
Zawartość pliku artykul.html została wstawiona do szablonu HTML (szablon.html), a wynik wstawienia znajduje się w podglad.html.
Możesz otworzyć plik podglad.html w przeglądarce, aby zobaczyć wynik końcowy. 

