#TODO: change in production
from authors_api.settings.local import DEFAULT_FROM_EMAIL

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.parsers import MultiPartParser

from .exceptions import CantFollowYourself
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer, FollowingSerializer


User = get_user_model()

#get all user profiles
class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = (ProfilesJSONRenderer,)

#retrieve single user profile:
class ProfileAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_queryset(self):
        queryset = Profile.objects.select_related("user") #fetch related objects along with the main objects
        return queryset
    
    #to get specific user profile pbject
    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile
    
class UpdateProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes=[MultiPartParser]
    renderer_classes = [ProfilesJSONRenderer]

    def get_object(self):
        profile = self.request.user.profile
        return profile
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


#return list of all profiles following user with specified id:
class FollowerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)
            formatted_response = {
                "status_code":status.HTTP_200_OK,
                "followers_count":follower_profiles.count(),
                "followers":serializer.data
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=404)
        
#retrieve all users a specified user is following:
class FollowingListView(APIView):
    def get(self, request, user_id, format=None):
        try:
            profile = Profile.objects.get(user__id=user_id)
            following_profiles = profile.following.all()
            users = [p.user for p in following_profiles ] 
            serializer = FollowingSerializer(users, may=True)
            formatted_response = {
                "status_code":status.HTTP_200_OK,
                "following_count":following_profiles.count(),
                "users_i_follow":serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=404)
        
#for users to follow each other:
class FollowAPIView(APIView):
    def post(self, request, user_id, format=None):
        try:
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id=user_id)

            #can't follow yourself:
            if profile == follower:
                raise CantFollowYourself
            
            #check if use is already following:
            if user_profile.check_following(profile):
               formatted_response = {
                "status_code":status.HTTP_400_BAD_REQUEST,
                "message": f"You are already following {profile.user.first_name} {profile.user.last_name}"
            } 
               return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
            
            #follow profile
            user_profile.follow()

            #send email
            subject = "You have a new follower"
            message=f"Hi there, {profile.user.first_name}!!, the user {user_profile.first_name} {user_profile.last_name} is now following you"
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [profile.user.email]
            send_mail(subject, message, from_email, recipient_list,)
            return Response({
                "status_code":status.HTTP_200_OK,
                "message":f"You are now following {profile.user.first_name} {profile.user.last_name}",
            },)
        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile that doesn't exist")
        

#unfollow other users:
