| Role         | GET List                              | GET Detail | PUT/PATCH | DELETE                        |
| ------------ | ------------------------------------- | ---------- | --------- | ----------------------------- |
| **Admin**    | All users                             | All users  | All users | All except self               |
| **Staff**    | Only users sharing at least one group | Same       | Same      | Same, but cannot delete admin |
| **Standard** | Only users sharing at least one group | Same       | Only self | Only self                     |

admin cannot delete itself, must be downgraded

Invece di scrivere un test per ogni view/metodo/utente, puoi parametrizzare i test:
import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
@pytest.mark.parametrize("username, url_name, method, expected_status", [
    ("admin", "user_list", "get", 200),
    ("staff", "user_list", "get", 200),
    ("normal", "user_list", "get", 200),
    ("admin", "user_delete", "post", 302),
    ("staff", "user_delete", "post", 403),
])
def test_user_views(client, django_user_model, username, url_name, method, expected_status):
    # Crea utenti con ruoli diversi
    if username == "admin":
        user = django_user_model.objects.create_superuser("admin", "a@a.com", "pass")
    elif username == "staff":
        user = django_user_model.objects.create_user("staff", "s@s.com", "pass", is_staff=True)
    else:
        user = django_user_model.objects.create_user("normal", "n@n.com", "pass")

    client.force_login(user)
    url = reverse(url_name, kwargs={"pk": 1} if "delete" in url_name else {})
    response = getattr(client, method.lower())(url)
    assert response.status_code == expected_status


Con factory_boy puoi generare utenti o oggetti modello senza scrivere il setup ogni volta:
import factory
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    is_staff = False
    is_superuser = False

Puoi scrivere un test generico parametrizzato per tutte le view di un modello usando un dizionario di configurazione:
TESTS = [
    {"url_name": "user_list", "methods": ["get"], "allowed": ["admin", "staff", "normal"]},
    {"url_name": "user_delete", "methods": ["post"], "allowed": ["admin"]},
    {"url_name": "user_update", "methods": ["post"], "allowed": ["admin", "staff"]},
]

@pytest.mark.django_db
@pytest.mark.parametrize("test_case", TESTS)
@pytest.mark.parametrize("username, role", [("admin", "superuser"), ("staff", "staff"), ("normal", "normal")])
def test_generic_user_views(client, django_user_model, test_case, username, role):
    if role == "superuser":
        user = django_user_model.objects.create_superuser(username, f"{username}@a.com", "pass")
    elif role == "staff":
        user = django_user_model.objects.create_user(username, f"{username}@s.com", "pass", is_staff=True)
    else:
        user = django_user_model.objects.create_user(username, f"{username}@n.com", "pass")

    client.force_login(user)
    url = reverse(test_case["url_name"], kwargs={"pk": 1} if "delete" in test_case["url_name"] else {})
    
    for method in test_case["methods"]:
        response = getattr(client, method)(url)
        if username in test_case["allowed"]:
            assert response.status_code in [200, 302]
        else:
            assert response.status_code in [403, 404]


Puoi creare fixture per DRY:
@pytest.fixture
def admin_user(db, django_user_model):
    return django_user_model.objects.create_superuser("admin", "admin@test.com", "pass")

@pytest.fixture
def staff_user(db, django_user_model):
    return django_user_model.objects.create_user("staff", "staff@test.com", "pass", is_staff=True)

@pytest.fixture
def normal_user(db, django_user_model):
    return django_user_model.objects.create_user("normal", "normal@test.com", "pass")


def test_list(client, admin_user, staff_user, normal_user):
    for user in [admin_user, staff_user, normal_user]:
        client.force_login(user)
        response = client.get(reverse("user_list"))
        assert response.status_code == 200



💡 In sintesi:

Parametrizza i test con pytest.mark.parametrize

Usa fixture o factory per creare utenti e dati modello

Usa dizionari di configurazione per le view CRUD → test generici

Così puoi testare tutte le combinazioni di utenti/metodi/URL senza scrivere decine di funzioni
