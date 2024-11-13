import io
import os
import time
import random
import base64
from PIL import Image
from functools import wraps
from anthropic import Anthropic, InternalServerError, APIError


client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

def retry_with_exponential_backoff(
    max_retries=5,
    initial_delay=1,
    max_delay=32,
    exponential_base=2,
    jitter=True
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay

            while True:
                try:
                    return func(*args, **kwargs)
                except InternalServerError as e:
                    if e.status_code != 529:  # If it's not an overloaded error
                        raise
                    
                    retries += 1
                    if retries > max_retries:
                        raise Exception(
                            f"Maximum retries ({max_retries}) exceeded. Last error: {str(e)}"
                        )

                    # Calculate delay with exponential backoff
                    delay = min(max_delay, initial_delay * (exponential_base ** (retries - 1)))
                    
                    # Add jitter if enabled
                    if jitter:
                        delay = delay * (1 + random.random() * 0.1)  # 10% jitter

                    print(f"Attempt {retries} failed. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                except Exception as e:
                    # Handle other exceptions if needed
                    raise

        return wrapper
    return decorator

@retry_with_exponential_backoff(
    max_retries=5,
    initial_delay=1,
    max_delay=32
)
def scraping_image(image_data):

    image_data = webp_to_jpeg_base64(image_data)

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": """Devolve um json dos produtos com seu preço (preco é igual a preço), ofertas se tem,
                                   gramagem (com unidade de medida), a categoria do produto e a data de inicio(formato: yyyy-mm-dd) e fim da oferta (formato: yyyy-mm-dd).
                                   Apaga os encabeçados das respostas. Formato do json: 
                                   [{"nome": valor, "preco": valor, "oferta": valor, "categoria": valor, "data_ini": valor, "data_fim": valor}, ...]""",
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
            }
        ]
    )
    return [block.text for block in message.content]


def webp_to_jpeg_base64(webp_file_path):
    # Open the WebP image
    with Image.open(webp_file_path) as img:
        # Convert to RGB mode (in case of transparency)
        img = img.convert('RGB')
        
        # Save as JPEG to a bytes buffer
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        
        # Get the byte data and encode to base64
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_str

@retry_with_exponential_backoff(
    max_retries=5,
    initial_delay=1,
    max_delay=32
)
def separate_product_and_brand(text_list):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text":"<produtos>" + str(text_list) + "</produtos>",
                        "cache_control": {"type": "ephemeral"}
                     },
                     {
                        "type": "text",
                        "text":  """ Devolve uma tupla por cada produto onde fica separado
                               o nome do produto, sem o gramagem e o nome da marca.
                               A resposta tem que ser uma lista de tuplas sem enumciado, nem observações,
                               no formato: [('nome do produto', 'marca do produto'), ...]"""
                     }
                ]
                   
            }
        ]
    )
    # print(f"Cached API call input tokens: {message.usage.input_tokens}")
    # print(f"Cached API call output tokens: {message.usage.output_tokens}")
    return [block.text for block in message.content]

if __name__ == '__main__':
    # image_data = "imagens_carrefour/f7c70ddbe638702332991406db2e24b87d29d926-0008.jpeg"
    # image_type = "image/jpeg"

    # print(scraping_image(image_data=image_data, image_type=image_type))

    text_list = ['VINHO CONCHAYTORO 750ML RESERVADO', 'Pão de Queijo Massa Leve Forno de Minas',
                 'Mortadela Defumada Ouro Perdigão', 'Limão siciliano', 'FEIJÃO CARIOCA TIPO 1 DELÍCIA']
    print(separate_product_and_brand(text_list=text_list))