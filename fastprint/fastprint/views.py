from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import requests
import datetime
import hashlib
import pytz
from .models import Products, Status, Categories
from django.core.serializers import serialize
from .forms import ProductForm

def getData(username=False, retry=0):
    try:
        url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer";
        cur_gmt = datetime.datetime.now(pytz.timezone('GMT'))
        nextday = cur_gmt + datetime.timedelta(days=1)
        payload_next = {
            'username': username or f"tesprogrammer{nextday.strftime('%d%m%y')}C00",
            'password': hashlib.md5(f"bisacoding-{nextday.strftime('%d-%m-%y')}".encode()).hexdigest(),
        }
        payload_cur = {
            'username': username or f"tesprogrammer{cur_gmt.strftime('%d%m%y')}C00",
            'password': hashlib.md5(f"bisacoding-{cur_gmt.strftime('%d-%m-%y')}".encode()).hexdigest(),
        }
        if retry < 2:
            response = requests.post(url, data=payload_cur)
        else:
            response = requests.post(url, data=payload_next)

        if response.status_code == 200:
            print("try: ", retry," status code: ", response.status_code)
            return json.loads(response.text)
        else:
            print("try: ", retry," status code: ", response.status_code)
            retry += 1
            usernameFromResponse = response.headers.get('X-Credentials-Username').split()[0]
            if retry <= 3:
                return getData(usernameFromResponse, retry)
            else:
                return HttpResponse(status=500, content='Internal Server Error')
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return HttpResponse(status=500, content='Internal Server Error')

def getProducts(request):
    data = getData()
    for item in data['data']:
        if not Categories.objects.filter(nama_kategori=item['kategori']).exists():
            category = Categories(
                nama_kategori=item['kategori'],
            )
            try:
                category.save()
            except IntegrityError:
                print(f"Duplicate category entry: {item['kategori']}")
                pass

    for item in data['data']:
        if not Status.objects.filter(nama_status=item['status']).exists():
            status = Status(
                nama_status=item['status'],
            )
            try:
                status.save()
            except IntegrityError:
                print(f"Duplicate status entry: {item['status']}")
                pass
            
    for item in data['data']:
        if not Products.objects.filter(id_produk=item['id_produk']).exists():
            category_instance = Categories.objects.get(nama_kategori=item['kategori'])
            status_instance = Status.objects.get(nama_status=item['status'])

            product = Products(
                id_produk=item['id_produk'],
                nama_produk=item['nama_produk'],
                harga=item['harga'],
                kategori_id=category_instance,
                status_id=status_instance,  
            )
            try:
                product.save()
            except IntegrityError:
                print(f"Duplicate entry: {item['id_produk']}")
                pass

    return HttpResponse(status=200, content='OK')

def index(request):
    productsFromDB = Products.objects.filter(status_id__nama_status='bisa dijual')
    products_json = serialize('json', productsFromDB, fields=('id_produk', 'nama_produk', 'harga', 'kategori_id', 'status_id'))
    products_list = json.loads(products_json)

    categoriesFromDB = Categories.objects.all()
    statusFromDB = Status.objects.all()

    for item in products_list:
        item['fields']['id'] = item['pk']
        item['fields']['kategori'] = categoriesFromDB.get(id_kategori=item['fields']['kategori_id']).nama_kategori
        item['fields']['status'] = statusFromDB.get(id_status=item['fields']['status_id']).nama_status
        item['fields'].pop('kategori_id', None)
        item['fields'].pop('status_id', None)

    updated_products_json = json.dumps(products_list)
    column_names = [col for col in products_list[0]['fields'].keys()]

    context = {
        "data": updated_products_json,
        "column_names": column_names,
    }

    return render(request, 'index.html', context)

def deleteProduct(request, id):
    product = Products.objects.get(id_produk=id)
    product.delete()
    return HttpResponse(status=200, content='OK')
    pass

def editProduct(request, id):
    product = Products.objects.get(id_produk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200, content='Product updated successfully')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})
    pass