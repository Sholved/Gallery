from supabase import create_client
from django.conf import settings

supabase = create_client(settings.SUPABASE_URL,
                         settings.SUPABASE_SERVICE_ROLE_KEY)

def upload_image(file, user, image_id):
    path = f"images/{user.id}/{image_id}.jpg"
    supabase.storage.from_("images").upload(path,
            file.read(),
            {"content-type": file.content_type}
    )
    
    return path

def delete_image(path:str):
        supabase.storage.from_("images").remove([path])
        
        