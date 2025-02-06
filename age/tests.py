from django.test import TestCase
from .forms import DateForm  # Assurez-vous que le chemin vers votre formulaire est correct
from datetime import date, timedelta
from .forms import DateForm

class IndexViewTest(TestCase):

    def test_get_request(self):
        """
        Test pour la requête GET vers la vue index.
        Vérifie que le formulaire est présent dans le contexte.
        """
        response = self.client.get('/')  # Remplacez '/' par l'URL de votre vue
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], DateForm)

    def test_post_request_valid_date(self):
        """
        Test pour une requête POST avec une date valide.
        Vérifie que l'âge est calculé correctement et que les variables sont 
        présentes dans le contexte.
        """
        date_user_str = '2000-01-01'  # Date de naissance de test
        response = self.client.post('/', {'date': date_user_str}) # Remplacez '/' par l'URL de votre vue

        self.assertEqual(response.status_code, 200)  # ou 302 si vous redirigez

        # Récupérer les valeurs du contexte et les convertir en entiers
        years = int(response.context['years'])
        months = int(response.context['months'])
        days = int(response.context['days'])
        seconds = int(response.context['seconds'])


        date_user = date(2000, 1, 1)
        date_now = date.today()
        diff = date_now - date_user

        expected_years = diff.days // 365
        expected_months = (diff.days % 365) // 30
        expected_days = (diff.days % 365) % 30
        expected_seconds = diff.days * 24 * 3600 + diff.seconds

        self.assertEqual(years, expected_years)
        self.assertEqual(months, expected_months)
        self.assertEqual(days, expected_days)
        # On ne teste pas l'égalité parfaite des secondes, car la date change à chaque exécution du test
        self.assertAlmostEqual(seconds, expected_seconds, delta=1) # Delta permet une marge d'erreur de 1 seconde

        self.assertIsInstance(response.context['form'], DateForm) # Le formulaire doit toujours être présent

    def test_post_request_invalid_date(self):
        """
        Test pour une requête POST avec une date invalide.
        Vérifie que le formulaire contient une erreur.
        """
        response = self.client.post('/', {'date': 'invalid date'}) # Remplacez '/' par l'URL de votre vue
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())  # Le formulaire doit être invalide
        self.assertIn('date', form.errors) # Vérifie que l'erreur concerne le champ date

    def test_post_request_future_date(self):
        """
        Test pour une requête POST avec une date future.
        Vérifie que le formulaire contient une erreur (si vous gérez ce cas).
        """

        future_date = date.today() + timedelta(days=365)  # Date dans un an
        response = self.client.post('/', {'date': future_date}) # Remplacez '/' par l'URL de votre vue
        self.assertEqual(response.status_code, 200)
        form = response.context['form']

        # Deux options : soit vous gérez l'erreur dans le formulaire, soit dans la vue
        # Option 1 : Gestion de l'erreur dans le formulaire (plus propre)
        # self.assertFalse(form.is_valid())
        # self.assertIn('date', form.errors)

        # Option 2 : Gestion de l'erreur dans la vue (moins propre)
        self.assertIsNone(response.context.get('years')) # Assurez-vous que les variables d'âge ne sont pas calculées