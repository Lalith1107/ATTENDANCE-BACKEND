from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time

from attendance.models import Attendance


class Command(BaseCommand):
    help = "Automatically check out staff who forgot to check out"

    def handle(self, *args, **options):
        now = timezone.localtime()
        today = now.date()

        # ⏰ Auto checkout cutoff time (6:30 PM)
        AUTO_CHECKOUT_TIME = time(18, 30)

        # Run only after cutoff time
        if now.time() < AUTO_CHECKOUT_TIME:
            self.stdout.write(
                self.style.WARNING("Auto checkout skipped (before cutoff time)")
            )
            return

        # Find active attendance records
        open_attendances = Attendance.objects.filter(
            date=today,
            check_out_time__isnull=True,
            admin_override=False
        )

        count = 0

        for attendance in open_attendances:
            attendance.check_out_time = now
            attendance.status = "AUTO_CHECKOUT"
            attendance.auto_checked_out = True
            attendance.save()
            count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Auto checkout completed. {count} record(s) updated."
            )
        )
