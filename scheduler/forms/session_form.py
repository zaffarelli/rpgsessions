from django import forms
from scheduler.models.session import Session
from django.utils.translation import gettext_lazy as _


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'description', 'game', 'campaign', 'optional_spots', 'time_start', 'duration', 'place',
                  'one_shot_adventure', 'newbies_allowed']
        labels = {
            'title': _('Titre'),
            'game': _('Jeu'),
            'campaign': _('Campagne'),
            # 'wanted': _('Joueurs Sollicités'),
            'optional_spots': _('Joueurs'),
            'time_start': _('Heure de début'),
            'duration': _('Durée'),
            'one_shot_adventure': _('Séance "Oneshot"'),
            'place': _('Lieu de la partie'),
            'newbies_allowed': _('Partie Initiation'),
        }
        help_texts = {
            'title': _("Alors oui je sais c'est petit mais le but c'est de ne pas prendre trop de place... :-)"),
            'game': _('Le jeu de rôle et système de règle de la partie. Si vous ne trouvez pas, choisissez Autre, je reviendrai vers vous...'),
            'campaign': _('Campagne associée. Laisser vide dans le doute.'),
            'optional_spots': _("Si vous n'avez pas de joueurs sollicités, ceci est le nombre total de joueurs. Les deux peuvent se combien: 3 joueurs sollicité et une place dispo par exemple.")


        }