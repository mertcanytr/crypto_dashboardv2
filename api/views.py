# api/views.py
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import datetime
from .utils import calc_wavg

class WavgView(APIView):
    def post(self, request):
        try:
            symbol = request.data.get("symbol")
            qty = float(request.data.get("qty"))
            side = request.data.get("side")

            # Binance order book verisi
            url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=1000"
            resp = requests.get(url)
            orderbook = resp.json()

            # Maksimum gösterilecek kademe sayısı
            MAX_KADEME = 20

            if side == "BUY":
                # Satış kademelerinden al
                levels = orderbook.get("asks", [])
            else:
                # Alış kademelerinden sat
                levels = orderbook.get("bids", [])

            remaining = qty
            cost = 0.0
            filled = 0.0
            response_kademeler = []

            for i, (price_str, amount_str) in enumerate(levels):
                if i >= MAX_KADEME:  # Kademe limiti
                    break

                price = float(price_str)
                amount = float(amount_str)

                if remaining <= amount:
                    cost += remaining * price
                    filled += remaining
                    response_kademeler.append({"price": price, "lot": remaining})
                    remaining = 0
                    break
                else:
                    cost += amount * price
                    filled += amount
                    response_kademeler.append({"price": price, "lot": amount})
                    remaining -= amount

            if filled == 0:
                return JsonResponse({"error": "Yeterli veri yok"}, status=400)

            avg_price = cost / filled
            timestamp = datetime.now().strftime("%H:%M:%S")

            return JsonResponse({
                "average_price": round(avg_price, 2),
                "kademeler": response_kademeler,
                "timestamp": timestamp
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class MarketDataView(APIView):
    def get(self, request):
        try:
            symbol = request.GET.get("symbol", "").upper()
            if not symbol:
                return JsonResponse({"error": "symbol parametresi zorunlu"}, status=400)

            period = "5m"
            limit  = 500

            # --- DOĞRU endpoint'ler  ------------------------------------
            oi_url = f"https://fapi.binance.com/futures/data/openInterestHist"
            ls_url = f"https://fapi.binance.com/futures/data/globalLongShortAccountRatio"
            fr_url = f"https://fapi.binance.com/fapi/v1/fundingRate"      # <-- düzeltildi
            # -------------------------------------------------------------

            headers = {"User-Agent": "Mozilla/5.0"}  # JSON yerine HTML gelmesini azaltır

            oi = requests.get(oi_url, params={"symbol":symbol,"period":period,"limit":limit},
                              timeout=5, headers=headers)
            ls = requests.get(ls_url, params={"symbol":symbol,"period":period,"limit":limit},
                              timeout=5, headers=headers)
            fr = requests.get(fr_url, params={"symbol":symbol,"limit":1},
                              timeout=5, headers=headers)

            oi.raise_for_status(); ls.raise_for_status(); fr.raise_for_status()

            open_interest  = oi.json()
            long_short     = ls.json()
            funding_rate   = fr.json()

            last_oi = open_interest[-1] if open_interest else {}
            last_ls = long_short[-1]    if long_short  else {}
            last_fr = funding_rate[-1]  if funding_rate else {}

            return JsonResponse({
                "open_interest"   : float(last_oi.get("sumOpenInterest", 0)),
                "long_short_ratio": float(last_ls.get("longShortRatio", 0)),
                "timestamp"       : last_oi.get("timestamp") or last_ls.get("timestamp"),
                "funding_rate"    : float(last_fr.get("fundingRate", 0))
            })
        except Exception as e:
            # Terminalde ayrıntı görünsün
            import traceback; traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)

class WavgPriceOnlyView(APIView):
    authentication_classes = []
    permission_classes     = []

    def get(self, request, symbol, qty, side):
        try:
            avg = calc_wavg(symbol.upper(), float(qty), side.upper())
            return JsonResponse({"average_price": avg})
        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# -------------- 2)  Piyasa Verileri JSON ----------------------------
class MarketSnapshotView(APIView):
    """
    GET /api/market/<symbol>/
    Dönen JSON:
        {
          "open_interest": 1234567,
          "long_short_ratio": 1.53,
          "funding_rate": 0.00051,
          "timestamp": 1694617200000
        }
    """
    authentication_classes = []
    permission_classes     = []

    def get(self, request, symbol):
        try:
            symbol = symbol.upper()
            period = "5m"
            limit  = 1
            h = {"User-Agent": "Mozilla/5.0"}

            oi_url = "https://fapi.binance.com/futures/data/openInterestHist"
            ls_url = "https://fapi.binance.com/futures/data/globalLongShortAccountRatio"
            fr_url = "https://fapi.binance.com/fapi/v1/fundingRate"

            oi = requests.get(oi_url, params={"symbol":symbol,"period":period,"limit":limit},
                              timeout=5, headers=h).json()
            ls = requests.get(ls_url, params={"symbol":symbol,"period":period,"limit":limit},
                              timeout=5, headers=h).json()
            fr = requests.get(fr_url, params={"symbol":symbol,"limit":1},
                              timeout=5, headers=h).json()

            if not (oi and ls):
                return JsonResponse({"error":"Binance verisi yok"}, status=502)

            return JsonResponse({
                "open_interest"   : float(oi[-1]["sumOpenInterest"]),
                "long_short_ratio": float(ls[-1]["longShortRatio"]),
                "funding_rate"    : float(fr[-1]["fundingRate"]) if fr else 0,
                "timestamp"       : oi[-1]["timestamp"]
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)           