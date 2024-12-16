from google.cloud import pubsub_v1
import json


class PubSubService:
    def __init__(self, project_id: str):
        """
        Initialize Pub/Sub Publisher and Subscriber clients.
        :param project_id: Google Cloud Project ID
        """
        self.project_id = project_id
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish_message(self, topic_name: str, message: dict):
        """
        Publish a message to a Pub/Sub topic.
        :param topic_name: Name of the Pub/Sub topic
        :param message: Dictionary payload to publish
        """
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        json_message = json.dumps(message).encode("utf-8")

        future = self.publisher.publish(topic_path, json_message)
        print(f"Message published to {topic_name}: {future.result()}")

    def subscribe_to_topic(self, subscription_name: str, callback):
        """
        Subscribe to a Pub/Sub topic and handle messages with a callback function.
        :param subscription_name: Name of the Pub/Sub subscription
        :param callback: Function to process messages
        """
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_name)

        def wrapped_callback(message):
            data = json.loads(message.data.decode("utf-8"))
            print(f"Received message: {data}")
            callback(data)
            message.ack()

        streaming_pull_future = self.subscriber.subscribe(subscription_path, callback=wrapped_callback)
        print(f"Listening for messages on {subscription_name}...")

        try:
            streaming_pull_future.result()  
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            print("Subscription stopped.")
