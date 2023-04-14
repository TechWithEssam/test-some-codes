from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelform_factory
from django.http import HttpResponseBadRequest, Http404, HttpResponse
from django.contrib import messages
from accounts.models import User
from .models import *
from .forms import *
# Create your views here.

def home_product(request) :
    qs = Product.objects.all()
    context = {
        "qs" : qs
    }
    return render(request, 'products/home.html', context)

def not_found_page(request) :
    return render(request, "products/not-found.html", {})



def upload_product_view(request) :
    template_name = "products/create-update.html"
    context = {}
    ImageFormSet = modelform_factory(Images, form=ImageForm)
    if request.method == 'POST':
        form_product = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)
        if form_product.is_valid() and formset.is_valid() :
            obj = form_product.save(commit=False)
            if request.user.is_authenticated:
                obj.salesman = request.user
                obj.save()
                for image in request.FILES.getlist('image') :
                    Images.objects.create(product=obj, image=image)
                return redirect(obj.manager_url())
            form_product.add_error(None, "Your must be logged in to create products.")
        else :
            print(form_product.errors, formset.errors)
    else :
        form_product = ProductForm()
        formset = ImageFormSet()
    context["form_image"] = formset
    context["form_product"] = form_product
    return render(request, template_name, context)


def product_manage_detil(request, slug) :
    template_name = 'products/manager.html'
    obj = get_object_or_404(Product, slug=slug)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_manager = False
    if request.user.is_authenticated:
        is_manager = obj.salesman == request.user
    context = {"object": obj}
    if not is_manager:
        return HttpResponseBadRequest()
    form = ProductUpdateForm(request.POST or None, instance=obj)
    formset = ProductAttachmentInlineFormSet(request.POST or None, queryset=attachments)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        formset.save(commit=False)
        for _form in formset:
            is_delete = _form.cleaned_data.get("DELETE")
            try:
                attachment_obj = _form.save(commit=False)
            except:
                attachment_obj = None
            if is_delete:
                if attachment_obj is not None:
                    if attachment_obj.pk:
                        attachment_obj.delete()
            else:
                if attachment_obj is not None:
                    attachment_obj.product  = instance
                    attachment_obj.save()
        if not obj.all_image_related :
            return redirect(obj.upload_image_url())
        return redirect(obj.manager_url())
    context['form'] = form
    context['formset'] = formset
    return render(request, template_name, context)

def delete_image_view(request, pk) :
    try :
        item = Images.objects.get(pk=pk)
    except Images.DoesNotExist :
        raise Http404
    if request.user.is_authenticated :
        if request.user == item.product.salesman :
            item.delete()
            return redirect(item.product.manager_url())
    return HttpResponseBadRequest()
    
def upload_image(request, pk) :
    template_name = "products/images.html"
    context = {}
    ImageFormSet = modelform_factory(Images, form=ImageForm)
    if request.user.is_authenticated :
        try :
            obj = Product.objects.get(pk=pk)
        except Product.DoesNotExist :
            raise Http404
        form = ImageFormSet(request.POST or None, request.FILES or None) 
        if form.is_valid() :
            for image in request.FILES.getlist('image') :
                    Images.objects.create(product=obj, image=image)
            return redirect(obj.manager_url())
        context["form"] = form
    else :
        return HttpResponseBadRequest()
    return render(request, template_name, context)
    

def detail_product_view(request, slug=None) :
    template_name = "products/detail.html"
    context = dict()
    if slug :
        try :
            qs = Product.objects.get(slug=slug)
            context["qs"] = qs
        except Product.DoesNotExist :
            return redirect("products:not_found")
        if qs.brand :
            similar_brand = Product.objects.filter(brand__name=qs.brand.name).order_by("?")[:4]
            context["s_brand"] = similar_brand
        if qs.category :
            similar_c = Product.objects.filter(category__name=qs.category.name).order_by("?")[:4]
            context["s_category"] = similar_c
    else :
        return redirect("products:home")
    return render(request, template_name, context)
        

