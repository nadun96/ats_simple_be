from django.core.management.base import BaseCommand
from apps.api.models import EmailTemplate


class Command(BaseCommand):
    help = "Load default email templates"

    def handle(self, *args, **options):
        templates = [
            {
                "name": "application_received",
                "template_type": "confirmation",
                "subject": "Application Received - {position_title}",
                "body_html": """
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Thank you for your application!</h2>
                    <p>Dear {applicant_name},</p>
                    <p>We have received your application for the position of <strong>{position_title}</strong> at {company_name}.</p>
                    <p>Our team will review your application and get back to you within {review_timeframe} business days.</p>
                    <p>Application Details:</p>
                    <ul>
                        <li>Position: {position_title}</li>
                        <li>Application ID: {application_id}</li>
                        <li>Submitted: {submission_date}</li>
                    </ul>
                    <p>Best regards,<br>{company_name} Recruitment Team</p>
                </div>
                """,
                "body_text": """
                Thank you for your application!
                
                Dear {applicant_name},
                
                We have received your application for the position of {position_title} at {company_name}.
                
                Our team will review your application and get back to you within {review_timeframe} business days.
                
                Application Details:
                - Position: {position_title}
                - Application ID: {application_id}
                - Submitted: {submission_date}
                
                Best regards,
                {company_name} Recruitment Team
                """,
            },
            {
                "name": "interview_scheduled",
                "template_type": "meeting_reminder",
                "subject": "Interview Scheduled - {position_title}",
                "body_html": """
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Interview Invitation</h2>
                    <p>Dear {applicant_name},</p>
                    <p>We are pleased to invite you for an interview for the position of <strong>{position_title}</strong>.</p>
                    <p><strong>Interview Details:</strong></p>
                    <ul>
                        <li>Date: {interview_date}</li>
                        <li>Time: {interview_time}</li>
                        <li>Duration: {interview_duration}</li>
                        <li>Type: {interview_type}</li>
                        <li>Location: {interview_location}</li>
                    </ul>
                    {interview_link}
                    <p>Please confirm your attendance by replying to this email.</p>
                    <p>Best regards,<br>{interviewer_name}<br>{company_name}</p>
                </div>
                """,
                "body_text": """
                Interview Invitation
                
                Dear {applicant_name},
                
                We are pleased to invite you for an interview for the position of {position_title}.
                
                Interview Details:
                - Date: {interview_date}
                - Time: {interview_time}
                - Duration: {interview_duration}
                - Type: {interview_type}
                - Location: {interview_location}
                
                {interview_link}
                
                Please confirm your attendance by replying to this email.
                
                Best regards,
                {interviewer_name}
                {company_name}
                """,
            },
            {
                "name": "task_reminder",
                "template_type": "task_reminder",
                "subject": "Task Reminder: {task_name}",
                "body_html": """
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Task Reminder</h2>
                    <p>Hello {assignee_name},</p>
                    <p>This is a reminder about the following task:</p>
                    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <h3>{task_name}</h3>
                        <p><strong>Description:</strong> {task_description}</p>
                        <p><strong>Due Date:</strong> {due_date}</p>
                        <p><strong>Priority:</strong> {priority}</p>
                    </div>
                    <p>Please complete this task by the due date.</p>
                    <p>Best regards,<br>ATS Team</p>
                </div>
                """,
                "body_text": """
                Task Reminder
                
                Hello {assignee_name},
                
                This is a reminder about the following task:
                
                Task: {task_name}
                Description: {task_description}
                Due Date: {due_date}
                Priority: {priority}
                
                Please complete this task by the due date.
                
                Best regards,
                ATS Team
                """,
            },
            {
                "name": "application_status_update",
                "template_type": "application_status",
                "subject": "Application Status Update - {position_title}",
                "body_html": """
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2>Application Status Update</h2>
                    <p>Dear {applicant_name},</p>
                    <p>We would like to update you on the status of your application for the position of <strong>{position_title}</strong>.</p>
                    <div style="background-color: #e6f3ff; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p><strong>Current Status:</strong> {application_status}</p>
                        <p><strong>Next Steps:</strong> {next_steps}</p>
                    </div>
                    <p>{status_message}</p>
                    <p>If you have any questions, please don't hesitate to contact us.</p>
                    <p>Best regards,<br>{company_name} Recruitment Team</p>
                </div>
                """,
                "body_text": """
                Application Status Update
                
                Dear {applicant_name},
                
                We would like to update you on the status of your application for the position of {position_title}.
                
                Current Status: {application_status}
                Next Steps: {next_steps}
                
                {status_message}
                
                If you have any questions, please don't hesitate to contact us.
                
                Best regards,
                {company_name} Recruitment Team
                """,
            },
        ]

        created_count = 0
        updated_count = 0

        for template_data in templates:
            template, created = EmailTemplate.objects.update_or_create(
                name=template_data["name"], defaults=template_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created template: {template.name}")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Updated template: {template.name}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Completed! Created: {created_count}, Updated: {updated_count}"
            )
        )
