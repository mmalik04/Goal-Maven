"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from datetime import date

from goal_maven.core.tests.helper_methods import HelperMethods

# import pdb


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.helper = HelperMethods()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
            first_name='test',
            last_name='admin',
            username='useradmin69',
            date_of_birth=date(1996, 1, 5),
        )
        self.client.force_login(self.admin_user)
        self.user = self.helper.get_user()

        self.continent = self.helper.create_continent()
        self.nation = self.helper.create_nation()
        self.city = self.helper.create_city()
        self.stadium = self.helper.create_stadium()
        self.manager = self.helper.create_manager()
        self.referee = self.helper.create_referee()
        self.playerrole = self.helper.create_playerrole()
        self.player = self.helper.create_player()
        self.season = self.helper.create_season()
        self.league = self.helper.create_league()
        self.team = self.helper.create_team()
        self.leaguetable = self.helper.create_leaguetable()
        self.matchstatus = self.helper.create_matchstatus()
        self.fixture = self.helper.create_fixture()
        self.match = self.helper.create_match()
        self.eventtype = self.helper.create_eventtype()
        self.pitchlocation = self.helper.create_pitchposition()
        self.matchevent = self.helper.create_matchevent()

    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        # pdb.set_trace()
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_continent_lists(self):
        """Test that continents are listed on page."""
        url = reverse('admin:core_continent_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.continent.continent_name)

    def test_edit_continent_page(self):
        """Test the edit continent page works."""
        url = reverse(
            'admin:core_continent_change', args=[self.continent.continent_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_continent_page(self):
        """Test the create continent page works."""
        url = reverse('admin:core_continent_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_nation_lists(self):
        """Test that nations are listed on page."""
        url = reverse('admin:core_nation_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.nation.nation_name)

    def test_edit_nation_page(self):
        """Test the edit nation page works."""
        url = reverse(
            'admin:core_nation_change', args=[self.nation.nation_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_nation_page(self):
        """Test the create nation page works."""
        url = reverse('admin:core_nation_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_city_lists(self):
        """Test that cities are listed on page."""
        url = reverse('admin:core_city_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.city.city_name)

    def test_edit_city_page(self):
        """Test the edit city page works."""
        url = reverse(
            'admin:core_city_change', args=[self.city.city_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_city_page(self):
        """Test the create city page works."""
        url = reverse('admin:core_city_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_stadium_lists(self):
        """Test that stadiums are listed on page."""
        url = reverse('admin:core_stadium_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.stadium.stadium_name)

    def test_edit_stadium_page(self):
        """Test the edit stadium page works."""
        url = reverse(
            'admin:core_stadium_change', args=[self.stadium.stadium_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_stadium_page(self):
        """Test the create stadium page works."""
        url = reverse('admin:core_stadium_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_manager_lists(self):
        """Test that managers are listed on page."""
        url = reverse('admin:core_manager_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.manager.manager_name)

    def test_edit_manager_page(self):
        """Test the edit manager page works."""
        url = reverse(
            'admin:core_manager_change', args=[self.manager.manager_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_manager_page(self):
        """Test the create manager page works."""
        url = reverse('admin:core_manager_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_referee_lists(self):
        """Test that referees are listed on page."""
        url = reverse('admin:core_referee_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.referee.referee_name)

    def test_edit_referee_page(self):
        """Test the edit referee page works."""
        url = reverse(
            'admin:core_referee_change', args=[self.referee.referee_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_referee_page(self):
        """Test the create referee page works."""
        url = reverse('admin:core_referee_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_playerrole_lists(self):
        """Test that player roles are listed on page."""
        url = reverse('admin:core_playerrole_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.playerrole.role_name)

    def test_edit_playerrole_page(self):
        """Test the edit player role page works."""
        url = reverse(
            'admin:core_playerrole_change', args=[self.playerrole.role_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_playerrole_page(self):
        """Test the create player role page works."""
        url = reverse('admin:core_playerrole_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_player_lists(self):
        """Test that players are listed on page."""
        url = reverse('admin:core_player_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.player.player_name)

    def test_edit_player_page(self):
        """Test the edit player page works."""
        url = reverse(
            'admin:core_player_change', args=[self.player.player_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_player_page(self):
        """Test the create player page works."""
        url = reverse('admin:core_player_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_season_lists(self):
        """Test that seasons are listed on page."""
        url = reverse('admin:core_season_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.season.season_name)

    def test_edit_season_page(self):
        """Test the edit season page works."""
        url = reverse(
            'admin:core_season_change', args=[self.season.season_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_season_page(self):
        """Test the create season page works."""
        url = reverse('admin:core_season_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_league_lists(self):
        """Test that leagues are listed on page."""
        url = reverse('admin:core_league_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.league.league_name)

    def test_edit_league_page(self):
        """Test the edit league page works."""
        url = reverse(
            'admin:core_league_change', args=[self.league.league_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_league_page(self):
        """Test the create league page works."""
        url = reverse('admin:core_league_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_team_lists(self):
        """Test that teams are listed on page."""
        url = reverse('admin:core_team_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.team.team_name)

    def test_edit_team_page(self):
        """Test the edit team page works."""
        url = reverse(
            'admin:core_team_change', args=[self.team.team_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_team_page(self):
        """Test the create team page works."""
        url = reverse('admin:core_team_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_leaguetable_lists(self):
        """Test that league tables are listed on page."""
        url = reverse('admin:core_leaguetable_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.leaguetable.team.team_name)

    def test_edit_leaguetable_page(self):
        """Test the edit league table page works."""
        url = reverse(
            'admin:core_leaguetable_change', args=[self.leaguetable.table_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_leaguetable_page(self):
        """Test the create league table page works."""
        url = reverse('admin:core_leaguetable_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_matchstatus_lists(self):
        """Test that match statuses are listed on page."""
        url = reverse('admin:core_matchstatus_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.matchstatus.status_name)

    def test_edit_matchstatus_page(self):
        """Test the edit match statuses page works."""
        url = reverse(
            'admin:core_matchstatus_change', args=[self.matchstatus.match_status_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_matchstatus_page(self):
        """Test the create match statuses page works."""
        url = reverse('admin:core_matchstatus_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_fixture_lists(self):
        """Test that fixtures are listed on page."""
        url = reverse('admin:core_fixture_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.fixture.home_team.team_name)
        self.assertContains(res, self.fixture.away_team.team_name)

    def test_edit_fixture_page(self):
        """Test the edit fixture page works."""
        url = reverse(
            'admin:core_fixture_change', args=[self.fixture.fixture_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_fixture_page(self):
        """Test the create fixture page works."""
        url = reverse('admin:core_fixture_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_match_lists(self):
        """Test that matches are listed on page."""
        url = reverse('admin:core_match_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.match.fixture.home_team.team_name)
        self.assertContains(res, self.match.fixture.away_team.team_name)

    def test_edit_match_page(self):
        """Test the edit match page works."""
        url = reverse(
            'admin:core_match_change', args=[self.match.match_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_match_page(self):
        """Test the create match page works."""
        url = reverse('admin:core_match_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_eventtype_lists(self):
        """Test that event types are listed on page."""
        url = reverse('admin:core_eventtype_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.eventtype.event_name)

    def test_edit_eventtype_page(self):
        """Test the edit event type page works."""
        url = reverse(
            'admin:core_eventtype_change', args=[self.eventtype.event_type_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_eventtype_page(self):
        """Test the create event type page works."""
        url = reverse('admin:core_eventtype_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_pitchlocation_lists(self):
        """Test that pitch positions are listed on page."""
        url = reverse('admin:core_pitchlocation_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.pitchlocation.pitch_area_name)

    def test_edit_pitchlocation_page(self):
        """Test the edit pitch position page works."""
        url = reverse(
            'admin:core_pitchlocation_change', args=[self.pitchlocation.pitch_area_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_pitchlocation_page(self):
        """Test the create pitch position page works."""
        url = reverse('admin:core_pitchlocation_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_matchevent_lists(self):
        """Test that match events are listed on page."""
        url = reverse('admin:core_matchevent_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.matchevent.event_type.event_name)
        self.assertContains(res, self.matchevent.player.player_name)

    def test_edit_matchevent_page(self):
        """Test the edit match event page works."""
        url = reverse(
            'admin:core_matchevent_change', args=[self.matchevent.event_id],
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_matchevent_page(self):
        """Test the create match event page works."""
        url = reverse('admin:core_matchevent_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
