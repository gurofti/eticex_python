import base64
import os
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from PIL import Image
import urllib.request
import uuid


def imageConvertBase64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    return image_data


def imageConvert(file, path, width, height):
    file.resize((width, height)).save(path, format='WEBP', quality=100)


@api_view(['POST'])
def uploadUrlImage(request):
    imageUrl = request.data['url']
    key = request.data['key']
    imageTypes = request.data['image_type']

    print("---------")
    basePath = os.getcwd() + "/backend/public/"
    print(f"baspath {basePath}")
    print("---------")
    filePathUUID = key + str(uuid.uuid4())
    items = list()

    # if os.path.isdir(os.getcwd()):
    #     return JsonResponse({'result': 'scc', 'data': filePathUUID})
    # return JsonResponse({'result': 'err', 'data': filePathUUID})


    # Temporary File
    temporary = filePathUUID

    temporaryPNG = (temporary + ".png")
    temporaryWEBP = (temporary + ".webp")

    urllib.request.urlretrieve(imageUrl, temporaryPNG)
    urllib.request.urlretrieve(imageUrl, temporaryWEBP)

    items.append({
        'origin': [
            {
                'png': imageConvertBase64(temporaryPNG),
            },
            {
                'webp': imageConvertBase64(temporaryWEBP),
            }
        ]
    })

    for image in imageTypes:
        path = filePathUUID + "_" + image['name']

        pngPath = (path + ".png")
        imageConvert(Image.open(temporaryPNG), pngPath, image['width'], image['height'])

        webpPath = (path + ".webp")
        imageConvert(Image.open(temporaryWEBP), webpPath, image['width'], image['height'])

        items.append({
            str(image['name']): [
                {'png': imageConvertBase64(pngPath)},
                {'webp': imageConvertBase64(webpPath)}
            ]
        })
        os.remove(pngPath)
        os.remove(webpPath)

    # Temporary File Remove
    os.remove(temporaryPNG)
    os.remove(temporaryWEBP)

    return JsonResponse({"items": items})

    # conn = MysqlConnection()
    # conn.cursor.execute("SELECT * FROM stores WHERE visited = 0 LIMIT 1")
    # resultOne = conn.cursor.fetchone()
    # conn.cursor.execute("SELECT * FROM stores")
    # resultAll = conn.cursor.fetchall()
    # return JsonResponse({"one": resultOne, "all": items})


@api_view(['POST'])
def uploadBinaryImage(request):
    files = request.FILES
    image = files.get("image")

    path = "./public/" + str(image)
    imageConvert(Image.open(image), path, 300, 200)
    return JsonResponse({"data": str(image)})
