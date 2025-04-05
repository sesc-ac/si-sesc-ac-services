from django.http import JsonResponse
from rest_framework.decorators import api_view
from setup.settings import CUPONS_KEY
from services.xamp_connection import fetchCashiers, fetchCashierSales, fetchSaleItems
from .models import Cashier, Sale, SaleItem

@api_view(['POST'])
def cashiers(request):
    
    # Authentication

    if not 'cupons_key' in request.headers or request.headers['cupons_key'] != CUPONS_KEY:
        return JsonResponse(
            status= 401, 
            data= {'error': 'Invalid Credentials'}
        )
    
    print('Authentication OK')

    # Data Input Validation

    if not 'initialDate' in request.POST or not 'finalDate' in request.POST:
        return JsonResponse(
            status= 400, 
            data= {'error': 'Invalid Input Data'}
        )
    
    print('Data Input Validation OK')

    initial_date = request.POST.get('initialDate')
    final_date = request.POST.get('finalDate')

    print('Cashiers Post Data', initial_date, final_date)

    # Fetching Cashiers Data

    response = fetchCashiers(initial_date, final_date)

    if response.status_code != 200:
        return JsonResponse(
            status= 500, 
            data= {'error': 'Internal Fetch Error'}
        )

    cashiers = response.json()

    print('Cashiers Data Fetch OK')

    # Init Data Sync
    
    print('Iterating over Cashier Data')
    print()

    total_cashiers_created = 0
    total_cashiers_updated = 0

    total_sales_created = 0
    total_sales_updated = 0

    total_sales_items_created = 0
    total_sales_items_updated = 0

    for fetched_cashier in cashiers:
        print('Fetched Cashier: ', fetched_cashier)

        # Update or create the Cashier

        cashier, created = Cashier.update_or_create(fetched_cashier)

        if created:
            total_cashiers_created += 1
        else:
            total_cashiers_updated += 1

        status = 'Created' if created else 'Updated'

        print(f'Cashier {cashier} {status}')
        print()
        
        print('Sales Post Data', cashier.legacyId, cashier.openDate, cashier.locationId, cashier.operatorId)
        
        # Fetching Sales Data

        response = fetchCashierSales(cashier.legacyId, cashier.openDate, cashier.locationId, cashier.operatorId)

        if response.status_code != 200:
            print('Fetch Sales Error...')
            print()
            continue
        
        sales = response.json()
        
        print('Sales Data Fetch OK')
        
        # Iterating over Sales Data

        print('Iterating Over the List')
        print()
            
        for fetched_sale in sales:
            print('Fetched Sale: ', fetched_sale)
            print()
            
            # Update or created Sale

            sale, created = Sale.update_or_create(cashier, fetched_sale)

            if created:
                total_sales_created += 1
            else:
                total_sales_updated += 1

            status = 'Created' if created else 'Updated'

            print(f'Sale {sale} {status}')
            print()

            if status == 'Created':
                print('Sale Items Post Data', cashier.legacyId, cashier.openDate, sale.legacyId, cashier.operatorId)

                # Fetching Sale Items Data

                response = fetchSaleItems(cashier.legacyId, cashier.openDate, sale.legacyId, cashier.operatorId)

                if response.status_code != 200:
                    print('Fetch Sale Items Error...')
                    print()
                    continue

                sales_items = response.json()

                print('Sale Items Data Fetch OK')

                # Iterating over Sale Items Data

                print('Iterating Over the List')
                print()

                for fetched_sale_item in sales_items:
                    print('Fetched Sale Item: ', fetched_sale_item)
                    print()

                    # Update or created Sale Item

                    sale_item, created = SaleItem.update_or_create(sale, fetched_sale_item)

                    if created:
                        total_sales_items_created += 1
                    else:
                        total_sales_items_updated += 1

                    status = 'Created' if created else 'Updated'

                    print(f'Sale Item {sale_item} {status}')
                    print()

    return JsonResponse({
        'total_cashier_created': total_cashiers_created,
        'total_cashier_updated': total_cashiers_updated,
        'total_sales_created': total_sales_created,
        'total_sales_updated': total_sales_updated,
        'total_sales_items_created': total_sales_items_created,
        'total_sales_items_updated': total_sales_items_updated,
        'message': f'Sincronização de Caixas e Vendas realizada com sucesso!',
    })

    

# def estudantes(request):
#     # posts = Post.objects.all()
#     # print(posts)

#     # new_post = Post.objects.create(title= 'Post 4', content= 'Quarta vez', published= False)

#     # print(new_post)
#     # posts = Post.objects.all()
#     # print(posts)

#     headers = {'CUPONS-KEY': 's3sc4cr3cupons4pik3y2025'}
#     response = requests.post('http://consulta.sescacre.com.br/cupons/caixas.php', headers= headers, data= {'initialDate': '2025-03-24', 'finalDate': '2025-03-24'})

#     if not response.ok:
#         return({'error': 'erro'})
    
#     for fetched_cashier in response.json():
#         print(fetched_cashier)
        
#         # new_cashier = Cashier()

#         closeTime = fetched_cashier['HRFECHAMEN']
#         legacyId = fetched_cashier['SQCAIXA']
#         location = fetched_cashier['DSLOCVENDA']
#         locationId = fetched_cashier['CDLOCVENDA']
#         openDate = fetched_cashier['DTABERTURA']
#         openStatus = fetched_cashier['STCAIXA']
#         openTime = fetched_cashier['HRABERTURA']
#         operator = fetched_cashier['NMPESSOA']
#         totalSalesQuantity = fetched_cashier['QTDVENDAS']
#         totalSalesValue = fetched_cashier['TOTALVENDIDO'].replace(',', '.') if fetched_cashier['TOTALVENDIDO'] is not None else '0'
#         unit = fetched_cashier['NMUOP']
        
#         new_cashier = Cashier.objects.create(
#             closeTime= closeTime,
#             legacyId= legacyId,
#             location= location,
#             locationId= locationId,
#             openDate= openDate,
#             openStatus= openStatus,
#             openTime= openTime,
#             operator= operator,
#             totalSalesQuantity= totalSalesQuantity,
#             totalSalesValue= totalSalesValue,
#             unit= unit
#         )
#         print(f'CAIXA #{new_cashier.id} criado com sucesso.')

#         print()

#     # for i in response.json():
#     #     print(i)

#     return JsonResponse({'teste': 'deu'})