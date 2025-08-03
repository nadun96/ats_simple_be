from django.core.management.base import BaseCommand
from apps.api.rabbitmq_client import (
    RabbitMQClient,
    email_queue_callback,
    notification_queue_callback,
)
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Start RabbitMQ email queue consumer"

    def add_arguments(self, parser):
        parser.add_argument(
            "--queue",
            type=str,
            default="email_queue",
            help="Queue name to consume from (email_queue or notification_queue)",
        )

    def handle(self, *args, **options):
        queue_name = options["queue"]

        self.stdout.write(
            self.style.SUCCESS(f"Starting consumer for queue: {queue_name}")
        )

        try:
            client = RabbitMQClient()

            if queue_name == "email_queue":
                callback = email_queue_callback
            elif queue_name == "notification_queue":
                callback = notification_queue_callback
            else:
                self.stdout.write(self.style.ERROR(f"Unknown queue: {queue_name}"))
                return

            self.stdout.write(
                self.style.SUCCESS(f"Consuming messages from {queue_name}...")
            )

            client.consume_messages(queue_name, callback)

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Consumer stopped by user"))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Consumer failed: {str(exc)}"))
            logger.error(f"RabbitMQ consumer failed: {str(exc)}")
