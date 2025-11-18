import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = "Fill database with test data"

    def add_arguments(self, parser):
        parser.add_argument(
            'ratio',
            type=int,
            nargs='?',
            default=1,
            help="Multiplier for amount of generated data"
        )

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        self.stdout.write(self.style.WARNING(f"Generating data with ratio = {ratio}"))

        NUM_USERS = ratio
        NUM_TAGS = ratio
        NUM_QUESTIONS = ratio * 10
        NUM_ANSWERS = ratio * 100
        NUM_LIKES = ratio * 200

        # USERS
        users = []
        for i in range(NUM_USERS):
            user = User.objects.create_user(
                username=f"user_{ratio}_{i}",
                password="password"
            )
            profile = Profile.objects.create(user=user)
            users.append(profile)

        self.stdout.write(self.style.SUCCESS("Users created"))

        # TAGS
        tags = []
        for i in range(NUM_TAGS):
            tag = Tag.objects.create(name=f"tag_{ratio}_{i}")
            tags.append(tag)

        self.stdout.write(self.style.SUCCESS("Tags created"))

        # QUESTIONS
        questions = []
        for i in range(NUM_QUESTIONS):
            title = f"Question title {ratio}-{i}"
            text = ''.join(random.choices(string.ascii_letters + " " * 10, k=random.randint(80, 250)))

            question = Question.objects.create(
                title=title,
                text=text,
                user=random.choice(users)
            )

            question.tags.set(random.sample(tags, k=random.randint(1, min(4, len(tags)))))

            questions.append(question)

        self.stdout.write(self.style.SUCCESS("Questions created"))

        # ANSWERS
        answers = []
        for i in range(NUM_ANSWERS):
            text = ''.join(random.choices(string.ascii_letters + " " * 10, k=random.randint(50, 200)))

            answer = Answer.objects.create(
                question=random.choice(questions),
                text=text,
                is_correct=random.choice([True, False]),
                user=random.choice(users)
            )

            answers.append(answer)

        self.stdout.write(self.style.SUCCESS("Answers created"))

        # LIKES (split roughly 50/50 between questions и answers)
        like_targets = questions + answers
        random.shuffle(like_targets)

        for i in range(NUM_LIKES):
            obj = random.choice(like_targets)
            profile = random.choice(users)

            if isinstance(obj, Question):
                if not QuestionLike.objects.filter(user=profile, question=obj).exists():
                    QuestionLike.objects.create(user=profile, question=obj)
            else:
                if not AnswerLike.objects.filter(user=profile, answer=obj).exists():
                    AnswerLike.objects.create(user=profile, answer=obj)

        self.stdout.write(self.style.SUCCESS("Likes created"))

        self.stdout.write(self.style.SUCCESS(f"Database filled with ratio={ratio}"))
