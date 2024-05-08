# Async Python client library for AI Horde

## Usage examples:
Here you can find some usage examples of library

### Image generation
```python
import asyncio
from aihorde.client import AIHordeClient
from aihorde import models

API_KEY = '0000000000' # Your API key from aihorde.net/register. You can also use 0000000000.

async def image():
    q = input('Введите запрос: ')
    client = AIHordeClient(API_KEY)
    generation_input = models.GenerationInputStable(
        q,
        models=['Anything v5', 'Anything v3', 'MeinaMix', 'Cetus-Mix', 'Anything Diffusion',
                'AAM XL', 'AlbedoBase XL (SDXL)', 'Animagine XL', 'Anime Illust Diffusion', 'DreamShaper XL',
                'ICBINP XL', 'Juggernaut XL', 'Quiet Goodnight XL', 'Unstable Diffusers XL']
    )
    generations: list[models.GenerationStable] = await client.generate_image(generation_input)
    for generation in generations:
        print(f'{generation.model}: {generation.img}')

asyncio.run(image())
```

### Text generation
```python
import asyncio
from aihorde.client import AIHordeClient
from aihorde import models

API_KEY = '0000000000' # Your API key from aihorde.net/register. You can also use 0000000000.

async def text():
    q = input('Введите запрос: ')
    client = AIHordeClient(API_KEY)
    params = models.ModelGenerationInputKobold(
        stop_sequence=['Human:'],
        max_length=160
    )
    generation_input = models.GenerationInputKobold(
        f' Human: {q}/n AI:',
        params=params,
        models=['koboldcpp/Kunoichi-DPO-v2-7B-Q8_0-imatrix'] # i dont know which models are good for text :D
    )
    results: list[models.GenerationKobold] = await client.generate_text(generation_input)
    for result in results:
        print(result.text.strip())

asyncio.run(text())
```

