from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from django.db.models.signals import m2m_changed
from django.db.models import F
from menu.models import MenuItem, Component
from story.models import Ingredient

User = get_user_model()


class PurchaseOrder(models.Model):
    STATUS_CHOICE = (
        (1, _("New")),  #Nowe
        (2, _("Pending")),  #W przygotowaniu
        (3, _("Ready")),  #Gotowe
        (4, _("Retrieved")),  # Odebrane
        (5, _("Canceled")),  # Anulowane
    )
    items = models.ManyToManyField("menu.MenuItem")
    status = models.PositiveIntegerField(
        choices=STATUS_CHOICE,
        default=1
    )
    order_number = models.CharField(max_length=50)
    client_name = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.order_number} - {self.get_status_display()}"

def change_story(instance, **kwargs):
    action = kwargs.get('action')
    pk_set = kwargs.get('pk_set')

    all_quantity = dict()
    obj = list()

    for id in pk_set:
        item = MenuItem.objects.get(pk=id)
        for component in item.ingredients.all():
            if component.pk in all_quantity:
                all_quantity[component.pk] += component.quantity
            else:
                all_quantity[component.pk] = component.quantity

        for key in all_quantity.keys():
            all_res = all_quantity[key]
            new_obj = Component.objects.get(pk=key).ingredient
            if action == 'post_add':
                new_obj.quantity = F('quantity') - all_res
            if action == 'post_remove':
                new_obj.quantity = F('quantity') + all_res
            obj.append(new_obj)

    Ingredient.objects.bulk_update(obj, ['quantity'])


m2m_changed.connect(change_story, sender=PurchaseOrder.items.through)
