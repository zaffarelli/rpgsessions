# Work in progress


class WednesdayMessenger(object):
    def get_suitable_profiles(self):
        from scheduler.models.profile import Profile
        suitable = Profile.objects.get(mail_wednesday=True)
        for p in suitable:
            p.processed = False
            p.save()
        return suitable

    def perform(self):
        all = self.get_suitable_profiles()
        for p in all:
            p.fetch_week_sessions()



WednesdayMessenger().perform()
