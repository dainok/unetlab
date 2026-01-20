"""
Create demo data using Django Shell.

Usage:

poetry run ./manage.py shell < tests/demo_data.py
"""

import random
import yaml
from pathlib import Path
from django.conf import settings
from django.contrib.auth.models import Group, User

# from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from lab.models import Lab
from task.models import Task, Log


# Drop data
Token.objects.all().delete()
Group.objects.all().delete()
User.objects.all().exclude(username='admin').delete()
Lab.objects.all().delete()


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        pass
    return None


USERS = [
    {'first_name': 'Luca', 'last_name': 'Rinaldi'},
    {'first_name': 'Giulia', 'last_name': 'Ferraro'},
    {'first_name': 'Marco', 'last_name': 'Gentile'},
    {'first_name': 'Sara', 'last_name': 'Colombo'},
    {'first_name': 'Andrea', 'last_name': 'De Angelis'},
    {'first_name': 'Chiara', 'last_name': 'Barbieri'},
    {'first_name': 'Matteo', 'last_name': 'Fabbri'},
    {'first_name': 'Elisa', 'last_name': 'Fontana'},
    {'first_name': 'Davide', 'last_name': 'Ferretti'},
    {'first_name': 'Francesca', 'last_name': 'Monti'},
    {'first_name': 'Simone', 'last_name': 'Villa'},
    {'first_name': 'Martina', 'last_name': 'Santoro'},
    {'first_name': 'Giorgio', 'last_name': 'Moretti'},
    {'first_name': 'Alessia', 'last_name': 'Lombardi'},
    {'first_name': 'Stefano', 'last_name': 'Pellegrini'},
    {'first_name': 'Valentina', 'last_name': 'Grassi'},
    {'first_name': 'Federico', 'last_name': 'Serra'},
    {'first_name': 'Silvia', 'last_name': 'Martelli'},
    {'first_name': 'Riccardo', 'last_name': 'Caruso'},
    {'first_name': 'Ilaria', 'last_name': 'Caputo'},
    {'first_name': 'Daniele', 'last_name': 'Gatti'},
    {'first_name': 'Roberta', 'last_name': 'Farina'},
    {'first_name': 'Tommaso', 'last_name': 'Bellini'},
    {'first_name': 'Veronica', 'last_name': 'Conte'},
    {'first_name': 'Alessandro', 'last_name': 'Marino'},
    {'first_name': 'Serena', 'last_name': 'Basile'},
    {'first_name': 'Paolo', 'last_name': 'Rizzo'},
    {'first_name': 'Elena', 'last_name': 'Giordani'},
    {'first_name': 'Gabriele', 'last_name': 'De Luca'},
    {'first_name': 'Laura', 'last_name': 'Longo'},
    {'first_name': 'Pietro', 'last_name': 'Milani'},
    {'first_name': 'Beatrice', 'last_name': 'Ferrari'},
    {'first_name': 'Nicola', 'last_name': 'Rossetti'},
    {'first_name': 'Camilla', 'last_name': 'Palmieri'},
    {'first_name': 'Antonio', 'last_name': 'Fiore'},
    {'first_name': 'Marta', 'last_name': 'Negri'},
    {'first_name': 'Emanuele', 'last_name': 'Marchetti'},
    {'first_name': 'Noemi', 'last_name': 'Costantini'},
    {'first_name': 'Cristian', 'last_name': 'Sartori'},
    {'first_name': 'Alice', 'last_name': 'Coppola'},
    {'first_name': 'Lorenzo', 'last_name': 'Piras'},
    {'first_name': 'Federica', 'last_name': 'Montanari'},
    {'first_name': 'Salvatore', 'last_name': 'Pagani'},
    {'first_name': 'Gloria', 'last_name': 'Bruno'},
    {'first_name': 'Giovanni', 'last_name': 'Ruggeri'},
    {'first_name': 'Elena', 'last_name': 'Valente'},
    {'first_name': 'Cristina', 'last_name': 'Leone'},
    {'first_name': 'Edoardo', 'last_name': 'Giuliani'},
    {'first_name': 'Angela', 'last_name': 'Cattaneo'},
    {'first_name': 'Vincenzo', 'last_name': 'Orlando'},
    {'first_name': 'Irene', 'last_name': 'Riva'},
    {'first_name': 'Fabio', 'last_name': 'Sanna'},
    {'first_name': 'Michela', 'last_name': 'Gallo'},
    {'first_name': 'Samuel', 'last_name': 'Montagna'},
    {'first_name': 'Chiara', 'last_name': 'Bernardi'},
    {'first_name': 'Christian', 'last_name': 'De Rosa'},
    {'first_name': 'Emma', 'last_name': 'Bianco'},
    {'first_name': 'Diego', 'last_name': 'Vitali'},
    {'first_name': 'Rachele', 'last_name': 'Cortesi'},
    {'first_name': 'Gianluca', 'last_name': 'Testa'},
    {'first_name': 'Arianna', 'last_name': 'Savini'},
    {'first_name': 'Luigi', 'last_name': 'Puglisi'},
    {'first_name': 'Greta', 'last_name': 'Amato'},
    {'first_name': 'Alberto', 'last_name': 'Mancini'},
    {'first_name': 'Nicole', 'last_name': 'Battaglia'},
    {'first_name': 'Raffaele', 'last_name': 'Locatelli'},
    {'first_name': 'Elisabetta', 'last_name': 'Viviani'},
    {'first_name': 'Massimo', 'last_name': 'Pace'},
    {'first_name': 'Sofia', 'last_name': 'Silvestri'},
    {'first_name': 'Jacopo', 'last_name': 'Palmieri'},
    {'first_name': 'Giada', 'last_name': 'Magnani'},
    {'first_name': 'Filippo', 'last_name': 'Mariani'},
    {'first_name': 'Linda', 'last_name': 'Bianchi'},
    {'first_name': 'Samuele', 'last_name': 'Giuliani'},
    {'first_name': 'Maddalena', 'last_name': 'Amoroso'},
    {'first_name': 'Enrico', 'last_name': 'Valentini'},
    {'first_name': 'Claudia', 'last_name': 'De Santis'},
    {'first_name': 'Jonathan', 'last_name': 'Guerra'},
    {'first_name': 'Allegra', 'last_name': 'Ruggero'},
    {'first_name': 'Mirko', 'last_name': 'Lodi'},
    {'first_name': 'Rebecca', 'last_name': 'Pozzi'},
    {'first_name': 'Kevin', 'last_name': 'Benedetti'},
    {'first_name': 'Celeste', 'last_name': 'Rinaldo'},
    {'first_name': 'Tiziano', 'last_name': 'Borelli'},
    {'first_name': 'Gaia', 'last_name': 'Guidi'},
    {'first_name': 'Dario', 'last_name': 'Carlucci'},
    {'first_name': 'Sara', 'last_name': 'Cattaneo'},
    {'first_name': 'Mirco', 'last_name': 'Ferrante'},
    {'first_name': 'Agnese', 'last_name': 'Bellotti'},
    {'first_name': 'Ivan', 'last_name': 'Silva'},
    {'first_name': 'Melania', 'last_name': 'Pinto'},
    {'first_name': 'Alan', 'last_name': 'Pellegrino'},
    {'first_name': 'Vittoria', 'last_name': 'Rocca'},
    {'first_name': 'Omar', 'last_name': 'Catalano'},
    {'first_name': 'Erika', 'last_name': 'Biagini'},
    {'first_name': 'Sebastiano', 'last_name': 'Testoni'},
    {'first_name': 'Elena', 'last_name': 'Trevisan'},
    {'first_name': 'Giacomo', 'last_name': 'Mazzoleni'},
    {'first_name': 'Miriam', 'last_name': 'Sala'},
    {'first_name': 'Franco', 'last_name': 'Romano'},
    {'first_name': 'Adele', 'last_name': 'Mauri'},
    {'first_name': 'Matias', 'last_name': 'Colucci'},
    {'first_name': 'Aurora', 'last_name': 'Liguori'},
    {'first_name': 'Renato', 'last_name': 'Esposito'},
    {'first_name': 'Nadia', 'last_name': 'Torrisi'},
    {'first_name': 'Gianmarco', 'last_name': 'Pellegrino'},
    {'first_name': 'Monica', 'last_name': 'Vannini'},
    {'first_name': 'Stefania', 'last_name': 'Morelli'},
    {'first_name': 'Angelo', 'last_name': 'Serafini'},
    {'first_name': 'Diletta', 'last_name': 'Barone'},
    {'first_name': 'Alessio', 'last_name': 'Mazzanti'},
    {'first_name': 'Priscilla', 'last_name': 'Carbone'},
    {'first_name': 'Ruben', 'last_name': 'Marcello'},
    {'first_name': 'Eleonora', 'last_name': 'Lucchesi'},
    {'first_name': 'Claudio', 'last_name': 'Neri'},
    {'first_name': 'Carolina', 'last_name': 'Rizzi'},
    {'first_name': 'Maurizio', 'last_name': 'Fiorelli'},
    {'first_name': 'Bianca', 'last_name': 'Bassi'},
    {'first_name': 'Ettore', 'last_name': 'Martino'},
    {'first_name': 'Letizia', 'last_name': 'Bolognese'},
    {'first_name': 'Bruno', 'last_name': 'Sorrentino'},
    {'first_name': 'Fabiola', 'last_name': 'Vecchi'},
    {'first_name': 'Nicolò', 'last_name': 'De Carlo'},
    {'first_name': 'Giovanna', 'last_name': 'Basili'},
    {'first_name': 'Samir', 'last_name': 'Greco'},
    {'first_name': 'Anita', 'last_name': 'Bertoni'},
    {'first_name': 'Fabrizio', 'last_name': 'Romanelli'},
    {'first_name': 'Caterina', 'last_name': 'Spada'},
    {'first_name': 'Rocco', 'last_name': "D'Amico"},
    {'first_name': 'Asia', 'last_name': 'Pagliarini'},
    {'first_name': 'Mattia', 'last_name': 'Toma'},
    {'first_name': 'Nina', 'last_name': 'Ranieri'},
    {'first_name': 'Giulio', 'last_name': 'Casadei'},
    {'first_name': 'Iris', 'last_name': 'Bassi'},
    {'first_name': 'Adriano', 'last_name': 'Pizzocchi'},
    {'first_name': 'Elisa', 'last_name': 'Lanzoni'},
    {'first_name': 'Enea', 'last_name': 'Martelloni'},
    {'first_name': 'Tecla', 'last_name': 'Fossati'},
    {'first_name': 'Rinaldo', 'last_name': 'Zanetti'},
    {'first_name': 'Fiona', 'last_name': 'Arduini'},
    {'first_name': 'Marcello', 'last_name': 'Dal Maso'},
    {'first_name': 'Giorgia', 'last_name': 'Migliore'},
    {'first_name': 'Sergio', 'last_name': 'Bertolotti'},
    {'first_name': 'Vera', 'last_name': 'Coccia'},
    {'first_name': 'Walter', 'last_name': 'Bellucci'},
    {'first_name': 'Erica', 'last_name': 'Giorgetti'},
    {'first_name': 'Loris', 'last_name': 'Caracciolo'},
    {'first_name': 'Margherita', 'last_name': 'Grasso'},
    {'first_name': 'Eliot', 'last_name': 'Bassi'},
    {'first_name': 'Nora', 'last_name': 'Sabelli'},
    {'first_name': 'Kevin', 'last_name': 'Vitali'},
    {'first_name': 'Azzurra', 'last_name': 'Fornaciari'},
    {'first_name': 'Leonardo', 'last_name': 'Benetti'},
    {'first_name': 'Viola', 'last_name': 'Cialdini'},
    {'first_name': 'Gianpaolo', 'last_name': 'Farinelli'},
    {'first_name': 'Paola', 'last_name': 'Nobili'},
    {'first_name': 'Carlo', 'last_name': 'Borghi'},
    {'first_name': 'Rossella', 'last_name': 'Pecoraro'},
    {'first_name': 'Amos', 'last_name': 'Rispoli'},
    {'first_name': 'Eleonora', 'last_name': 'Gionta'},
    {'first_name': 'Graziano', 'last_name': 'Pisano'},
    {'first_name': 'Susanna', 'last_name': 'Scotti'},
    {'first_name': 'Ivan', 'last_name': 'Zanni'},
    {'first_name': 'Lavinia', 'last_name': 'Scarpati'},
    {'first_name': 'Carlo', 'last_name': 'Montesi'},
    {'first_name': 'Eva', 'last_name': 'Perri'},
    {'first_name': 'Domenico', 'last_name': 'Moscati'},
    {'first_name': 'Lara', 'last_name': 'Corsi'},
    {'first_name': 'Santo', 'last_name': 'Donati'},
    {'first_name': 'Nadia', 'last_name': 'Gori'},
    {'first_name': 'Elio', 'last_name': 'Baldini'},
    {'first_name': 'Flavia', 'last_name': 'Pecchioli'},
    {'first_name': 'Mauro', 'last_name': 'Orsini'},
    {'first_name': 'Giulia', 'last_name': 'Vassallo'},
    {'first_name': 'Rudi', 'last_name': 'Pennacchi'},
    {'first_name': 'Clara', 'last_name': 'Saponaro'},
    {'first_name': 'Tito', 'last_name': 'Roveri'},
    {'first_name': 'Elma', 'last_name': 'Morese'},
    {'first_name': 'Gualtiero', 'last_name': 'Poli'},
    {'first_name': 'Isabella', 'last_name': 'Sanna'},
    {'first_name': 'Osvaldo', 'last_name': 'Gambino'},
    {'first_name': 'Mirella', 'last_name': 'Luciani'},
]

FIRMS = [
    'TechNova Solutions',
    'BlueWave Networks',
    'GreenLogic Systems',
    'NextPhase Robotics',
    'FusionSoft Labs',
    'CloudBridge Technologies',
    'QuantumEdge Analytics',
    'IronGate Security',
    'Solaris Engineering',
    'PixelForge Media',
    'Skyline Consulting',
    'DeepCore Innovations',
    'SilverPeak Industries',
    'HyperLink Digital',
    'NeoGrid Software',
    'EverFlow Energy',
    'OmniData Solutions',
    'UrbanHive Architecture',
    'AquaSphere Research',
    'BrightPath Healthcare',
]


# Create superuser
admin_obj = get_or_none(User, username='admin')
if not admin_obj:
    admin_obj = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
    admin_obj.full_clean()


# Create groups
group_list = []
for firm in FIRMS:
    group = Group.objects.create(name=firm)
    group.full_clean()
    group_list.append(group)


# Create users
user_list = []
# password_hash = make_password("password")
password_hash = 'pbkdf2_sha256$1000000$eF2L5tYyTWTEro6dJaU9HS$n7JgU23uuRDpd+6ko7Zpd+UYpdRQhFLw9gvu945iGCU='
for user in USERS:
    username = f'{user["first_name"][0]}{user["last_name"]}'.replace("'", '').replace(' ', '').lower()
    role_id = random.randint(0, 2)
    is_admin = True if role_id == 0 else False
    is_staff = True if is_admin or role_id == 1 else False
    is_active = bool(random.randint(0, 1))
    payload = {
        'username': username,
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'email': f'{username}@example.com',
        'is_superuser': is_admin,
        'is_staff': is_staff,
        'is_active': is_active,
        'password': password_hash,
    }
    user_obj = User.objects.create(**payload)
    user_obj.full_clean()
    user_list.append(user_obj)
    Token.objects.create(user=user_obj)
    groups_obj = []
    for group in range(0, 3):
        firm_id = random.randint(0, 19)
        groups_obj.append(Group.objects.get(name=FIRMS[firm_id]))
    user_obj.groups.set(groups_obj)
    user_obj.save()


# Create labs
hld_dir = Path(settings.BASE_DIR) / 'tests' / 'lab' / 'hld'
hld_files = sorted(hld_dir.glob('hld-*.yml'))
lab_list = []
for ver in range(0, 2):
    for user_obj in user_list:
        hld_id = random.randint(0, len(hld_files) - 1)
        name = f'Lab {" ".join(hld_files[hld_id].stem.split("-")[2:])} by {user_obj.username} v{ver}'
        with open(hld_files[hld_id], encoding='utf-8') as fh:
            hld = yaml.safe_load(fh)
        payload = {
            'name': name,
            'hld': hld,
            'user': user_obj,
        }
        lab_obj = Lab.objects.create(**payload)
        lab_obj.full_clean()
        lab_list.append(lab_obj)
        if bool(random.randint(0, 1)):
            lab_obj.shared_group = group_list[random.randint(0, 19)]
            lab_obj.save()


# Create tasks and logs
for user_obj in user_list:
    for task_count in range(1, 5):
        task_obj = Task.objects.create(name=f'Task {task_count}', user=user_obj)
        for log_count in range(1, 5):
            Log.objects.create(
                task=task_obj,
                message=f"Log {log_count}",
                severity=30,
                hostname="test",
                type="APP",
            )
