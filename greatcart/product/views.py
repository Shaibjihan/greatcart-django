from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from django.core.paginator import(
    PageNotAnInteger,
    EmptyPage,
    InvalidPage,
    Paginator
)

from cart.carts import Cart
from . models import (
    Category,
    Product,
    Slider
)


class Home (generic.TemplateView):
    template_name = 'homes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'featured_categories': Category.objects.filter(featured= True),
                'featured_products': Product.objects.filter(featured= True),
                'slider': Slider.objects.filter(show=True)
                
            }
        )
        return context
    


# Create your views here.
class ProductDetails(generic.DetailView):
    model = Product
    template_name = 'product/product-details.html'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        cart_itmes = Cart(self.request)
        print(cart_itmes.cart)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Corrected the assignment below
        context['related_products'] = self.get_object().related.all() 
        return context



class CategoryDetails(generic.DetailView):
    model = Category
    template_name = 'product/category-details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Corrected the assignment below
        context['products'] = self.get_object().products.all() 
        return context


class CustomPaginator:
    def __init__(self, request, queryset, paginated_by ):
        self.paginator = Paginator(queryset, paginated_by)
        self.paginated_by = paginated_by
        self.queryset =queryset
        self.page = request.GET.get('page', 1 )


    def get_queryset(self):
        try:
            queryset = self.paginator.page(self.page)
        except PageNotAnInteger:
            queryset = self.paginator.page(1)
        except EmptyPage:
            queryset = self.paginator.page(1)
        except InvalidPage:
            queryset =  self.paginator.page(1)

        return queryset

            
        




class ProductList(generic.ListView):
    model = Product
    template_name ='product/product-list.html'
    context_object_name = 'object_list'
    paginate_by = 6


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Initialize your custom paginator
        page_obj = CustomPaginator(self.request, self.get_queryset(), self.paginate_by)
        
        # Update the context with results from your custom paginator
        context['object_list'] = page_obj.get_queryset()
        context['paginator'] = page_obj.paginator
        
        return context
    
class SearchProducts (generic.View):
    def get(self, *args, **kwargs):
        key = self.request.GET.get('key', '')
        products = Product.objects.filter(
            Q(title__icontains=key) | Q(category__title__icontains=key)

        )
        context = {
            'products' : products,
            "key" : key
        }
        return  render(self.request, 'product/search-products.html', context )
    
        
        
    
