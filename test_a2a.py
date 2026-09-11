import asyncio
import uuid

from a2a.client import create_client
from a2a.types import Message, Part, Role, SendMessageRequest


async def main():

    # 1. Connect to the remote Weather Agent
    client = await create_client(
        "http://localhost:8001"
    )

    print("A2A client created successfully.")

    # 2. Create the user message
    message = Message(
        role=Role.ROLE_USER,
        message_id=str(uuid.uuid4()),
        parts=[
            Part(
                text="What is the weather in Paris?"
            )
        ],
    )

    # 3. Wrap the message in an A2A request
    request = SendMessageRequest(
        message=message
    )

    print("Sending message through A2A...")

    # 4. Send the A2A request
    async for response in client.send_message(request):
        print("\n--- A2A RESPONSE ---")
        print(response)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())