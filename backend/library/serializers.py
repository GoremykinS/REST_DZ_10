from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, StringRelatedField, Serializer
from .models import Author, Book, Bio


class AuthorModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookModelSerializer(ModelSerializer):
    # authors = AuthorModelSerializer(many=True)
    # authors = StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = '__all__'


class BioModelSerializer(ModelSerializer):
    # author = AuthorModelSerializer()

    class Meta:
        model = Bio
        fields = '__all__'


class AuthorSerializer(Serializer):

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birthday_year = validated_data.get('birthday_year', instance.birthday_year)
        instance.save()
        return instance

    def create(self, validated_data):
        author = Author(**validated_data)
        author.save()
        return author

    def validate_birthday_year(self, value):
        if value < 1000:
            raise ValidationError('Must be gt 1000')
        return value

    def validate(self, attrs):
        if attrs['last_name'] == 'Достоевский' and attrs['birthday_year'] != 1820:
            raise ValidationError('Must be 1820')
        return attrs

    first_name = CharField(max_length=64)
    last_name = CharField(max_length=64)
    birthday_year = IntegerField()


class BioSerializer(Serializer):
    text = CharField(max_length=64)
    author = AuthorSerializer()


class BookSerializer(Serializer):
    title = CharField(max_length=64)
    authors = AuthorSerializer(many=True)
