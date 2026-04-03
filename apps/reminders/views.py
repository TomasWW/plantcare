from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.plants.models import Plant

from .forms import ReminderForm
from .models import Reminder


@login_required
def list_reminders(request):
    reminders = request.user.reminders.order_by("reminder_time")
    reminders_with_date = []
    for reminder in reminders:
        completed_dates = set(reminder.history.values_list("completed_date", flat=True))
        dates = []
        if reminder.repeat:
            current_date = reminder.reminder_time.date()
            for i in range(5):
                dates.append(current_date)
                current_date += timedelta(days=reminder.repeat)
        reminders_with_date.append(
            {"reminder": reminder, "dates": dates, "completed_dates": completed_dates}
        )
    return render(
        request,
        "reminders/reminder_list.html",
        {"reminders_with_date": reminders_with_date},
    )


@login_required
def create_reminder(request, plant_id):
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.plant = get_object_or_404(Plant, id=plant_id, user=request.user)
            reminder.save()
            return redirect("list_reminders")
    else:
        form = ReminderForm(initial={"reminder_time": timezone.now()})
    return render(request, "reminders/reminder_form.html", {"form": form})


@login_required
def complete_reminder(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    if request.method == "POST":
        completed_reminder = request.POST.get("completed_date")
        if completed_reminder:
            reminder.history.create(completed_date=completed_reminder)
        return redirect("list_reminders")
    return render(
        request, "reminders/reminder_confirm_complete.html", {"reminder": reminder}
    )


@login_required
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    if request.method == "POST":
        reminder.delete()
        return redirect("list_reminders")
    return render(
        request, "reminders/reminder_confirm_delete.html", {"reminder": reminder}
    )
