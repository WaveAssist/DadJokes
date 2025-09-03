from openai import OpenAI
import waveassist
import json

waveassist.init()


print("Generating AI joke")

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=waveassist.fetch_data("open_router_key"),
)

def extract_json(content):
    # Try direct JSON parsing first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    
    # Try extracting from ```json ... ``` blocks
    start = content.find("```json")
    if start != -1:
        end = content.find("```", start + 6)
        if end != -1:
            try:
                return json.loads(content[start + 7:end].strip())
            except json.JSONDecodeError:
                pass
    
    # Fallback to regex pattern matching
    import re
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    
    return None

# JSON prompt for joke generation
prompt = """Generate a unique new funny DAD joke, and return it in this exact JSON format:
{
    "joke": "your dad joke text here",
    "category": "dad_joke",
}

Return only the JSON, no other text or formatting."""

try:
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3.1",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7
    )
    
    content = response.choices[0].message.content.strip()
    joke_data = extract_json(content)
    
    if joke_data and 'joke' in joke_data:
        joke = joke_data['joke']
        waveassist.store_data('joke', joke)
        print(f"Generated joke: {joke}")
    else:
        # Fallback if JSON parsing fails
        joke = "Why did the AI go to therapy? It had too many processing issues!"
        waveassist.store_data('joke', joke)
        print(f"JSON parsing failed, using fallback joke: {joke}")
    
except Exception as e:
    print(f"Error generating joke: {e}")
    joke = "Why did the AI go to therapy? It had too many processing issues!"
    waveassist.store_data('joke', joke)