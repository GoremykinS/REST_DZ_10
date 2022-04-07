import io

from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import renderer_classes, api_view, action
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer, CharField, IntegerField
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.mixins import *
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, BasePermission

from .serializers import AuthorModelSerializer, BookModelSerializer, BioModelSerializer, AuthorSerializer
from .models import Author, Book, Bio


class IsSuperAdminUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


# client -> [url] -> [view] -> [serializer] -> [model]

class AuthorModelViewSet(ModelViewSet):
    # renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    permission_classes = [IsSuperAdminUser]

    serializer_class = AuthorModelSerializer
    queryset = Author.objects.all()


class BioViewSet(ModelViewSet):
    serializer_class = BioModelSerializer
    queryset = Bio.objects.all()


class BookViewSet(ModelViewSet):
    serializer_class = BookModelSerializer
    queryset = Book.objects.all()


class AuthorView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


class AuthorLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2


class AuthorViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    filterset_fields = ['first_name', 'last_name']
    pagination_class = AuthorLimitOffsetPagination

    # http://127.0.0.1:8000/api/authors/get_author_name/

    @action(detail=False, methods=['GET'])
    def get_author_name(self, request, pk=None):
        author = Author.objects.get(pk=1)
        return Response({'name': str(author)})

    # http://127.0.0.1:8000/api/authors/?first_name=Федор&last_name=Пушкин
    # def get_queryset(self):
    #     queryset = Author.objects.all()
    #     # first_name = None
    #     # first_name = self.kwargs['first_name']
    #     first_name = self.request.query_params.get('first_name', None)
    #     if first_name:
    #         queryset = queryset.filter(first_name=first_name)
    #     last_name = self.request.query_params.get('last_name', None)
    #     if last_name:
    #         queryset = queryset.filter(last_name=last_name)
    #     return queryset


class AuthorListView(ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class AuthorRetrieveView(RetrieveAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()



@api_view(['GET'])
@renderer_classes([JSONRenderer])
def author_api_view(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


def get_view(request):
    book = Book.objects.get(pk=1)
    serializer = BookSerializer(book)
    render = JSONRenderer()
    json_data = render.render(serializer.data)
    return HttpResponse(json_data)


    # author = Author.objects.get(pk=1)
    # return render_author(author)


@csrf_exempt
def post_view(request):
    data = JSONParser().parse(io.BytesIO(request.body))

    if request.method == 'POST':
        serializer = AuthorSerializer(data=data)
    elif request.method == 'PUT':
        author = Author.objects.get(pk=3)
        serializer = AuthorSerializer(author, data=data)
    elif request.method == 'PATCH':
        author = Author.objects.get(pk=3)
        serializer = AuthorSerializer(author, data=data, partial=True)

    if serializer.is_valid():
        print(serializer.validated_data)

        author = serializer.save()
        return render_author(author)
    else:
        return HttpResponseServerError(serializer.errors['non_field_errors'])


def render_author(author):
    serializer = AuthorSerializer(author)
    render = JSONRenderer()
    json_data = render.render(serializer.data)
    return HttpResponse(json_data)
