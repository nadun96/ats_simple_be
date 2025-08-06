import pika
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class RabbitMQClient:
    """RabbitMQ client for email service"""

    def __init__(self):
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(
                settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD
            )

            parameters = pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                virtual_host=settings.RABBITMQ_VHOST,
                credentials=credentials,
            )

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            # Declare queues
            self.declare_queues()

            logger.info("Connected to RabbitMQ successfully")

        except Exception as exc:
            logger.error(f"Failed to connect to RabbitMQ: {str(exc)}")
            raise exc

    def declare_queues(self):
        """Declare necessary queues"""
        try:
            # Email queue with priority support
            self.channel.queue_declare(
                queue="email_queue", durable=True, arguments={"x-max-priority": 10}
            )

            # Dead letter queue for failed emails
            self.channel.queue_declare(queue="email_queue_dlq", durable=True)

            # Notification queue for immediate notifications
            self.channel.queue_declare(queue="notification_queue", durable=True)

            logger.info("RabbitMQ queues declared successfully")

        except Exception as exc:
            logger.error(f"Failed to declare queues: {str(exc)}")
            raise exc

    def publish_message(self, queue_name, message, priority=0):
        """Publish message to queue"""
        try:
            if not self.channel or self.connection.is_closed:
                self.connect()

            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    priority=priority,
                    delivery_mode=2,  # Make message persistent
                ),
            )

            logger.info(f"Message published to {queue_name} with priority {priority}")

        except Exception as exc:
            logger.error(f"Failed to publish message: {str(exc)}")
            raise exc

    def consume_messages(self, queue_name, callback):
        """Consume messages from queue"""
        try:
            if not self.channel or self.connection.is_closed:
                self.connect()

            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue=queue_name, on_message_callback=callback, auto_ack=False
            )

            logger.info(f"Started consuming from {queue_name}")
            self.channel.start_consuming()

        except Exception as exc:
            logger.error(f"Failed to consume messages: {str(exc)}")
            raise exc

    def close_connection(self):
        """Close RabbitMQ connection"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logger.info("RabbitMQ connection closed")

        except Exception as exc:
            logger.error(f"Failed to close connection: {str(exc)}")

    def __del__(self):
        """Cleanup connection on object destruction"""
        self.close_connection()


def email_queue_callback(ch, method, properties, body):
    """Callback function for processing email queue messages"""
    try:
        message = json.loads(body.decode("utf-8"))
        email_id = message.get("email_id")

        if email_id:
            # Import here to avoid circular imports
            from .tasks import send_email_task

            # Process email
            send_email_task.delay(email_id)

            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Processed email queue message for email {email_id}")
        else:
            logger.error("Invalid message format - missing email_id")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Exception as exc:
        logger.error(f"Failed to process email queue message: {str(exc)}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def notification_queue_callback(ch, method, properties, body):
    """Callback function for processing notification queue messages"""
    try:
        message = json.loads(body.decode("utf-8"))

        # Import here to avoid circular imports
        from .tasks import send_notification_email

        # Process notification
        send_notification_email.delay(**message)

        # Acknowledge message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("Processed notification queue message")

    except Exception as exc:
        logger.error(f"Failed to process notification queue message: {str(exc)}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
