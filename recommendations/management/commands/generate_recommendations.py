"""
Management command to generate recommendations for all users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recommendations.recommendation_engine import RecommendationService
from recommendations.models import RecommendationCache


class Command(BaseCommand):
    help = 'Generate recommendations for all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=int,
            help='Generate recommendations for a specific user ID',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing recommendations before generating new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            RecommendationCache.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing recommendations'))

        if options['user']:
            users = User.objects.filter(id=options['user'])
        else:
            users = User.objects.all()

        for user in users:
            self.stdout.write(f'Generating recommendations for {user.username}...')
            recommendations = RecommendationService.get_personalized_recommendations(user, n=20)

            for rec in recommendations:
                RecommendationCache.objects.create(
                    user=user,
                    product=rec['product'],
                    score=rec['score'],
                    algorithm=rec['algorithm']
                )

            self.stdout.write(self.style.SUCCESS(
                f'Generated {len(recommendations)} recommendations for {user.username}'
            ))

        self.stdout.write(self.style.SUCCESS('Recommendation generation complete!'))
