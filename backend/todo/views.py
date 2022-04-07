import io

from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import renderer_classes, api_view, action
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser


from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import *
from rest_framework.pagination import LimitOffsetPagination

# AllowAny все права, IsAuthenticated залогиненые поьзователи, IsAuthenticatedOrReadOnly могут читать не залогиненые,
# IsAdminUser админы, DjangoModelPermissions, DjangoModelPermis
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, BasePermission

from rest_framework.serializers import Serializer, CharField, IntegerField
from rest_framework.viewsets import ModelViewSet



from .serializers import ProjectModelSerializer, TodoModelSerializer, ProjectModelSerializerV2, UserModelSerializer  , ProjectSerializer, TodoSerializer
from .models import Project, Todo, User


# client -> [url] -> [view] -> [serializer] -> [model]


class ProjectModelViewSet(ModelViewSet):
    # renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    # serializer_class = ProjectModelSerializer
    def get_serializer_class(self):
        if self.request.version == '2.0':
            return ProjectModelSerializerV2
        return ProjectModelSerializer

    queryset = Project.objects.all()


class TodoViewSet(ModelViewSet):
    serializer_class = TodoModelSerializer
    queryset = Todo.objects.all()


class UserModelViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


# -----
class ProjectView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        authors = Project.objects.all()
        serializer = ProjectSerializer(authors, many=True)
        return Response(serializer.data)

# class ProjectLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 3
#
#
# class GenericViewSet(object):
#     pass

# class ProjectViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     serializer_class = ProjectSerializer
#     queryset = Project.objects.all()
#     filterset_fields = ['project_name']
#     pagination_class = ProjectLimitOffsetPagination
#
#     # http://127.0.0.1:8000/api/authors/get_author_name/
#
#     @action(detail=False, methods=['GET'])
#     def get_author_name(self, request, pk=None):
#         author = Project.objects.get(pk=1)
#         return Response({'name': str(author)})

# class TodoLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 20

# class TodoViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     serializer_class = TodoSerializer
#     queryset = Todo.objects.all()
#     filterset_fields = ['author']
#     pagination_class = TodoLimitOffsetPagination



class ProjectListView(ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectRetrieveView(RetrieveAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def project_api_view(request):
    authors = Project.objects.all()
    serializer = ProjectSerializer(authors, many=True)
    return Response(serializer.data)


def get_view(request):
    todo = todo.objects.get(pk=1)
    serializer = TodoSerializer(todo)
    render = JSONRenderer()
    json_data = render.render(serializer.data)
    return HttpResponse(json_data)

# -----

#  #сюреализатор
# class ProjectSerializer(Serializer):
#
#     # def update(self, instance, validated_data):
#     #     instance.first_name = validated_data.get('first_name', instance.first_name)
#     #     instance.last_name = validated_data.get('last_name', instance.last_name)
#     #     instance.birthday_year = validated_data.get('birthday_year', instance.birthday_year)
#     #     instance.save()
#     #     return instance
#
#     def create(self, validated_data):
#         author = Project(**validated_data)
#         author.save()
#         return author

# class TodoSerializer(Serializer):
#     text = CharField(max_length=64)
#     author = ProjectSerializer()


def get_view2(request):
    #book = Book.objects.get(pk=1)
    #serializer = BookSerializer(book)
    render = JSONRenderer()
    json_data = render.render(serializer.data)
    return HttpResponse(json_data)


    # author = Author.objects.get(pk=1)
    # return render_author(author)


@csrf_exempt
def post_view2(request):
    data = JSONParser().parse(io.BytesIO(request.body))

    if request.method == 'POST':
        serializer = ProjectSerializer(data=data)
    elif request.method == 'PUT':
        author = Project.objects.get(pk=3)
        serializer = ProjectSerializer(author, data=data)
    elif request.method == 'PATCH':
        author = Project.objects.get(pk=3)
        serializer = ProjectSerializer(author, data=data, partial=True)

    if serializer.is_valid():
        print(serializer.validated_data)

        author = serializer.save()
        return render_project(author)
    else:
        return HttpResponseServerError(serializer.errors['non_field_errors'])


