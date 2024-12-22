import requests

# Django 서버 URL
url = "http://127.0.0.1:8000/api/predict/"  # Django 서버의 추론 API 엔드포인트

# 이미지 파일 경로
image_path = "./dog.jpeg"

def send_image_to_server(image_path):
    try:
        # 이미지 파일 열기
        with open(image_path, "rb") as image_file:
            # HTTP POST 요청으로 이미지 전송
            files = {'image': image_file}
            response = requests.post(url, files=files)

        # 서버 응답 처리
        if response.status_code == 200:
            print("Response from server:", response.json())
        else:
            print(f"Failed to get response. Status code: {response.status_code}")
            print("Error:", response.text)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    send_image_to_server(image_path)