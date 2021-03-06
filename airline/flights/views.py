from django.shortcuts import render , Http404 , HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.

from .models import Flight , Passengers

def index(request):
    flights = Flight.objects.all()
    context = {
        'flights': flights,
    }
    return render(request , 'flights/index.html' , context)

def flight(request , flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight Does not exist.")
    context = {
        'flight':flight,
        'passengers':flight.passenger.all(),
        'non_passengers':Passengers.objects.exclude(flights=flight).all()
    }

    return render(request ,'flights/flight.html' , context)

def book(request , flight_id):
    try:
        passenger_id = int(request.POST['passenger'])
        passenger = Passengers.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request , 'flights/error.html' , {'message' : 'No selection'})
    except Flight.DoesNotExist:
        return render(request , 'flights/error.html' , {'message' : 'Flight does not exist'})
    except Passenger.DoesNotExist:
        return render(request , 'flights/error.html' , {'message' : 'Passenger does not exist'})
    
    
    passenger.flights.add(flight)

    return HttpResponseRedirect(reverse("flight" , args=(flight_id,)))