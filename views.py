from urllib import response
from rest_framework import viewsets
from .models import MediaFile, Category
from .serializers import MediaFileSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from .tasks import extract_metadata_task
from rest_framework.response import Response
from rest_framework import status


# new file added
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
# END


class MediaFileViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [IsAuthenticated]


    # NEW
    def get_queryset(self):
        return MediaFile.objects.filter(owner=self.request.user)
    # END


    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data["size"] = uploaded_file.size

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save(owner=request.user)
        extract_metadata_task.delay(instance.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    # OLD
    # def perform_create(self, serializer):
    #     # This method can be optional or kept as a fallback
    #     instance = serializer.save(owner=self.request.user)
    #     extract_metadata_task.delay(instance.id)
    # END




    #     # Launch metadata task
    #     extract_metadata_task.delay(instance.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



# def perform_create(self, serializer):
#     uploaded_file = self.request.FILES.get("file")
#     size = uploaded_file.size if uploaded_file else 0
#     instance = serializer.save(owner=self.request.user, size=size)
#     extract_metadata_task.delay(instance.id)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
