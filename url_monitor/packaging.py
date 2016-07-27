#!/usr/bin/python
# -*- coding: utf-8 -*-
__doc__ = """url_monitor

Extensible URL monitor that iterates through supplied json/yaml
files to pull remote data from fields in http, xml, or json
documents and sends data to remote sources.  To support zabbix,
Rackspace Cloud Monitoring, collectd, etc...
"""

# The package name, which is also the "UNIX name" for the project.
package = 'url_monitor'
project = "URL Monitor Module"
version = "1.0.1"
project_no_spaces = project.replace(' ', '')
description = (
    'A zabbix plugin to perform URL endpoint monitoring for JSON and XML REST '
    'APIs, supporting multiple http auth mechinisms'
)
long_description = (
    'A Zabbix plugin written in Python that creates low level discovery items '
    'containing values from your JSON API. It supports multiple requests auth '
    'backends including oauth, basicauth, and your even own custom requests '
    'auth provider plugins. The low level discovery items can generate item '
    'prototypes which can be used to represent your data through this plugin.'
)
authors = ['Jon Kelley', 'Nick Bales', 'Landon Jurgens']
authors_string = ', '.join(authors)
emails = ['jon.kelley@rackspace.com',
          'nick.bales@rackspace.com',
          'landon.jurgens@rackspace.com']
url = 'https://github.com/rackerlabs/zabbix_url_monitor'

