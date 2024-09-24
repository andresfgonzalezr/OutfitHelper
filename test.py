import openai
from dotenv import load_dotenv


_ = load_dotenv()
client = openai.OpenAI()


def outfit_helper(user_input: str):
    user_prompt = f'''you are a fashion expert, you have to give advice to the user, in the user_input you are going to find a garment, you have to define what it is
    e.g t-shirt, pants, shoes or other type
    also extract the color and the fit of the garment
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


if __name__ == '__main__':
    user_input = "i have a pink oversize t-shirt"
    print(outfit_helper(user_input))



