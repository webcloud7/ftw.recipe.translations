from ftw.recipe.translations import discovery
from ftw.recipe.translations.discovery import discover_package
from ftw.recipe.translations.utils import chdir
from ftw.recipe.translations.writer import cleanup_pofile
from i18ndude.catalog import MessageCatalog
from i18ndude.catalog import POWriter
from path import Path
from six.moves import map
import i18ndude.script
import os.path
import sys

class Arguments(dict):
    def __init__(self, *args, **kwargs):
        super(Arguments, self).__init__(*args, **kwargs)
        self.__dict__ = self


def rebuild_package_potfiles(package_root, package_dir, primary_domain):
    for group in discover_package(package_dir, None):
        if group['domain'] != primary_domain:
            continue

        manual = ''
        if group['manual']:
            manual = os.path.join(package_dir, group['manual'])

        content = ''
        if group['content']:
            content = os.path.join(package_dir, group['content'])

        potpath = os.path.join(package_dir, group['pot'])
        rebuild_pot(package_root, package_dir, primary_domain, potpath,
                    manual, content)


def rebuild_pot(package_root, package_dir, domain, potpath, manual, content):
    print('Rebuilding ')
    print(potpath)
    relative_path = Path(package_dir).relpath(package_root)
    if relative_path != '.':
        relative_path = os.path.join('.', relative_path)
    arguments = Arguments({'pot_fn': potpath,
                           'create_domain': domain,
                           'path': [relative_path],
                           'exclude': '',
                           'merge_fn': manual,
                           'merge2_fn': content})

    with chdir(package_root):
        try:
            i18ndude.script.rebuild_pot(arguments)
        except SystemExit:
            pass
        cleanup_pofile(potpath)


def sync_package_pofiles(package_dir, languages):
    for group in discovery.discover_package(package_dir):
        if not group['pot']:
            continue

        langs = list(group['languages'].keys())
        if languages:
            langs += languages
        sync_pofile_group(package_dir, group, langs)


def sync_pofiles(sources_directory, languages):
    for group in discovery.discover(sources_directory):
        if not group['pot']:
            continue

        sync_pofile_group(sources_directory, group, languages)


def sync_pofile_group(base_dir, group, languages):
    pofiles = []
    for lang, popath in group['languages'].items():
        if languages is not None and lang not in languages:
            continue
        pofiles.append(os.path.join(base_dir,
                                    group['package'] or '',
                                    popath))

    for lang in set(languages or []) - set(group['languages'].keys()):
        path = os.path.join(base_dir,
                            group['package'] or '',
                            group['locales'],
                            lang,
                            'LC_MESSAGES',
                            '%s.po' % group['domain'])
        create_new_pofile(path, group['domain'])
        pofiles.append(path)

    potpath = os.path.join(base_dir,
                           group['package'] or '',
                           group['pot'])

    arguments = Arguments({'pot_fn': potpath.encode('utf-8'),
                           'files': pofiles})
    try:
        i18ndude.script.sync(arguments)
    except SystemExit:
        pass
    list(map(cleanup_pofile, pofiles))


def create_new_pofile(path, domain):
    catalog = MessageCatalog(domain=domain)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'w+') as file_:
        POWriter(file_, catalog).write(msgstrToComment=False,
                                       sync=True)
