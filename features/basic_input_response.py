import openai
from typing import Optional

def generate_emotional_support(user_input: str, api_key: str) -> str:
    """
    Generate personalized emotional support message using OpenAI API.
    
    Args:
        user_input (str): User's emotional input/description
        api_key (str): OpenAI API key
    
    Returns:
        str: Generated emotional support message
    """
    try:
        # Configure OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Create the prompt for emotional support
        system_prompt = """You are a compassionate AI emotional support companion. Your role is to:
1. Listen empathetically to the user's feelings
2. Provide gentle, supportive responses
3. Offer practical coping strategies when appropriate
4. Maintain a warm, caring tone
5. Remind users that it's okay to feel their emotions
6. Encourage self-care and reaching out to others when needed

Important: Always remind users that you're not a replacement for professional mental health care, especially if they mention serious concerns."""

        user_prompt = f"""Please provide emotional support for someone who shared: "{user_input}"

Respond with empathy, understanding, and gentle guidance. Keep your response under 300 words."""

        # Generate response using OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        # Extract and return the generated message
        support_message = response.choices[0].message.content
        support_message = support_message.strip() if support_message else "Üzgünüm bu sefer destek olamadım."
        return support_message
        
    except openai.AuthenticationError:
        raise Exception("Invalid OpenAI API key. Please check your API key and try again.")
    except openai.RateLimitError:
        raise Exception("Rate limit exceeded. Please wait a moment and try again.")
    except openai.APIError as e:
        raise Exception(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

def validate_user_input(user_input: str) -> tuple[bool, Optional[str]]:
    """
    Validate user input for emotional support generation.
    
    Args:
        user_input (str): User's input to validate
    
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not user_input or not user_input.strip():
        return False, "Lütfen duygularınızı veya düşüncelerinizi paylaşın."
    
    if len(user_input.strip()) < 10:
        return False, "Lütfen nasıl hissettiğiniz hakkında biraz daha detay verin."
    
    if len(user_input) > 1000:
        return False, "Mesajınız oldukça uzun. Lütfen 1000 karakterin altında tutmaya çalışın."
    
    return True, None