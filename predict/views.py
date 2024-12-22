import io
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from torchvision import models, transforms
from PIL import Image
from django.conf import settings

# ImageNet 분류 ID와 ImageNet 분류명 로드
with open(settings.BASE_DIR / 'imagenet_class_index.json', 'r', encoding='utf-8') as f:
    imagenet_class_index = json.load(f)

# Pretrained 모델 로드 및 eval 모드 설정
model = models.densenet121(pretrained=True)
model.eval()


def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


@csrf_exempt
def predict(request):
    if request.method == 'POST':
        file = request.FILES.get('image')
        if not file:
            return JsonResponse({'error': 'No image provided'}, status=400)

        try:
            img_bytes = file.read()
            class_id, class_name = get_prediction(image_bytes=img_bytes)
            response = {
                'class_id': class_id,
                'class_name': class_name,
                'answer': f"이 동물은 {class_name} 입니다"
            }
            return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)