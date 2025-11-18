"""
Topic classification using PydanticAI
"""
from pydantic_ai import Agent
from typing import List

from dotenv import load_dotenv

load_dotenv()


topic_classifier = Agent(
    "openai:gpt-4o-mini",
    output_type=list[str],
    system_prompt="Analyze personal reflections and identify 2-3 key topics to describe the following reflections",
)


async def classify_reflection_topics(
    title: str, text: str, existing_topics: List[str]
) -> List[str]:
    """Classify topics for a reflection"""
    user_prompt = f"""
    Given the following reflection:
    
    Title: {title}
    Text: {text}
    
    Please use one of the following topics if applicable or create a new one(s) otherwise. 
    Please be conservative and don't use the topic unless it would be deemed a very intuitive match by any user.
    {', '.join(existing_topics)}
    """

    result = await topic_classifier.run(user_prompt)
    return result.output