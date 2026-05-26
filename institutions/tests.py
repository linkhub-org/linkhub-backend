from django.test import TestCase
from .models import Institution


class InstitutionTests(TestCase):

    # Cria instituição a partir de um e-mail novo
    def test_creates_institution_from_new_email(self):
        institution = Institution.get_or_create_from_email('guilherme@ufrn.br')
        self.assertEqual(institution.email_domain, 'ufrn.br')

    # Reutiliza instituição já existente
    def test_reuses_existing_institution(self):
        inst1 = Institution.get_or_create_from_email('guilherme@ufrn.br')
        inst2 = Institution.get_or_create_from_email('kaio@ufrn.br')
        self.assertEqual(inst1.pk, inst2.pk)

    # E-mails de domínios diferentes geram instituições diferentes
    def test_different_domains_create_different_institutions(self):
        inst1 = Institution.get_or_create_from_email('guilherme@ufrn.br')
        inst2 = Institution.get_or_create_from_email('outro@ufpb.br')
        self.assertNotEqual(inst1.pk, inst2.pk)
