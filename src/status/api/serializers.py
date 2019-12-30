from rest_framework import serializers

from status.models import Status

"""
class CustomSerializer(serializers.Serializer):
    content = serializers.CharField()
    email = serializers.EmailField()
    
data = {'email': 'naver@naver.com', 'content':'please delete me'}
create_obj_serializer = CustomSerializer(data=data)
if create_obj_serializer.is_valid():
    data = create_obj_serializer.data
    print(data)
"""


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'user',
            'content',
            'image',
        ]

    """
    def validate_<fieldname>(self, value):
        validation...
        return value
   """

    # Field level validation
    # def validate_content(self, value):
    #     if len(value) > 10000:
    #         raise serializers.ValidationError("This is way too long.")
    #     return value

    # Serializer level validation
    def validate(self, data):
        content = data.get('content', None)
        if content == '':
            content = None
        image = data.get('image', None)
        if image is None and content is None:
            raise serializers.ValidationError('Content or image is required')
        return data
