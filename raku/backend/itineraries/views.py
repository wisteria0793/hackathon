from django.shortcuts import render

# Create your views here.
# chat/views.py
from rest_framework.views import APIView
from rest_framework import status


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MessageSerializer
from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings
# client = OpenAI()



class ChatGPTAPIView(APIView):
    
    # openai.api_key = settings.OPENAI_APIKEY
    def post(self, request):
        try:
            # フロントエンドからのデータを取得
            user_input = request.data.get('text', '')

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                # The messages parameter should be an array of objects, each with a role and content
                messages=[
                    {"role": "system", "content": "あなたは高校生です。与えられたテキストに返答して。"},
                    {"role": "user", "content": user_input},
                ],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={"type": "text"},
            )
            # ChatGPTの応答を取得
            chat_response = response.choices[0].message.content

            print(chat_response)

            # 応答を返す
            return Response({'response': chat_response}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def reply_message(request):
    

    
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        user_message = serializer.validated_data['message']
        
        
        
        openai.api_key = settings.OPENAI_APIKEY
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            # The messages parameter should be an array of objects, each with a role and content
            messages=[
                {"role": "system", "content": "あなたは高校生です。与えられたテキストに返答して。"},
                {"role": "user", "content": user_message},
            ],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "text"},

        )

        return Response({'reply': response.choices[0].message.content})
    return Response(serializer.errors, status=400)
