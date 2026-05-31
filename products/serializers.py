from rest_framework.serializers import Serializer,ModelSerializer
from products.models import Product,Brand,Category,Image,ProductAttribute,Attirbute

class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ["image","img_number"]


class ProductSerializer(ModelSerializer):
    images = ImageSerializer(many = True)
    category = CategorySerializer()
    brand = BrandSerializer()
    class Meta:
        model = Product
        fields = ["title","short_desc","desc","price","off_percent","category",
                  "review_avg_point","final_price","is_available","brand","created_at","updated_at"]

