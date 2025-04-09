import requests
from setup.settings import CUPONS_KEY

headers = {'CUPONS-KEY': CUPONS_KEY}

def fetchCashiers(initial_date, final_date):
    data = {
        'initialDate': initial_date,
        'finalDate': final_date 
    }

    return requests.post(
        'http://consulta.sescacre.com.br/cupons/caixas.php', 
        data= data,
        headers= headers 
    )
    

def fetchCashierSales(legacy_id, open_date, location_id, operator_id):
    data = {
        'cashier': legacy_id,
        'date': open_date,
        'locationId': location_id,
        'operator': operator_id
    }

    return requests.post(
        'http://consulta.sescacre.com.br/cupons/vendas.php',
        data= data,
        headers= headers
    )


def fetchSaleItems(cashier_legacy_id, open_date, sale_legacy_id, operator_id):
    data = {
        'cashier': cashier_legacy_id,
        'date': open_date,
        'sale': sale_legacy_id,
        'operator': operator_id
    }

    return requests.post(
        'http://consulta.sescacre.com.br/cupons/itens.php',
        data= data,
        headers= headers
    )