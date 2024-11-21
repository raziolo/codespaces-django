from django.http import JsonResponse
from django.shortcuts import render

from frontend.models import Venduto

# Create your views here.
'''
Pseudo-codice dell'algoritmo

# Step 1: Raccolta dei dati
vendite_anno_precedente = { # Esempio di vendite per mese
    "Gennaio": [1000, 1200, 1100, 1300],
    "Febbraio": [950, 1000, 1050, 1150],
    "Marzo": [1400, 1500, 1450, 1600],
    # Aggiungi gli altri mesi
}

ore_lavorative_giornaliere = 12  # Ore lavorative al giorno
personale_disponibile = 5  # Numero di dipendenti disponibili

# Step 2: Analisi delle vendite
def calcola_vendite_totali(mese):
    return sum(vendite_anno_precedente[mese])

# Step 3: Previsione del carico di lavoro (semplice esempio)
def stima_personale_necessario(vendite_totali, ore_lavorative, personale_disponibile):
    # Supponiamo che per ogni 1000 vendite siano necessari 2 dipendenti
    fattore_di_lavoro = vendite_totali / 1000
    personale_necessario = fattore_di_lavoro * 2
    # Limita il personale massimo disponibile
    return min(personale_necessario, personale_disponibile)

# Step 4: Pianificazione degli orari (distribuisci il personale per mese)
pianificazione_personale = {}

for mese, vendite in vendite_anno_precedente.items():
    vendite_totali = calcola_vendite_totali(mese)
    personale_necessario = stima_personale_necessario(vendite_totali, ore_lavorative_giornaliere, personale_disponibile)
    pianificazione_personale[mese] = personale_necessario

# Step 5: Risultati
for mese, personale in pianificazione_personale.items():
    print(f"A {mese}, sono necessari {personale:.1f} dipendenti.")


'''
from datetime import date, datetime, timedelta
from django.utils.dateparse import parse_date


base_response = {
    "response" : "",
    "color" : ""
}

def home(request):

    return render(request, 'frontend/homepage.html', context={})


def inserisci_venduto(request):
    today = date.today()

    if request.method == "GET":

        return render(request, 'frontend/inserisci_venduto.html', context={'today': today})
    elif request.method == "POST":

        data = request.POST.get('date')
        request_venduto = request.POST.get('venduto')

        try:
            request_venduto = int(request_venduto)
        except Exception as e:
            print(f"Error: {e}")

        if Venduto.objects.filter(data=data).exists():
            print("already exists")
            response = make_response("Venduto già inserito", "red")
            return render(request, 'frontend/base_response.html', context={'response' : response})

        V= Venduto.objects.create(data=data, valore=request_venduto)
        V.save()
        response = make_response("Venduto inserito correttamente", "green")
        return render(request, 'frontend/base_response.html', context={'response' : response})

    return None


def make_response(response_text, color):
    response = base_response.copy()
    response['response_text'] = response_text
    response['color'] = color
    return response

def storico_venduto(request):
    date_filter = request.GET.get('date-filter', None)
    venduti = Venduto.objects.all().order_by('-data')

    if not date_filter:
        venduti = Venduto.objects.all().order_by('-data')
    else:
        try:
            filter_date = parse_date(date_filter)  # Parse the date from the GET parameter
            if filter_date:
                venduti = venduti.filter(data=filter_date)
        except ValueError:
            pass  # Ignore invalid dates

    return render(request, 'frontend/storico_venduto.html', context={"venduti" : venduti})

def testdata():
    import random

    for _ in range(1, 31):
        data = date(2024, 9, _)
        valore = random.randint(1, 1000)
        V = Venduto.objects.create(data=data, valore=valore)
        V.save()

def grafico_venduto(request):
    if request.method == "GET":
        try:
            mese = request.GET.get('mese', None)
        except Exception as e:
            print(e)
        if mese:
            return render(request, template_name="frontend/grafico_venduto.html")
        if not mese:
            mese = datetime.now().month
            return render(request, template_name="frontend/grafico_venduto.html")





def get_venduto(request):
    if request.method == "GET":
        try:
            mese = request.GET.get('mese', None)
            mese = int(mese)
        except Exception as e:
            print(e)
        if mese:
            print(mese)
            venduti = Venduto.objects.filter(data__month=mese)
            data_dict = {venduto.data.strftime("%d-%m-%Y"): venduto.valore for venduto in venduti}
            print(data_dict)
            venduti = Venduto.objects.all()
            # Modifica il formato della risposta per includere la chiave "data"
            return JsonResponse({"data": data_dict})
        if not mese:
            venduti = Venduto.objects.filter(data__month=datetime.now().month)
            data_dict = {venduto.data.strftime("%d-%m-%Y"): venduto.valore for venduto in venduti}
            return JsonResponse({"data": data_dict})
