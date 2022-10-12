# Aanpassingen t.o.v. versie ingediend d.d. 05-10-2022

Ik was in alle eerlijkheid verbaasd dat e.e.a. niet werkt. Bij het schrijven van de usage guide is door alle functies heengelopen via CLI opdrachten en alles liep goed. Maar de grote fout die ik heb begaan is dat ik daarna nog enkele in mijn ogen kleine aanpassingen doorvoerde (obj.get_method() in CLI_router teruggebracht van per class naar 1 aan het eind van de functie en een wijziging in determine_stock() met een beperking in tijd middels de stock_date) en enkel de commando's heb getest die er volgens mij door werden geraakt.
Er niet bij stilstaand dat door de nieuwe plaats van obj.get_method() in de CLI_router de functie blijft doorlopen na het gebruiken van een optional argument en het uitvoeren van de bijbehorende functie. Voorheen stond de obj.get_method() 1 indent verder per class en werd deze niet bereikt.
Het wijzigen van determine_stock() was getest met "report inventory", maar ik was vergeten dat "stock_date" daar als string wordt aangeboden en bij andere functies als date vanwege date.today() als default.
**Lesson learned**: altijd alles nog eens testen, omdat veronderstellingen wel eens fout kunnen zijn.

Ik zal hierna per .py bestand aangeven wat er is gewijzigd ten opzichte van de eerder ingediende versie.

### superpy
- Import eigen modules: "import as" weggehaald.
- Toelichting toegevoegd waarom de import van de CLI_router niet bovenin staat. Heeft te maken met de volgorde waarin een bestand word doorlopen: eerst worden de importen geactiveerd en doorlopen en daarna pas de functies in superpy zelf. Dat zorgde ervoor dat bij de allereerste aanroep (wanneer de csv en txt bestanden nog niet bestaan) in de geïmporteerde modules (1) een functie wordt aangeroepen dat een bestand probeert te lezen dat niet bestaat en (2) iets probeert te doen met niet bestaande inhoud. Door de import van CLI_router pas na de creatie van de files en opslaan van de systemtime op te nemen. Het kan opgelost worden door in "functions_system.read_time()" een "fail save" op te nemen dat "functions_system.save_time()" wordt aangeroepen wanneer het bestand nog niet bestaan, maar ik vind het niet netjes om op die manier de benodigde bestanden aan te maken.

### CLI_router
- Import eigen modules: "import as" weggehaald.
- Comments toegevoegd.
- "return" toegevoegd aan de acties van de optional arguments (in de code op lijn 33, 41 en 49) zodat de functie dan wordt geëindigd in plaats van door te gaan en te proberen een niet gemaakt classobject aan te roepen.

### CLI_parser
- Import eigen modules: "import as" weggehaald.
- Comments toegevoegd.

### classes
- Import eigen modules: "import as" weggehaald.
- Comments toegevoegd.
- In Report.inventory() en Report.inventory_per_product() om de stock_date te bepalen eerst de self.report_date omgezet van string naar datetime en vervolgens in determine_stock() er een date() van gemaakt.

### functions_stock
- Import eigen modules: "import as" weggehaald.
- In functie "determine_stock()" datetime.strptime en .date() toegevoegd bij obj_bought.buy_date en ojb_sold.sell_date zodat nu date wordt vergeleken met date.
- Comments toegevoegd.

### functions_system
- In functie save_time() de laatste 2 lijnen 1 indent naar voren gezet, zodat nu weer een "OK" wordt geprint wanneer optionals "advance-time" of "restore-time" worden gebruikt.
- Comments toegevoegd. 

### functions_validation
- Import eigen modules: "import as" weggehaald.
- Comments toegevoegd.