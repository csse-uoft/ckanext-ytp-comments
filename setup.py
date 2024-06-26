from setuptools import setup, find_packages

version = '0.0'

setup(
    name='ckanext-ytp-comments',
    version=version,
    description="",
    long_description='''
    ''',
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    # package_data={'': ['./**/*.html', './**/*.txt', './**/*.css', '*/i18n/**/*']},
    namespace_packages=['ckanext', 'ckanext.ytp', 'ckanext.ytp.comments'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # CKAN extensions should not list dependencies here, but in a separate
        # ``requirements.txt`` file.
        #
        # http://docs.ckan.org/en/latest/extensions/best-practices.html
        # add-third-party-libraries-to-requirements-txt
    ],
    message_extractors={
        'ckanext/ytp/comments': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('templates/**.html', 'ckan', None)
        ]
    },
    entry_points='''
        [ckan.plugins]
        ytp_comments=ckanext.ytp.comments.plugin:YtpCommentsPlugin

        [paste.paster_command]
        initdb = ckanext.ytp.comments.command:InitDBCommand
        
        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
    ''',
)
