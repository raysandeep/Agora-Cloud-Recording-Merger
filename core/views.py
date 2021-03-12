from django.shortcuts import render
from .utils import Utils
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView



def index(request):
    return render(request,"index.html")



class AgoraAPI(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        channel_id = request.data.get("channel_id")
        if channel_id is None:
            return Response({
                "message":"Invalid Request"
            },status=400)
        merge_mode = request.data.get("merge_mode",settings.AGORA_DEFAULT_MERGE_MODE)
        fps = request.data.get("fps",settings.AGORA_DEFAULT_FPS)
        width = request.data.get("width",settings.AGORA_DEFAULT_WIDTH)
        height = request.data.get("height",settings.AGORA_DEFAULT_HEIGHT)
        if type(merge_mode) != int or type(fps) != int or type(width)!=int or type(height)!=int:
            return Response({
                "message":"Invalid Request"
            },status=400)
        output = Utils.process(channel_id,{
            "merge_mode":merge_mode,
            "fps":fps,
            "width":width,
            "height":height,
        })
        print(output)
        return Response(output,status=200)