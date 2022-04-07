from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer, StringRelatedField, Serializer
from .models import Project, Todo, User


class ProjectModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectModelSerializerV2(ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_users', 'project_name']


class TodoModelSerializer(ModelSerializer):
    #author = ProjectModelSerializer()
    class Meta:
        model = Todo
        fields = '__all__'


class UserModelSerializer(ModelSerializer):
    #author = ProjectModelSerializer()
    class Meta:
        model = User
        fields = '__all__'


class ProjectSerializer(Serializer):

    def update(self, instance, validated_data):
        instance.project_users = validated_data.get('project_users', instance.project_users)
        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.git_name = validated_data.get('git_name', instance.git_name)
        instance.save()
        return instance

    def create(self, validated_data):
        author = Project(**validated_data)
        author.save()
        return author

    #
    # def validate(self, attrs):
    #     if attrs['project_name'] != 'project_ivan':
    #         raise ValidationError("it's not project_ivan")
    #     return attrs


    project_users = CharField(max_length=64)
    project_name = CharField(max_length=64)
    git_name = CharField(max_length=64)


# class TodoSerializer(Serializer):
#     text = CharField(max_length=64)
#     author = ProjectSerializer()


class TodoSerializer(Serializer):
    text = CharField(max_length=64)
    time = models.DateTimeField(auto_now=True)
    author = CharField(max_length=64)



class UserSerializer(Serializer):
    age = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    user_name = CharField(max_length=64)

#     def update(self, instance, validated_data):
#         instance.text = validated_data.get('text', instance.text)
#         instance.time = validated_data.get('time', instance.time)
#         instance.author = validated_data.get('author', instance.author)
#         instance.save()
#         return instance
# #
#     def create(self, validated_data):
#         author = Todo(**validated_data)
#         author.save()
#         return author
#
#
#     # def validate(self, attrs):
#     #     if attrs['author'] != 'vasay':
#     #         raise ValidationError("it's not vasay")
#     #     return attrs
#
#     text = CharField(max_length=64)
#     time = models.DateTimeField(auto_now=True)
#     author = CharField(max_length=64)
