from ftw.recipe.translations.i18ntools import rebuild_package_potfiles


def main(package_name, i18n_domain, package_namespace, package_directory):
    pass


def build_translations(buildout_directory, package_directory, i18n_domain,
                       new_languages=None):
    rebuild_inflator(package_directory, i18n_domain)
    rebuild_package_potfiles(package_directory, i18n_domain)
    sync_potfiles(package_directory, new_languages)


def rebuild_inflator(package_directory, i18n_domain):
    pass


def sync_potfiles(package_directory, new_languages=None):
    pass
