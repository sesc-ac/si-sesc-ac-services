from django.db import models

# Create your models here.
class Cashier(models.Model):
    id = models.AutoField(primary_key= True)

    closeDate = models.CharField()
    closeTime = models.CharField()
    legacyId = models.IntegerField()
    location = models.CharField()
    locationId = models.IntegerField()
    openDate = models.CharField()
    openStatus = models.BooleanField()
    openTime = models.CharField()
    operator = models.CharField()
    operatorId = models.IntegerField()
    totalSalesQuantity = models.IntegerField()
    totalSalesValue = models.DecimalField(decimal_places= 2, max_digits= 10)
    unit = models.CharField()
    
    class Meta:
        managed = False
        db_table = 'Cashier'

    def __str__(self):
        return f'#{self.legacyId} - {self.locationId} - {self.openDate} - {self.operator}'
    
    def update_or_create(fetched_cashier):
        return Cashier.objects.update_or_create(
            legacyId = fetched_cashier['SQCAIXA'],
            locationId = fetched_cashier['CDLOCVENDA'],
            openDate = fetched_cashier['DTABERTURA'],

            defaults = {
                'closeDate': fetched_cashier['DTFECHAMEN'],
                'closeTime': fetched_cashier['HRFECHAMEN'],
                'location': fetched_cashier['DSLOCVENDA'],
                'openTime': fetched_cashier['HRABERTURA'],
                'openStatus': fetched_cashier['STCAIXA'] == '0',
                'operator': fetched_cashier['NMPESSOA'],
                'operatorId': fetched_cashier['CDPESSOA'],
                'totalSalesQuantity': fetched_cashier['QTDVENDAS'],
                'totalSalesValue': fetched_cashier['TOTALVENDIDO'].replace(',', '.') if fetched_cashier['TOTALVENDIDO'] else 0,
                'unit': fetched_cashier['NMUOP'],
            }
        )
    

class Sale(models.Model):
    id = models.AutoField(primary_key= True)

    cashier = models.ForeignKey(Cashier, on_delete= models.CASCADE, db_column= 'cashierId')

    costumer = models.CharField(null= True)
    costumerCategory = models.CharField(null= True)
    costumerCpf = models.CharField(null= True)
    date = models.CharField()
    legacyId = models.IntegerField()
    time = models.CharField()
    value = models.DecimalField(decimal_places= 2, max_digits= 10)

    class Meta:
        managed = False
        db_table = 'Sale'

    def __str__(self):
        return f'#{self.legacyId} - {self.date} - {self.time} - {self.value} - {self.cashier}'
    
    def update_or_create(cashier, fetched_sale):
        return Sale.objects.update_or_create(
            cashier = cashier,
            legacyId = fetched_sale['SQVENDA'],

            defaults = {
                'costumer': fetched_sale['NMCLIENTE'],
                'costumerCategory': fetched_sale['DSCATEGORI'],
                'costumerCpf': fetched_sale['NUCPF'],
                'date': fetched_sale['DTVENDA'],
                'time': fetched_sale['HRVENDA'],
                'value': fetched_sale['VLRECEBIDO'].replace(',', '.'),
            }
        )
    

class SaleItem(models.Model):
    id = models.AutoField(primary_key= True)

    sale = models.ForeignKey(Sale, on_delete= models.CASCADE, db_column= 'saleId')

    itemValue = models.DecimalField(decimal_places= 2, max_digits= 10)
    # legacyId = models.IntegerField()
    product = models.CharField()
    productUnit = models.CharField()
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'SaleItem'

    def __str__(self):
        return f'#{self.id} - {self.sale} - {self.product} - {self.productUnit} - {self.quantity} - {self.itemValue}'
    
    def update_or_create(sale, fetched_sale_item):
        if fetched_sale_item['CDUNIDADE'].strip() == 'KG':
            quantity = int(float(fetched_sale_item['QTDPRODUTO'].replace(',', '.')) * 1000)
        else:
            quantity = int(float(fetched_sale_item['QTDPRODUTO'].replace(',', '.')))
        
        return SaleItem.objects.update_or_create(
            sale = sale,

            itemValue = fetched_sale_item['VLRECEBIDO'].replace(',', '.'),
            # legacyId = fetched_sale_item['SQITVENDA'],
            product = fetched_sale_item['DSPRODUTO'],
            productUnit = 'Hora' if fetched_sale_item['CDUNIDADE'].strip() == 'HS' else 'Grama' if fetched_sale_item['CDUNIDADE'].strip() == 'KG' else 'Unidade',
            quantity = quantity
        )