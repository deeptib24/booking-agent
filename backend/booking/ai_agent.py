import os
from openai import OpenAI

client = OpenAI()
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-5.2")

INSTRUCTIONS = (
    "You are a booking assistant for a business. "
    "Help users book, reschedule, or cancel appointments. "
    "Be short and clear. "
    "Ask only the minimum follow-up questions needed. "
    "Use tools to check availability and create or update bookings. "
    "If the user asks something outside booking, answer briefly and offer to book."
)

def run_agent(user_message: str, tools: list[dict], tool_handler):
    response = client.responses.create(
        model=CHAT_MODEL,
        instructions=INSTRUCTIONS,
        input=[{"role": "user", "content": user_message}],
        tools=tools,
    )

    while True:
        tool_calls = [x for x in response.output if x.type == "tool_call"]
        if not tool_calls:
            return response.output_text

        outputs = []
        for call in tool_calls:
            result = tool_handler(call.name, call.arguments)
            outputs.append(
                {"type": "tool_output", "tool_call_id": call.id, "output": result}
            )

        response = client.responses.create(
            model=CHAT_MODEL,
            instructions=INSTRUCTIONS,
            input=response.output + outputs,
            tools=tools,
        )