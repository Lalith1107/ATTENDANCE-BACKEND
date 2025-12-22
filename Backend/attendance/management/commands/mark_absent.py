from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time

from attendance.models import Attendance
from locations.models import LocationLog


class Command(BaseCommand):
    help = "Mark staff ABSENT if no location ping is recorded"

    def handle(self, *args, **options):
        now = timezone.localtime()
        today = now.date()

        # ⏰ Location ping cutoff time (12:00 PM)
        PING_CUTOFF_TIME = time(12, 0)

        # Run only after cutoff time
        if now.time() < PING_CUTOFF_TIME:
            self.stdout.write(
                self.style.WARNING("Absent check skipped (before cutoff time)")
            )
            return

        # Get today's attendance records
        attendances = Attendance.objects.filter(
            date=today,
            admin_override=False
        )

        absent_count = 0

        for attendance in attendances:
            # Skip if already checked out or auto-checked out
            if attendance.check_out_time:
                continue

            # Check if location ping exists for today
            has_ping = LocationLog.objects.filter(
                user=attendance.user,
                timestamp__date=today
            ).exists()

            if not has_ping:
                attendance.status = "ABSENT"
                attendance.check_in_time = None
                attendance.check_out_time = None
                attendance.save()
                absent_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Absent marking completed. {absent_count} user(s) marked ABSENT."
            )
        )
