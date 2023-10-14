from rest_framework import serializers

from QZ_Star.models import Category, Quiz, QuizQuestions, QuizUserScoreSheet


class QuizQuestionsSerializer(serializers.ModelSerializer):
    quiz_question_id = serializers.ReadOnlyField(source="id")
    question_type = serializers.ReadOnlyField(source="question_id.answer_option_type_id.question_type")
    question_text = serializers.ReadOnlyField(source="question_id.question_description")
    correct_option = serializers.ReadOnlyField(source="question_id.answer_option_type_id.correct_option")
    options = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestions
        fields = ["quiz_question_id", "question_type", "question_text", "correct_option", "options"]


    def get_options(self, obj):
        question = obj.question_id
        if question:
            question_answer_option_type = question.answer_option_type_id
            if question_answer_option_type:
                if question_answer_option_type.question_type == "MCQ":
                    return [
                            {
                                "option_id": 1,
                                "option_text": question_answer_option_type.option1
                            },
                            {
                                "option_id": 2,
                                "option_text": question_answer_option_type.option2
                            },
                            {
                                "option_id": 3,
                                "option_text": question_answer_option_type.option3
                            },
                            {
                                "option_id": 4,
                                "option_text": question_answer_option_type.option4
                            }
                        ]
                elif question_answer_option_type.question_type == "TF":
                    return [
                        {
                            "option_id": 1,
                            "option_text": question_answer_option_type.option1
                        },
                        {
                            "option_id": 2,
                            "option_text": question_answer_option_type.option2
                        }
                    ]


class QuizSerializer(serializers.ModelSerializer):
    quiz_id = serializers.ReadOnlyField(source="id")
    quiz_questions = QuizQuestionsSerializer(source="quizquestions_set", many=True)

    class Meta:
        model = Quiz
        fields = ["quiz_id", "quiz_name", "is_active", "is_anonymous", "quiz_questions"]


class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.ReadOnlyField(source="id")
    category_name = serializers.ReadOnlyField()
    quizs = QuizSerializer(source="quiz_set", many=True)

    class Meta:
        model = Category
        fields = ["category_id",
                  "category_name",
                  "quizs"]


class LeaderBoardSerializer(serializers.ModelSerializer):
    scores = serializers.ReadOnlyField()
    user_id = serializers.ReadOnlyField(source='user_id_id')
    last_name = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()

    class Meta:
        model = QuizUserScoreSheet
        fields = ['scores', 'user_id', 'first_name', 'last_name']


class QuizUserScoreSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizUserScoreSheet
        fields = "__all__"

