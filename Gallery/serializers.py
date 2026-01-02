from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    class Meta():
        fields = ['Username', 'email']



class ReminderSerializer(serializers.Serializer):
    class Meta():
        fields = ['title','date','location','repeat',]
        
    