import requests

def calc_wavg(symbol: str, qty: float, side: str,
              depth_limit: int = 1000, max_levels: int = 20) -> float:
    """
    Binance order-book’tan ağırlıklı ortalama fiyatı hesaplar.
    Dönen değer: float (sadece average_price)
    """
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={depth_limit}"
    ob  = requests.get(url, timeout=5).json()

    levels = ob["asks"] if side.upper() == "BUY" else ob["bids"]

    remaining, cost, filled = qty, 0.0, 0.0

    for i, (p_str, a_str) in enumerate(levels):
        if i >= max_levels:
            break
        price  = float(p_str)
        amount = float(a_str)

        take = min(remaining, amount)
        cost += take * price
        filled += take
        remaining -= take
        if remaining <= 0:
            break

    if filled == 0:
        raise ValueError("Yeterli kademe yok")

    return round(cost / filled, 2)

def calc_wavg_full(symbol: str, qty: float, side: str, depth_limit=1000, max_levels=20):
    """
    Binance order-book’tan alınan kademelerle ağırlıklı ortalama fiyat döndürür.
    return:
        { "average_price": 123.45}
    """
    url  = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={depth_limit}"
    ob   = requests.get(url, timeout=5).json()

    levels = ob["asks"] if side.upper() == "BUY" else ob["bids"]

    remaining, cost, filled, resp_lvls = qty, 0.0, 0.0, []
    for i, (p_str, a_str) in enumerate(levels):
        if i >= max_levels: break
        p, a = float(p_str), float(a_str)

        take  = min(remaining, a)
        cost += take * p
        filled += take
        resp_lvls.append({"price": p, "lot": take})
        remaining -= take
        if remaining <= 0: break

    if filled == 0:
        raise ValueError("Yeterli kademe yok")

    return {
        "average_price": round(cost / filled, 2),
        "filled"       : filled,
        "kademeler"    : resp_lvls
    }

    #Full hali istenirse views'ta şurası değişecek:
    # return JsonResponse({"average_price": data["average_price"]})