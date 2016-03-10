from setuptools import setup

extra = {}

try:
    from trac.util.dist  import  get_l10n_cmdclass
    cmdclass = get_l10n_cmdclass()
    if cmdclass:
        extra['cmdclass'] = cmdclass
        extractors = [
#            ('**.py',                'python', None),
#            ('**/templates/**.html', 'genshi', None),
        ]
        extra['message_extractors'] = {
            'mainnavsubmenu': extractors,
        }
except:
    pass

setup(
    name='TracMainNavSubMenuPlugin',
    #description='',
    #keywords='',
    #url='',
    version='0.1',
    #license='',
    #author='',
    #author_email='',
    #long_description="",
    packages=['mainnavsubmenu'],
    package_data={
        'mainnavsubmenu': [
            'htdocs/css/*.css',
#            'templates/*.html',
#            'locale/*/LC_MESSAGES/*.mo',
        ]
    },
    entry_points={
        'trac.plugins': [
            'mainnavsubmenu.web_ui = mainnavsubmenu.web_ui',
        ]
    },
#    **extra
)
