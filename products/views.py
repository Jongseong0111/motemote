import json
from random import sample
from typing import ItemsView

from django.http     import JsonResponse
from django.views    import View
from django.db.models  import Q

from products.models import Option, Product, Category, Concept, Item

class PageView(View):
     def get(self, request):
        try:
            product_id  = request.GET.get('product_id', None)
            category_id = request.GET.get('category_id', None)
            option_id   = request.GET.get('option_id', None)
            main        = request.GET.get('main', None)

            if not main and (not Product.objects.filter(id=product_id).exists() or not Category.objects.filter(id=category_id).exists() or not Option.objects.filter(id=option_id)):
                return JsonResponse({'MESSAGE':'NO_MENU'}, status=400)

            concepts = Concept.objects.filter(item__category_id = category_id) if not main else Item.objects.order_by('-order_quantity')[:8] 
            
            results = [
                {
                        'concept'             : concept.name if not main else None,
                        'concept_description' : concept.content if not main else None,
                        'concept_id'          : concept.id if not main else None,
                        'information'         : [
                            {
                                'id'       : item.id,
                                'name'     : item.name,
                                'price'    : item.price,
                                'discount' : item.discount,
                                'stock'    : item.stock,
                                'color'    : item.color.name if not item.color is None else None,
                                'image'    : item.image_set.get(main=1).image_url
                            } for item in (Item.objects.filter(Q(concept_id=concept.id)&Q(option_id=option_id)) if not main else [concept])]
                } for concept in concepts]

            if main: 
                for result in results:
                    del result['concept'], result['concept_description'], result['concept_id']            

            return JsonResponse({'RESULTS': results}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)