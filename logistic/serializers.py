from django.db.migrations import serializer
from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', ]


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):

        # в validated_date - json запрос с полями 'addess' и 'positions'
        # в positions сохраняем только поле 'positions'
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам (в validated_data осталось поле 'adress')
        stock = super().create(validated_data)

        # перебираем все positions и создаем для каждой объект модели StockProduct,
        # где stock=stock - это ссылка на склад, созданный строчкой выше
        for pos in positions:
            StockProduct.objects.create(
                stock=stock,
                product=pos.get('product'),
                quantity=pos.get('quantity'),
                price=pos.get('price')
            )
        return stock

    def update(self, instance, validated_data):

        # в validated_date - json запрос с полями 'addess' и 'positions'
        # в positions сохраняем только поле 'positions'
        positions = validated_data.pop('positions')

        # в instance находится наш склад. Согласно README мы передаем только поле
        # positions, так что validated_data всегда будет пустым
        stock = super().update(instance, validated_data)

        # метод update_or_create ищет в базе данных обхект с полями stock и product,
        # если находит - обновляет остальные поля, указанные в defaults, а если не находит,
        # то создает новый объект
        for pos in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=pos.get('product'),
                defaults={
                    'quantity': pos.get('quantity'),
                    'price': pos.get('price'),
                }
            )
        return stock
