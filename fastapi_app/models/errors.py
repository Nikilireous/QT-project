class SiteExistingError(Exception):
    def __str__(self):
        return 'Site with this address is already exist'
