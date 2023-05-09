# """
# Django command to create a database record.
# """
# from goal_maven.core import models

# from django.core.management.base import BaseCommand


# class Command(BaseCommand):
#     """Django command create a database record."""

#     def handle(self, *args, **options):
#         """Entrypoint for command."""
#         model_option = ['1 - Continent', '2 - Nation', '3 - City',
#         '4 - Stadium', '5 - Team', '6 - Manager', '7 - Player', '8 - PlayerRole',
#         '9 - Referee', '10 - Season', '11 - League', '12 - LeagueTable', '13 - Fixture',
#         '14 - Match', '15 - MatchEvent', '16 - EventType', '17 - PitchLocation']
#         for option in model_option:
#             self.stdout.write(option)
#         selection = input('(1 - 17): ')
#         if selection == 1:
#             self.stdout.write(selection)
#             print(selection)
#             self.prompt_continent()
#         if selection == 2:
#             prompt_continent()
#         if selection == 3:
#             prompt_continent()
#         if selection == 4:
#             prompt_continent()
#         if selection == 5:
#             prompt_continent()
#         if selection == 6:
#             prompt_continent()
#         if selection == 7:
#             prompt_continent()
#         if selection == 8:
#             prompt_continent()
#         if selection == 9:
#             prompt_continent()
#         if selection == 10:
#             prompt_continent()
#         if selection == 11:
#             prompt_continent()

#     def create(self, model, **params):
#         pass

#     def prompt_continent(self):
#         # Prompt for the continent
#         self.continent_name = None
#         while not self.continent_name:
#             self.continent_name = input('Continent Name: ')
#             if not self.continent_name:
#                 self.stderr.write('Error: Continent Name cannot be blank.')

#         try:
#             models.Continent.objects.get(continent_name=self.continent_name)
#         except DoesNotExist:
#             models.Continent.objects.create(continent_name=self.continent_name)
#             self.stdout.write(self.style.SUCCESS('Record added successfully.'))
#         else:
#             self.stderr.write('Continent with provided name already exists.')
