import os
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError, TopicAlreadyExistsError
from kafka.admin import KafkaAdminClient, NewTopic

# Retrieve Kafka SASL credentials from environment variables
kafka_username = os.getenv('KAFKA_SASL_USERNAME')
kafka_password = os.getenv('KAFKA_SASL_PASSWORD')
kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka.messaging.svc.cluster.local:9092')

class KafkaHandler:
    def __init__(self, bootstrap_servers=kafka_bootstrap_servers):
        try:
            # Kafka Producer setup with SASL authentication
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                security_protocol='SASL_PLAINTEXT',
                sasl_mechanism='PLAIN',
                sasl_plain_username=kafka_username,
                sasl_plain_password=kafka_password
            )
            self.admin_client = KafkaAdminClient(
                bootstrap_servers=bootstrap_servers,
                security_protocol='SASL_PLAINTEXT',
                sasl_mechanism='PLAIN',
                sasl_plain_username=kafka_username,
                sasl_plain_password=kafka_password
            )
        except KafkaError as e:
            print(f"Error initializing Kafka: {e}")
            self.producer = None

    def create_topic(self, topic):
        try:
            topic_list = [NewTopic(name=topic, num_partitions=1, replication_factor=1)]
            self.admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print(f"Topic '{topic}' created successfully.")
        except TopicAlreadyExistsError:
            print(f"Topic '{topic}' already exists.")
        except KafkaError as e:
            print(f"Error creating topic: {e}")

    def send_message(self, topic, value):
        try:
            if self.producer:
                self.producer.send(topic, value.encode('utf-8')).get(timeout=10)
            else:
                print("Producer is not available.")
        except KafkaError as e:
            print(f"Error sending message: {e}")

    def create_consumer(self, topic):
        try:
            # Kafka Consumer setup with SASL authentication
            self.consumer = KafkaConsumer(
                topic,
                bootstrap_servers=bootstrap_servers,
                security_protocol='SASL_PLAINTEXT',
                sasl_mechanism='SCRAM-SHA-256',
                sasl_plain_username=kafka_username,
                sasl_plain_password=kafka_password
            )
            return self.consumer
        except KafkaError as e:
            print(f"Error creating Kafka consumer: {e}")
            return None

    def process_messages(self, topic):
        consumer = self.create_consumer(topic)
        if consumer:
            try:
                for message in consumer:
                    print(f"Received message: {message.value.decode('utf-8')}")
            except KafkaError as e:
                print(f"Error processing messages: {e}")
