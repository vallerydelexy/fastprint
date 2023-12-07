from django.db import models
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Status(models.Model):
    id_status = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Categories(models.Model):
    id_kategori = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    nama_kategori = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Products(models.Model):
    id_produk = models.CharField(max_length=30, primary_key=True, unique=True)
    nama_produk = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=30, decimal_places=2)
    kategori_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)