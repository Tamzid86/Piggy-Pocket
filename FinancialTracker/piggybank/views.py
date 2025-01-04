import json
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
import jwt
from .models import Budget, Category, Profile, TransactionHistory, FutureTransaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes



def home(request):
    return HttpResponse("hello world")

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateProfile(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Authentication required"}, status=401)

        user = request.user
        username=user.username
        email=user.email

        data = json.loads(request.body)

        profile, created = Profile.objects.update_or_create(
            user=user,  
            defaults={
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'address': data.get('address'),
                'bio': data.get('bio'),
                'username':username,
                'email':email
                
            }
        )

        if created:
            return JsonResponse({"message": "Profile created successfully"}, status=201)
        else:
            return JsonResponse({"message": "Profile updated successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"message": f"Internal server error: {str(e)}"}, status=500)
    
    
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message":"Authentication required"})
        
        user=request.user
        
        try:
            profile=Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return JsonResponse({"message":"This profile does not exists"}, status=404)
        
        profile_data = {
            "first_name":profile.first_name,
            "last_name":profile.last_name,
            "address":profile.address,
            "bio":profile.bio,
            "username":profile.username,
            "email":profile.email
        }
        
        return JsonResponse(profile_data, status=200)

    except Exception as e:
        return JsonResponse({"message": f"Internal server error: {str(e)}"}, status=500)
    


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddTransactions(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Authentication required"}, status=401)

        user = request.user

        data = json.loads(request.body)

        amount = data.get('amount')
        description = data.get('description')
        date = data.get('date')
        category = data.get('category')

        transaction = TransactionHistory.objects.create(
            user=user,
            amount=amount,
            description=description,
            date=date,
            category=Category.objects.get(category_name=category)
        )

        return JsonResponse({"message": "Transaction added successfully"}, status=201)

    except Exception as e:
        return JsonResponse({"message": f"Internal server error: {str(e)}"}, status=500)  



@csrf_exempt
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
def AddCategory(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Authentication required"}, status=401)
        

        data = json.loads(request.body)

        category = data.get('category_name')
        if category is None:
            raise ValueError("category_name cannot be null")

        category = Category.objects.create(
            category_name=category
        )

        return JsonResponse({"message": "Category added successfully"}, status=201)

    except Exception as e:
        return JsonResponse({"message": f"Internal server error: {str(e)}"}, status=500)
    
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddFutureTransaction(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Authentication required"}, status=401)

        user = request.user

        data = json.loads(request.body)

        amount = data.get('amount')
        description = data.get('description')
        date = data.get('date')
        category = data.get('category')
        execute_date = data.get('execute_date')

        transaction = FutureTransaction.objects.create(
            user=user,
            amount=amount,
            description=description,
            date=date,
            category=Category.objects.get(category_name=category),
            execute_date=execute_date
        )

        return JsonResponse({"message": "Future transaction added successfully"}, status=201)

    except Exception as e:
        return JsonResponse({"message": f"Internal server error: {str(e)}"}, status=500)
    
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_budget(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Authentication required"}, status=401)

        user = request.user

        data = json.loads(request.body)

        amount = data.get('amount')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        budget, created = Budget.objects.update_or_create(
            user=user, 
            start_date=start_date,  
            defaults={
                'amount': amount,
                'end_date': end_date
            }
        )

        if created:
            return JsonResponse({"message": "Budget created successfully"}, status=201)
        else:
            return JsonResponse({"message": "Budget updated successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"message": f"Internal server error: {str(e)}"}, status=500)
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_budget(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Authentication required"}, status=401)

        user = request.user

        data = json.loads(request.body)

        amount = data.get('amount')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        budget = Budget.objects.get(user=user, start_date=start_date, end_date=end_date)
        budget.amount = amount
        budget.save()

        return JsonResponse({"message": "Budget updated successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"message": f"Internal server error: {str(e)}"}, status=500)
    
    
