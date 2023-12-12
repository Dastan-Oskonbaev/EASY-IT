from decouple import config as env_config
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai

openai.api_key = env_config('YOUR_API_KEY')


class ChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')

        if not text:
            return Response({'error': 'Текст не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)

        response_text = self.generate_response(text)
        if response_text:
            return Response({'response': response_text}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ошибка при генерации ответа.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_response(self, text):
        openai.api_key = env_config('YOUR_API_KEY')

        response = openai.Completion.create(
            prompt=text,
            engine='text-davinci-003',
            max_tokens=100,
            temperature=0.5,
            n=1,
            stop=None,
            timeout=15,
        )
        if response and response.choices:
            return response.choices[0].text.strip()
        else:
            return None

