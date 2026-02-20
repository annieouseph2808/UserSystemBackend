from django.core import serializers

class UserSerializer(serializers.ModelSerialize):
    class Meta:
        model = User #which model to serialize
        fields = '__all__' # what all fields to include
        