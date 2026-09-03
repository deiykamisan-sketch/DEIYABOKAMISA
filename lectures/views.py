import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import LectureForm, QuestionForm
from .models import ChatMessage, Lecture, LiveParticipant, LiveSession, WhiteboardSnapshot
from realtime.models import SignalingMessage
from recording.models import LectureRecording
from ai.summarizer import summarize
from ai.notes import build_notes
from ai.pdf_generator import create_lecture_pdf
from django.core.files.base import ContentFile
from pathlib import Path
import tempfile


def home(request):
    return render(request, 'lectures/home.html')


def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'lectures/dashboard.html', {'lectures': request.user.lectures.all()})


@login_required
def lecture_create(request):
    form = LectureForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        lecture = form.save(commit=False)
        lecture.owner = request.user
        lecture.save()
        session = LiveSession.objects.create(lecture=lecture)
        return redirect('live_room', code=session.code)
    return render(request, 'lectures/lecture_form.html', {'form': form})


@login_required
def lecture_detail(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk, owner=request.user)
    qform = QuestionForm()
    return render(request, 'lectures/lecture_detail.html', {'lecture': lecture, 'qform': qform})


def shared_lecture(request, token):
    lecture = get_object_or_404(Lecture, share_token=token, privacy='shared')
    return render(request, 'lectures/shared.html', {'lecture': lecture})


@login_required
@require_POST
def save_snapshot(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk, owner=request.user)
    try:
        payload = json.loads(request.body)
        image = payload.get('image', '')
        if not image.startswith('data:image/png;base64,') or len(image) > 6_000_000:
            raise ValueError
        snapshot = WhiteboardSnapshot.objects.create(
            lecture=lecture, original_drawing=image,
            recognized_text=payload.get('recognized_text', '')[:5000],
            drawing_type=payload.get('drawing_type', '')[:60],
        )
        return JsonResponse({'ok': True, 'id': snapshot.pk})
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'ok': False, 'error': 'Invalid drawing'}, status=400)


@login_required
@require_POST
def add_question(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk, owner=request.user)
    form = QuestionForm(request.POST)
    if form.is_valid():
        question = form.save(commit=False)
        question.lecture, question.author = lecture, request.user
        question.save()
    return redirect(lecture)


@login_required
@require_POST
def start_live(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk, owner=request.user)
    session, _ = LiveSession.objects.get_or_create(lecture=lecture)
    session.is_live = True
    session.ended_at = None
    session.save()
    return redirect('live_room', code=session.code)


@login_required
def join_live(request):
    error_message = None
    if request.method == 'POST':
        entered_code = ''.join(ch for ch in request.POST.get('code', '').upper() if ch.isalnum())
        session = next((item for item in LiveSession.objects.filter(is_live=True)
                        if ''.join(ch for ch in item.code.upper() if ch.isalnum()) == entered_code), None)
        if session is None:
            error_message = 'The lecture code is incorrect, or the lecture is no longer live.'
        else:
            if session.lecture.owner_id != request.user.id:
                LiveParticipant.objects.get_or_create(session=session, user=request.user)
            return redirect('live_room', code=session.code)
    return render(request, 'lectures/join_live.html', {'error_message': error_message})


@login_required
def live_room(request, code):
    session = get_object_or_404(LiveSession, code=code, is_live=True)
    is_lecturer = session.lecture.owner_id == request.user.id
    if not is_lecturer:
        LiveParticipant.objects.get_or_create(session=session, user=request.user)
    return render(request, 'lectures/live_room.html', {'session': session, 'is_lecturer': is_lecturer})


@login_required
def live_api(request, code):
    session = get_object_or_404(LiveSession, code=code, is_live=True)
    is_lecturer = session.lecture.owner_id == request.user.id
    participant = None if is_lecturer else get_object_or_404(LiveParticipant, session=session, user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body or '{}')
        action = data.get('action')
        if action == 'board' and is_lecturer:
            image = data.get('image', '')
            if image.startswith('data:image/png;base64,') and len(image) <= 6_000_000:
                session.whiteboard_state = image
                session.save(update_fields=['whiteboard_state'])
        elif action == 'chat':
            text = data.get('text', '').strip()[:500]
            if text:
                ChatMessage.objects.create(session=session, author=request.user, text=text)
        elif action == 'transcript' and is_lecturer:
            text = data.get('text', '').strip()[:5000]
            if text:
                session.lecture.transcript = (session.lecture.transcript + '\n' + text).strip()
                session.lecture.save(update_fields=['transcript', 'updated_at'])
        elif action == 'hand' and participant:
            participant.raised_hand = not participant.raised_hand
            participant.save(update_fields=['raised_hand', 'last_seen'])
        elif action == 'end' and is_lecturer:
            lecture = session.lecture
            lecture.summary = summarize(lecture.transcript)
            notes_data = build_notes(lecture.title, lecture.transcript)
            lecture.notes = '\n'.join([notes_data['summary'], '', 'Review questions:', *[f'- {q}' for q in notes_data['review_questions']]])
            with tempfile.TemporaryDirectory() as folder:
                pdf_path = Path(folder) / 'lecture.pdf'
                create_lecture_pdf(pdf_path, notes_data)
                lecture.attachment.save(f'{lecture.title[:50]}_summary.pdf', ContentFile(pdf_path.read_bytes()), save=False)
            lecture.save()
            session.is_live = False
            session.save(update_fields=['is_live'])
            return JsonResponse({'ended': True})
    if participant:
        participant.save(update_fields=['last_seen'])
    return JsonResponse({'board': session.whiteboard_state, 'lecturer': session.lecture.owner.username,
        'participants': [{'id': p.user_id, 'name': p.user.username, 'hand': p.raised_hand} for p in session.participants.select_related('user')],
        'messages': [{'name': m.author.username, 'text': m.text} for m in session.messages.select_related('author').order_by('-id')[:30]][::-1]})


@login_required
def signal_api(request, code):
    session = get_object_or_404(LiveSession, code=code, is_live=True)
    allowed = session.lecture.owner_id == request.user.id or session.participants.filter(user=request.user).exists()
    if not allowed:
        return JsonResponse({'error': 'Not a participant'}, status=403)
    if request.method == 'POST':
        try:
            data = json.loads(request.body or '{}')
            message = SignalingMessage.objects.create(
                session=session, sender=request.user,
                target_user_id=data.get('target_user_id'),
                signal_type=data['signal_type'], payload=data.get('payload', {}))
            return JsonResponse({'ok': True, 'id': message.id})
        except (KeyError, TypeError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid signal'}, status=400)
    after = request.GET.get('after', '0')
    try: after_id = int(after)
    except ValueError: after_id = 0
    messages = SignalingMessage.objects.filter(session=session, id__gt=after_id, target_user_id=request.user.id).order_by('id')[:100]
    return JsonResponse({'signals': [{'id': m.id, 'sender_id': m.sender_id,
        'type': m.signal_type, 'payload': m.payload} for m in messages]})


@login_required
@require_POST
def upload_recording(request, code):
    session = get_object_or_404(LiveSession, code=code)
    if session.lecture.owner_id != request.user.id:
        return JsonResponse({'error': 'Only the lecturer can save recordings.'}, status=403)
    video = request.FILES.get('recording')
    if not video:
        return JsonResponse({'error': 'No recording supplied.'}, status=400)
    recording = LectureRecording.objects.create(
        lecture=session.lecture, state='ready', video_file=video,
        duration_seconds=max(0, int(request.POST.get('duration', '0') or 0)))
    return JsonResponse({'ok': True, 'id': recording.id, 'url': recording.video_file.url})
