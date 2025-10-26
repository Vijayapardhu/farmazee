from django.apps import AppConfig


class FarmerProblemsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'farmer_problems'

    def ready(self):
        from django.db.models.signals import post_save
        from .models import ProblemImage

        def schedule_auto_detection(sender, instance, created, **kwargs):
            if created and not instance.auto_checked:
                try:
                    from ai_ml.tasks import analyze_problem_image
                    instance.auto_check_status = 'processing'
                    instance.save(update_fields=['auto_check_status'])
                    try:
                        analyze_problem_image.delay(
                            image_url=instance.image_url,
                            problem_id=instance.problem_id,
                            user_id=instance.problem.author_id,
                            location=instance.problem.location or ''
                        )
                    except Exception:
                        # Fallback to direct call if background worker isn't running
                        analyze_problem_image(
                            image_url=instance.image_url,
                            problem_id=instance.problem_id,
                            user_id=instance.problem.author_id,
                            location=instance.problem.location or ''
                        )
                except Exception:
                    # Defer failures silently to avoid UI noise
                    instance.auto_check_status = 'failed'
                    instance.save(update_fields=['auto_check_status'])

        post_save.connect(schedule_auto_detection, sender=ProblemImage, dispatch_uid='farmer_problems_image_auto_detect')