import aiohttp
import asyncio
import uvicorn
import torch
from torchvision import transforms
from torch.autograd import Variable
from pathlib import Path
from PIL import Image
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
import sys

imsize = 224
loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])

def image_loader(image_name):
    """load image, returns cuda tensor"""
    image = Image.open(image_name)
    image = loader(image).float()
    image = Variable(image, requires_grad=True)
    image = image.unsqueeze(0)  
    return image  

#export_file_url = 'https://drive.google.com/uc?export=download&id=1-D_tomTAoQ_wakRPmquwBdChbZzRLg1V'
export_file_name = 'IntelImageClassifier.pt'

classes = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']
path = Path(__file__).parent

print("Path in Server File :", path)

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def setup_model():
    try:
        print("Trying to Load Model")
        model = torch.load(path/export_file_name)
        model.eval()
        print("Model Loaded")
        return model
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_model())]
model = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open(encoding = 'utf-8').read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = image_loader(BytesIO(img_bytes))
    prediction = model(img)
    prediction = classes[prediction.argmax(-1)]
    return JSONResponse({'result': str(prediction)})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=8008, log_level="info")
