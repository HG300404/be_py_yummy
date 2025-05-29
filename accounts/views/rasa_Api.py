import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RasaChatbot(APIView):
    def post(self, request):
        message = request.data.get("message", "")

        if message:
            try:
                # Địa chỉ của REST API Rasa
                rasa_url = "http://localhost:5005/webhooks/rest/webhook"  # Đảm bảo cổng đúng

                # Gửi yêu cầu đến REST API của Rasa
                response = requests.post(rasa_url, json={"message": message})

                if response.status_code == 200:
                    return Response(response.json(), status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Error from Rasa API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except requests.exceptions.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)
# import subprocess
# import os
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class RasaChatbot(APIView):
#     def post(self, request):
#         message = request.data.get("message", "")
        
#         if message:
#             try:
#                 # Đảm bảo sử dụng đường dẫn đúng tới tệp thực thi của Rasa
#                 rasa_path = "C:\\Users\\dungh\\my-rasa-assistant\\venv\\Scripts\\rasa.exe"  # Cập nhật đường dẫn chính xác

#                 # Sử dụng subprocess.Popen để tương tác với Rasa Shell
#                 process = subprocess.Popen(
#                     [rasa_path, 'shell', '--debug'],  # Lệnh Rasa shell
#                     stdin=subprocess.PIPE,  # Để gửi dữ liệu tới stdin của Rasa
#                     stdout=subprocess.PIPE,  # Để lấy dữ liệu trả về từ stdout
#                     stderr=subprocess.PIPE,  # Để lấy lỗi nếu có
#                     text=True
#                 )

#                 # Gửi tin nhắn đến stdin của Rasa Shell
#                 stdout, stderr = process.communicate(input=message + "\n")  # Tin nhắn gửi vào Rasa Shell

#                 if stderr:
#                     return Response({"error": stderr}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
#                 # Trả về kết quả trả về từ Rasa
#                 return Response({"response": stdout}, status=status.HTTP_200_OK)

#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response({"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)
