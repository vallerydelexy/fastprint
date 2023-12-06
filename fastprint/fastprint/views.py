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

def getData(username=False, retry=0):
    print("try ", retry)
    try:
        url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer";
        cur_gmt = datetime.datetime.now(pytz.timezone('GMT'))
        nextday = cur_gmt + datetime.timedelta(days=1)
        payload = {
            'username': username or f"tesprogrammer{nextday.strftime('%d%m%y')}C00",
            'password': hashlib.md5(f"bisacoding-{nextday.strftime('%d-%m-%y')}".encode()).hexdigest(),
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Request failed with status code {response.status_code}")
            if retry == 0:
                retry += 1
            usernameFromResponse = response.headers.get('X-Credentials-Username').split()[0]
            if retry == 1:
                return getData(usernameFromResponse, retry)
            else:
                return HttpResponse(status=500, content='Internal Server Error')
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return HttpResponse(status=500, content='Internal Server Error')


def index(request):
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


    productsFromDB = Products.objects.filter(status_id__nama_status='bisa dijual')
    products_json = serialize('json', productsFromDB)
    products_list = json.loads(products_json)

    categoriesFromDB = Categories.objects.all()
    statusFromDB = Status.objects.all()

    for item in products_list:
        item['fields']['kategori'] = categoriesFromDB.get(id_kategori=item['fields']['kategori_id']).nama_kategori
        item['fields']['status'] = statusFromDB.get(id_status=item['fields']['status_id']).nama_status
        item['fields'].pop('created_at', None)
        item['fields'].pop('updated_at', None)
        item['fields'].pop('kategori_id', None)
        item['fields'].pop('status_id', None)

    updated_products_json = json.dumps(products_list)
    column_names = [col for col in products_list[0]['fields'].keys()]

    context = {
        "data": updated_products_json,
        "column_names": column_names,
    }

    return render(request, 'index.html', context)
