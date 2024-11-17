from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
import json
from django.http import JsonResponse
from .models import UserLink, UserProfile
import uuid
# Create your views here.

def home(request):
    return render(request,'index.html')

def create_bio(request):
    return render(request,'create_bio_page.html')

def bio_page(request,id):
    user = UserProfile.objects.filter(id=id).first()
    if not user:
        return render(request,'bio_share_page.html')
    user_links = UserLink.objects.filter(user_profile__id=id)
    return render(request,'bio_share_page.html',{'user':user,'user_links':user_links})


@csrf_exempt
def save_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get("name")
            bio = data.get("bio")
            profile_image_data = data.get("profile_image")
            links = data.get("links", [])
        
            # Create UserProfile instance
            profile = UserProfile.objects.create(name=name, bio=bio)
             
            # Decode and save the profile image
            if profile_image_data:
                format, imgstr = profile_image_data.split(";base64,")
                ext = format.split("/")[-1]
                profile.profile_image.save(
                    f"{profile.name}_profile.{ext}", 
                    ContentFile(base64.b64decode(imgstr))
                )

            # Save links
            for index, link in enumerate(links):
                link_image_data = link.get("image")
                link_url = link.get("url")
                
                if link_image_data:
                    # Generate a unique filename for each link image
                    format, imgstr = link_image_data.split(";base64,")
                    ext = format.split("/")[-1]
                    unique_filename = f"{profile.name}_link_{index}_shsh.{ext}"
                    
                    # Create the link with the image
                    link_obj = UserLink.objects.create(
                        user_profile=profile,
                        link_url=link_url
                    )
                    
                    # Save the link image with the unique filename
                    link_obj.link_image.save(
                        unique_filename,
                        ContentFile(base64.b64decode(imgstr)),
                        save=True
                    )

            return JsonResponse({
                "message": "Profile saved successfully!", 
                "link": f"http://127.0.0.1:8000/bio-page/{profile.id}/"
            })
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
            
    return JsonResponse({"error": "Invalid request method"}, status=405)