import openai
from dotenv import load_dotenv
import pandas as pd

_ = load_dotenv()
client = openai.OpenAI()


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
    '''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    message_response = response.choices[0].message.content

    return message_response


def outfit_helper_db(user_input: str):
    file_path = '/Users/andresgonzalez/Outfit/test.xlsx'
    df = pd.read_excel(file_path)
    data_as_text = df.to_string(index=False)

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
    for giving the response to the user you have to use the information from the following database {data_as_text}
    '''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    message_response = response.choices[0].message.content

    return message_response



if __name__ == '__main__':
    user_input = "i have a pink oversize t-shirt and a black sneakers"
    print(outfit_helper_db(user_input))

