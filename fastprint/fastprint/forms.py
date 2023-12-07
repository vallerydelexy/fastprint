from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori_id', 'status_id']
        widgets = {
            'kategori_id': forms.Select(attrs={'class': 'form-control'}),
            'status_id': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        editing_instance = kwargs.pop('editing_instance', None)
        super().__init__(*args, **kwargs)

        if editing_instance:
            # If editing, disable the id_produk field and remove the label
            self.fields['id_produk'].widget.attrs['readonly'] = True
            self.fields['id_produk'].label = 'id'
        else:
            # If adding, remove the id_produk field from the form if it exists
            if 'id_produk' in self.fields:
                del self.fields['id_produk']

    def clean(self):
        cleaned_data = super().clean()

        # If adding a new product, get the latest id_produk and increment it
        if 'id_produk' not in cleaned_data and not self.instance.id_produk:
            latest_product = Products.objects.order_by('-updated_at').first()
            latest_id = latest_product.id_produk if latest_product else 0
            new_id = str(int(latest_id) + 1)

            cleaned_data['id_produk'] = new_id

        return cleaned_data

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