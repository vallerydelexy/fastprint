from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['nama_produk', 'harga', 'kategori_id', 'status_id']
        widgets = {
            'kategori_id': forms.Select(attrs={'class': 'form-control'}),
            'status_id': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nama_produk(self):
        nama_produk = self.cleaned_data['nama_produk']
        if not nama_produk:
            raise forms.ValidationError("Nama Produk cannot be empty.")
        return nama_produk

    def clean_harga(self):
        harga = self.cleaned_data['harga']
        try:
            harga = float(harga)
        except ValueError:
            raise forms.ValidationError("Harga must be a valid number.")
        return harga
