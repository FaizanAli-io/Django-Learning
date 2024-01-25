from rest_framework import generics, mixins, permissions, authentication

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsStaffEditorPermission
from api.authentication import TokenAuthentication

# For Function Based View
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [
        TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    permission_classes = [
        permissions.IsAdminUser,
        IsStaffEditorPermission,
    ]

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content')
        if content is None:
            content = "created using a generic view"
        serializer.save(content=content)


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


product_update_view = ProductUpdateAPIView.as_view()


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


product_delete_view = ProductDeleteAPIView.as_view()


# Alternative Function Based View
@api_view(["GET", "POST"])
def all_function_view(request, pk=None, *args, **kwargs):
    if request.method == "GET":
        if pk is None:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)
        obj = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(obj, many=False)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            content = serializer.validated_data.get('content')
            if content is None:
                content = "created using a functional view"
            serializer.save(content=content)
        return Response(serializer.data)


# Product Mixin View
class ProductMixinView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content')
        if content is None:
            content = "created using a model mixin view"
        serializer.save(content=content)


product_mixin_view = ProductMixinView.as_view()


@api_view(["GET"])
def clean_product_database(request, *args, **kwargs):
    Product.objects.all().delete()
    return Response(200)
