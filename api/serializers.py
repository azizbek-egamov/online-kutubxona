from rest_framework import serializers
from main.models import Kitob


class KitoblarSerializer(serializers.ModelSerializer):
    
    # category = serializers.SerializerMethodField()
    
    # def get_category(self, obj):
    #     return obj.category.name
    
    class Meta:
        model = Kitob
        fields = "__all__"
        