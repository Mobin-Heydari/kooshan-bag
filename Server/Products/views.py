from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from django.core.paginator import Paginator
from .models import(
    PrimeryCategory,
    Category,
    Product,
    Color,
    Comment
)
from .forms import CommentForm
    
    
class ProductDetail(View):
    
    def get(self, request, slug):
        
        product = get_object_or_404(Product, slug=slug, available=True)
        
        categories = Category.objects.all()
        
        primery_categories = PrimeryCategory.objects.all()
        
        comments = Comment.objects.filter(product=product)
        
        form = CommentForm
        
        page_number = request.GET.get('page')
        
        paginator = Paginator(comments, 6)
        
        queryset = paginator.get_page(page_number)
        
        suggested_products = Product.objects.filter(
            primery_category = product.primery_category,
            category = product.category
            
        ).order_by('-created')[:6]
        
        
        return render(request,'products/detail.html', {
            'product' : product,
            'categories' : categories,
            'primery_categories' : primery_categories,
            'comments' : queryset,
            'form' : form,
            'suggested_products' : suggested_products,
        })
    
    
    def post(self, request, slug):
        
        form = CommentForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            product = get_object_or_404(
                Product,
                slug=slug
            )
            
            Comment.objects.create(
                product = product,
                suggestion = request.POST.get('suggestion'),
                comment = cd['comment'],
                title = cd['title']
            )
            
            return redirect('products:product_detail', slug)
        
        return render(request, 'products/detail.html', {'form' : form})


class ProductListFilter(TemplateView):
    
    template_name = "products/list.html"
    product = Product.objects.all()
    
    
    def get_context_data(self, **kwargs):
        request = self.request
        primery_category = request.GET.get('primery_category')
        color = request.GET.get('color')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        categories = Category.objects.all()
        primery_categories = PrimeryCategory.objects.all()
        colors = Color.objects.all()
        
        queryset = Product.objects.all()
        
        if primery_category:
            queryset = queryset.filter(primery_category=primery_category).distinct()
                
        if color:
            print(color)
            queryset = queryset.filter(colors=color).distinct()
        
        if min_price and max_price:
            print(min_price, max_price)
            queryset = queryset.filter(price__lte=max_price, price__gte=min_price).distinct()
        
        page_number = request.GET.get('page')
        paginator = Paginator(queryset, 8)
        queryset = paginator.get_page(page_number)
        
        
        context = super(ProductListFilter, self).get_context_data()
        context = {
            'products' : queryset,
            'categories' : categories,
            'primery_categories' : primery_categories,
            'colors' : colors,
            'color' : color,
            'min_price' : min_price,
            'max_price' : max_price,
            'primery_category' : primery_category,
        }
        return context