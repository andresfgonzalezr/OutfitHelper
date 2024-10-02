import openai
from dotenv import load_dotenv
import pandas as pd
from PIL import Image
import anthropic


_ = load_dotenv()
clientOAI = openai.OpenAI()
clientA = anthropic.Anthropic()


def outfit_helper(user_input: str):
    user_prompt = f'''you are a fashion expert, you have to give advice to the user, in the user_input you are going to find a garment, you have to define what it is
    e.g t-shirt, pants, shoes or other type
    also extract the color and the fit of the garment
    e.g black oversize t-shirt, blue jean baggy pants.
    you can receive more than one type of garment and also include it and give the advice based on both of them
    e.g black oversize t-shirt, blue jean baggy pants.
    then give an advice to the user for the rest of the garment that are missing.
    e.g a blue oversize t-shirt, could combine with a black jean baggy pants, and white sneakers.
    the user_input is the next one: {user_input}
    also give me a list of every garment that you include in the response but also the response
    examples for your answer are the following, also if you have another one that can adjust to the outfit you can use it
    t-shirts: crew neck t-shirt, v-neck t-shirt, tank top, oversize t-shirt, turtleneck t-shirt, ringer t-shirt, raglan sleeve t-shirt, crop top t-shirt, henley t-shirt, slim fit t-shirt, sleeveless t-shirt, graphic t-shirt, long-sleeve t-shirt, polo t-shirt.
    pants: Jeans, Dress Pants, Chinos, Joggers, Cargo Pants, Shorts, Culotte Pants, Palazzo Pants, Skinny Pants, Slim Fit Pants, Corduroy Pants, Leather Pants, Wide-Leg Pants, Capri Pants, Bootcut Pants, Tapered Pants, Suit Pants, Paper Bag Pants, Leggings, Harem Pants.
    jacket: Denim Jacket, Bomber Jacket, Leather Jacket, Blazer, Hoodie, Parka, Peacoat, Trench Coat, Windbreaker, Puffer Jacket, Utility Jacket, Varsity Jacket, Jean Jacket, Faux Fur Jacket, Quilted Jacket, Overcoat, Anorak, Cardigan, Biker Jacket, Track Jacket.
    shoes: Sneakers, Loafers, Oxfords, Ankle Boots, Sandals, Heels, Wedges, Flats, Chelsea Boots, Derby Shoes, Brogues, Espadrilles, Flip-Flops, Chukka Boots, Combat Boots, Slippers, Monk Strap Shoes, Platform Shoes, Mary Janes, Moccasins.
    '''

    response = clientOAI.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    message_response = response.choices[0].message.content

    return message_response


def extract_image(image_path):
    img = Image.open(image_path)

    user_prompt = f'''from the image {img} extract the color and the fit of the garments in there and return me that information in a json.
    also specify the type of garment, and in the json specify the information with it
    if in the image there is no information don´t fill
    '''

    message = clientA.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system="you are a fashion expert.",
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    message_response = message.text
    return message_response


def outfit_helper_db(user_input: str):
    file_path = '/Users/andresgonzalez/Outfit/test.xlsx'
    df = pd.read_excel(file_path)

    json_data = df.to_json(orient='records', indent=4)
    with open('archivo.json', 'w') as json_file:
        json_file.write(json_data)

    user_prompt = f'''you are a fashion expert, you have to give advice to the user, in the user_input you are going to find a garment, you have to define what it is
    e.g t-shirt, pants, shoes or other type
    also extract the color and the fit of the garment
    e.g black oversize t-shirt, blue jean baggy pants.
    you can receive more than one type of garment and also include it and give the advice based on both of them
    e.g black oversize t-shirt, blue jean baggy pants.
    then give an advice to the user for the rest of the garment that are missing.
    e.g a blue oversize t-shirt, could combine with a black jean baggy pants, and white sneakers.
    only give one option for each type of garment.
    e.g for a white t-shirt, a black baggy pants and green sneakers
    the user_input is the next one: {user_input}
    also give me a list of every garment that you include in the response but also the response
    for giving the response to the user you have to use the information from the following json {json_data}
    for the advices with the information you give be more specific.
    examples for your answer are the following, also if you have another one that can adjust to the outfit you can use it
    t-shirts: crew neck t-shirt, v-neck t-shirt, tank top, oversize t-shirt, turtleneck t-shirt, ringer t-shirt, raglan sleeve t-shirt, crop top t-shirt, henley t-shirt, slim fit t-shirt, sleeveless t-shirt, graphic t-shirt, long-sleeve t-shirt, polo t-shirt.
    pants: Jeans, Dress Pants, Chinos, Joggers, Cargo Pants, Shorts, Culotte Pants, Palazzo Pants, Skinny Pants, Slim Fit Pants, Corduroy Pants, Leather Pants, Wide-Leg Pants, Capri Pants, Bootcut Pants, Tapered Pants, Suit Pants, Paper Bag Pants, Leggings, Harem Pants.
    jacket: Denim Jacket, Bomber Jacket, Leather Jacket, Blazer, Hoodie, Parka, Peacoat, Trench Coat, Windbreaker, Puffer Jacket, Utility Jacket, Varsity Jacket, Jean Jacket, Faux Fur Jacket, Quilted Jacket, Overcoat, Anorak, Cardigan, Biker Jacket, Track Jacket.
    shoes: Sneakers, Loafers, Oxfords, Ankle Boots, Sandals, Heels, Wedges, Flats, Chelsea Boots, Derby Shoes, Brogues, Espadrilles, Flip-Flops, Chukka Boots, Combat Boots, Slippers, Monk Strap Shoes, Platform Shoes, Mary Janes, Moccasins.
    '''

    response = clientOAI.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    message_response = response.choices[0].message.content

    return message_response


if __name__ == '__main__':
    image_path = '/Users/andresgonzalez/Outfit/WhatsApp Image 2024-09-24 at 12.30.19 PM.jpeg'
    print(extract_image(image_path))
    # user_input = "i have a black shirt"
    # print(outfit_helper_db(user_input))

