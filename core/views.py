from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from .redis_queue import add_to_queue, get_first
from .tasks import send_command_task

@login_required
def fila_view(request):
    add_to_queue(request.user.username)
    return render(request, "core/queue.html")

@login_required
def controlo_view(request):
    if request.user.username != get_first():
        return redirect("fila")
    return render(request, "core/control.html")

class CommandAPIView(APIView):
    def post(self, request):
        if request.user.username != get_first():
            return Response({"error": "not your turn"}, status=403)
        cmd = request.data.get("cmd")
        if not cmd:
            return Response({"error": "missing cmd"}, status=400)
        task = send_command_task.delay(cmd)
        return Response({"status": "queued", "task_id": str(task.id)})