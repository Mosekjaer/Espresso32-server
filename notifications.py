from exponent_server_sdk import PushClient, PushMessage

def send_push_notification(expo_push_token, title, body):
    try:
        response = PushClient().publish(
            PushMessage(
                to=expo_push_token,
                title=title,
                body=body,
                sound="default",
                priority="high",
                channel_id="default"
            )
        )
        print("Push-svar:", response)
    except Exception as e:
        print(f"Fejl ved push-besked: {e}")
