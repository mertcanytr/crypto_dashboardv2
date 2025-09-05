from django.urls import path
from .views import (
    WavgPriceOnlyView,
    MarketSnapshotView,
    WavgView, 
    MarketDataView  
)

urlpatterns = [
    path('wavg/', WavgView.as_view(), name="wavg"),
    path('market-data/', MarketDataView.as_view()),
    path("wavg/<str:symbol>/<str:qty>/<str:side>/", WavgPriceOnlyView.as_view()),
    path("market/<str:symbol>/",  MarketSnapshotView.as_view()),

]
