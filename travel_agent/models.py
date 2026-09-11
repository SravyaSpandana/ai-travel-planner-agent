from pydantic import BaseModel
from typing import List


class Flight(BaseModel):
    origin: str
    destination: str
    airline: str
    price: float
    departure: str
    arrival: str


class Hotel(BaseModel):
    city: str
    name: str
    rating: float
    price_per_night: float


class WeatherDay(BaseModel):
    date: str
    condition: str
    high: float
    low: float
    rain_probability: float


class WeatherForecast(BaseModel):
    location: str
    forecast: List[WeatherDay]


class Attraction(BaseModel):
    location: str
    name: str
    category: str
    duration_hours: float
    price: float
    indoor: bool

class TripRequest(BaseModel):
    origin: str
    destination: str
    start_date: str
    end_date: str
    travelers: int

class TripPlan(BaseModel):
    trip: TripRequest
    flights: List[Flight]
    hotels: List[Hotel]
    weather: WeatherForecast
    attractions: List[Attraction]