from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Ingredient
from supplier.serializers import (
    AdminSupplierSerializer
)


class BaseIngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class BaristaIngredientSerializer(BaseIngredientSerializer):
    supplier = SlugRelatedField(
        read_only=True,
        slug_field='custom_id'
    )


class ManagerIngredientSerializer(BaseIngredientSerializer):
    supplier = AdminSupplierSerializer()
