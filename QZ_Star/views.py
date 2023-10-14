import json

from django.contrib.auth.models import User
from django.db.models import F
from django.db.models import Prefetch, Sum
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from QZ_Star.models import Category, Quiz, QuizUserScoreSheet, QuizQuestions
from QZ_Star.serializers import CategorySerializer, QuizUserScoreSheetSerializer, LeaderBoardSerializer


@csrf_exempt
def index(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except (json.decoder.JSONDecodeError, ValueError, TypeError) as e:
            return JsonResponse({
                "error": str(e)
            },
                status=400
            )

        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').strip()

        if not email:
            JsonResponse({
                "error": "Email is required"
            },
                status=400
            )

        user = User.objects.filter(email=email).first()
        update = {}
        if first_name:
            update["first_name"] = first_name
        if last_name:
            update["last_name"] = last_name

        if not user:
            user = User.objects.create_user(username=email,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password="admin@123")
        else:
            if update:
                for k, v in update.items():
                    setattr(user, k, v)
                user.save()

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        })


@csrf_exempt
def get_user_score(request, id):
    queryset = QuizUserScoreSheet.objects.filter(user_id_id=id).annotate(first_name=F('user_id__first_name'),
                                                   last_name=F('user_id__last_name')) \
        .values('user_id_id', 'first_name', 'last_name').annotate(scores=Sum('score')) \
        .values('user_id_id', 'first_name', 'last_name', 'scores')


@csrf_exempt
def home_page(request):
    html = "<html><body><h2>Quiz Star</h2></body></html>"
    return HttpResponse(html)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().prefetch_related(Prefetch(
        'quiz_set',
        queryset=Quiz.objects.all().prefetch_related("quizquestions_set")
    ))
    serializer_class = CategorySerializer


class QuizUserScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuizUserScoreSheet.objects.annotate(first_name=F('user_id__first_name'),
                                                   last_name=F('user_id__last_name'))\
                .values('user_id_id', 'first_name', 'last_name').annotate(scores=Sum('score'))\
                .values('user_id_id', 'first_name', 'last_name', 'scores').order_by('-scores')
    serializer_class = LeaderBoardSerializer


class QuizUserScoreIndividualViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuizUserScoreSheet.objects.all()

    def retrieve(self, request, pk=None):
        queryset = QuizUserScoreSheet.objects.filter(user_id_id=pk).annotate(first_name=F('user_id__first_name'),
                                                   last_name=F('user_id__last_name'))\
                .values('user_id_id', 'first_name', 'last_name').annotate(scores=Sum('score'))\
                .values('user_id_id', 'first_name', 'last_name', 'scores')
        if not len(queryset):
            queryset = [{}]
        return Response(queryset[0])


class QuizAnswerViewSet(viewsets.mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = QuizUserScoreSheet.objects.all()
    serializer_class = QuizUserScoreSheetSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        if QuizUserScoreSheet.objects.filter(
                quiz_id=data["quiz_id"], user_id=data["user_id"]).exists():
            Response({}, status=status.HTTP_201_CREATED)

        try:
            for ans in data["answers"]:
                ans["quiz_id"] = data["quiz_id"]
                ans["user_id"] = data["user_id"]
                quiz_question = QuizQuestions.objects.filter(
                    id=ans["quiz_questions"]
                ).select_related("question_id__answer_option_type_id").first()
                if not quiz_question:
                    raise ValidationError({
                        "error": "Invalid question."
                    })
                if quiz_question.question_id.answer_option_type_id.correct_option == ans["option_selected"]:
                    ans["score"] = quiz_question.question_id.points
                else:
                    ans["score"] = 0
        except QuizQuestions.DoesNotExist:
            return JsonResponse({
                "error": "Invalid question id"
            },
                status=400
            )

        serializer = self.get_serializer(data=data["answers"], many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({}, status=status.HTTP_201_CREATED, headers=headers)
