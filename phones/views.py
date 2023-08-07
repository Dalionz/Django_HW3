from django.http import HttpResponse
from django.shortcuts import render, redirect

from phones.models import Phone


def get_phones(phone):
    return [{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'release_date': p.release_date,
        'lte_exists': p.lte_exists,
        'slug': p.slug,
        'image': p.image,
    } for p in phone.objects.all()]


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_phone = request.GET.get('sort', None)
    phones_all = get_phones(Phone)
    if sort_phone == 'name':
        phones_all.sort(key=lambda d: d['name'])
    if sort_phone == 'max_price':
        phones_all.sort(reverse=True, key=lambda d: d['price'])
    if sort_phone == 'min_price':
        phones_all.sort(reverse=False, key=lambda d: d['price'])

    context = {'phones': phones_all, 'sort_by': sort_phone}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug__contains=slug).first()
    context = {'phone': phone}
    return render(request, template, context)


def show_all_product(request):
    phones_all = Phone.objects.all()
    phones_list = [f'{c.image}' for c in phones_all]
    return HttpResponse('<br>'.join(phones_list))
