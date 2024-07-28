# Create your views here.
import base64
import os
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blog import models as blogmodels
import uuid
from login import views as loginviews
from django.conf import settings

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog(request):
    try:
        title = request.data.get('title')
        content = request.data.get('content')
        if(title == '' or content == ''):
            return Response({'error': 'All fields are required'}, status=400)
        image_objs = request.FILES.getlist('images')
        image_paths = []
        for image in image_objs:
            image_name = str(uuid.uuid4()) + '.' + image.name.split('.')[-1]
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            image_paths.append(image_path)
        user = request.user
        blogmodels.Blog.objects.create(title=title, content=content, user=user,img_path=image_paths)
        return Response({'message': 'Blog created successfully'}, status=200)
    except Exception as e:
        return Response({'error': 'Error creating blog','description':str(e)}, status=400)
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_blog(request):
    if(len(request.data) != 0 ):
        try:
            user_info = request.data.get('userId')
            blogs = blogmodels.Blog.objects.filter(user=user_info)
            blog_data = []
            for blog in blogs:
                decoded_images = []
                for imagePath in blog.img_path:
                    try:
                        with open(imagePath, "rb") as image_file:
                            image_name = os.path.basename(imagePath)
                            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                            mime_type = f"data:image/{image_name.split('.')[-1]};base64,"
                            decoded_images.append(mime_type + encoded_string)
                    except FileNotFoundError:
                        return Response({'error': 'Image not found'}, status=400)
                blog_data.append({
                    'title': blog.title,
                    'content': blog.content,
                    'user': blog.user.username,
                    'images': decoded_images,
                    'created_at': blog.created_at,
                    'updated_at': blog.updated_at
                })
            return Response(blog_data, status=200)
        except Exception as e:
            return Response({'error': 'Error fetching blogs','description':str(e)}, status=400) 
    else:
        try:
            user_info = request.user
            blogs = blogmodels.Blog.objects.filter(user=user_info)
            blog_data = []
            for blog in blogs:
                decoded_images = []
                for imagePath in blog.img_path:
                    try:
                        with open(imagePath, "rb") as image_file:
                            image_name = os.path.basename(imagePath)
                            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                            mime_type = f"data:image/{image_name.split('.')[-1]};base64,"
                            decoded_images.append(mime_type + encoded_string)
                    except FileNotFoundError:
                        return Response({'error': 'Image not found'}, status=400)
                blog_data.append({
                    'title': blog.title,
                    'content': blog.content,
                    'user': blog.user.username,
                    'images': decoded_images,
                    'created_at': blog.created_at,
                    'updated_at': blog.updated_at
                })
            return Response(blog_data, status=200)
        except Exception as e:
            return Response({'error': 'Error fetching blogs','description':str(e)}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_blog(request):
    try:
        blog_id = request.data.get('blog_id')
        title = request.data.get('title')
        content = request.data.get('content')
        image_objs = request.FILES.getlist('image')
        image_paths = []
        for image in image_objs:
            image_name = str(uuid.uuid4()) + '.' + image.name.split('.')[-1]
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            image_paths.append(image_path)
        blog = blogmodels.Blog.objects.get(id=blog_id)
        blog.title = title
        blog.content = content
        blog.img_objec = image_paths
        blog.save()
        return Response({'message': 'Blog updated successfully'}, status=200)
    except Exception as e:
        return Response({'error': 'Error updating blog','description':str(e)}, status=400)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blog(request):
    try:
        blog_id = request.data.get('blog_id')
        blog = blogmodels.Blog.objects.get(id=blog_id)
        blog.delete()
        return Response({'message': 'Blog deleted successfully'}, status=200)
    except Exception as e:
        return Response({'error': 'Error deleting blog','description':str(e)}, status=400)