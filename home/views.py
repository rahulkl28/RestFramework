from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

@api_view(['GET'])
def get_book(request):
   book_objs = Book.objects.all()
   serializer = BookSerializer(book_objs, many = True)
   return Response({'status': 200, 'payload': serializer.data})



class RegisterUser(APIView):
   def post(self, request):
      serializer = UserSerializer(data = request.data)

      if not serializer.is_valid():
         print(serializer.errors)
         return Response({'status': 403, 'errors': serializer.errors, 'message': 'Invalid Credentials'})

      serializer.save()
      
      user = User.objects.get(username = serializer.data['username'])
      refresh = RefreshToken.for_user(user)


      return Response({'status': 200, 'payload': serializer.data, 'refresh': str(refresh),'access': str(refresh.access_token), 'message': "Your token is generated"})

class StudentAPI(APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsAuthenticated]
   throttle_classes = [UserRateThrottle]


   def get(self, request):
       student_objs = Student.objects.all()
       serializer = StudentSerializer(student_objs, many = True)
         
       return Response({'status' : 200, 'payload': serializer.data})

   def post(self, request):
      serializer = StudentSerializer(data = request.data)

      if not serializer.is_valid():
            print(serializer.errors)
            return Response({'status': 403, 'error': serializer.errors, 'message': 'Something went wrong'})

      serializer.save()

      return Response({'status':200, 'payload': serializer.data, 'message': 'you data is posted'})


   def put(self, request):
      try: 
         student_obj = Student.objects.get(id = request.data['id'])

         serializer = StudentSerializer(student_obj, data = request.data)

         if not serializer.is_valid():
            print(serializer.errors)
            return Response({'status': 403, 'error': serializer.errors, 'message': 'Something went wrong'})

         serializer.save()

         return Response({'status':200, 'payload': serializer.data, 'message': 'you data is updated'})

      except Exception as e:
         print(e)
         return Response({'status' : 403, 'message' : 'invalid id'})

   def patch(self, request):
      try: 
         student_obj = Student.objects.get(id = request.data['id'])

         serializer = StudentSerializer(student_obj, data = request.data, partial = True)

         if not serializer.is_valid():
            print(serializer.errors)
            return Response({'status': 403, 'error': serializer.errors, 'message': 'Something went wrong'})

         serializer.save()

         return Response({'status':200, 'payload': serializer.data, 'message': 'you data is updated'})

      except Exception as e:
         print(e)
         return Response({'status' : 403, 'message' : 'invalid id'})


   def delete(self, request):
      try:
         id = request.GET.get('id')
         student_obj = Student.objects.get(id = id)
         student_obj.delete() 
         return Response({'status': 200, 'message': 'deleted'})

      except Exception as e:
         print(e)
         return Response({'status' : 403, 'message' : 'invalid id'})


#Generic Views

class StudentGeneric(generics.ListAPIView, generics.CreateAPIView):
   permission_classes =  [IsAuthenticated]
   queryset = Student.objects.all()
   serializer_class = StudentSerializer


class StudentGeneric1(generics.UpdateAPIView, generics.DestroyAPIView):
      queryset = Student.objects.all()
      serializer_class = StudentSerializer
      lookup_field = "id"


#With The Help of Serialization method only

# @api_view(['GET'])
# def home(request):
#    student_objs = Student.objects.all()
#    serializer = StudentSerializer(student_objs, many = True)
    
#    return Response({'status' : 200, 'payload': serializer.data})


# @api_view([ 'POST'])
# def post_student(request):
#    serializer = StudentSerializer(data = request.data)

#    if request.data['age'] < '18':
#       return Response({'status': 403, 'message': 'age must be > 18'})

#    if not serializer.is_valid():
#       print(serializer.errors)
#       return Response({'status': 403, 'error': serializer.errors, 'message': 'Something went wrong'})

#    serializer.save()

#    return Response({'status':200, 'payload': serializer.data, 'message': 'you data is posted'})


# @api_view(['PUT'])
# def update_student(request, id):
#    try: 
#       student_obj = Student.objects.get(id = id)

#       serializer = StudentSerializer(student_obj, data = request.data, partial = True)
#       if not serializer.is_valid():
#          print(serializer.errors)
#          return Response({'status': 403, 'error': serializer.errors, 'message': 'Something went wrong'})

#       serializer.save()

#       return Response({'status':200, 'payload': serializer.data, 'message': 'you data is updated'})

#    except Exception as e:
#       print(e)
#       return Response({'status' : 403, 'message' : 'invalid id'})


# @api_view(['DELETE'])
# def delete_student(request, id):
#    try:

#       student_obj = Student.objects.get(id = id)
#       student_obj.delete() 
#       return Response({'status': 200, 'message': 'deleted'})

#    except Exception as e:
#       print(e)
#       return Response({'status' : 403, 'message' : 'invalid id'})


