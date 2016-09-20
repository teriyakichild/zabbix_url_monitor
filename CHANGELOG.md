## 1.1.3-1 (Sep 19 2016)

Feature:

  - Add support for using custom zabbix host name. (#20, @jonkelleyatrackspace)
  - Rename zabbix: host to zabbix: server, to make room for new feature. (#20, @jonkelleyatrackspace)

## 1.1.2-2 (Sep 16 2016)

Feature:

  - Adding an stdout message to print the worst return status code seen for a particular set of check(s). (@jonkelleyatrackspace)
  - Change output info message to only appear in debug, to limit confusion for the status code evaluation. (@jonkelleyatrackspace)

## 1.1.0-1 (Jul 27 2016)

Bugfixes:

  - Fix the --key flag for selective run. (@jonkelleyatrackspace)
  - Fix the yaml configuration file to meet YAML spec. (@jonkelleyatrackspace)

Docs:

  - Update readme to match new configs (@jonkelleyatrackspace)

## 1.0.2-1 (Jul 27 2016)

Cleanup:

  - Remove misreferenced packaging import(s) (@jonkelleyatrackspace)
  - Remove {url} from epilog output (@jonkelleyatrackspace)
  - Remove __author__ from __init__ (@jonkelleyatrackspace)

Bugfixes:

  - Make zbx_send timeouts cast into float() from configparser (@jonkelleyatrackspace)
  - Fix a missing ) in the config parser. (@jonkelleyatrackspace)

## 1.0.0-1 (Jul 18 2016)

Bugfixes:

  - Fix a bug where missing variable from packaging.py (@jonkelleyatrackspace)

## 0.9.0-1 (Jul 10 2016)

Bugfixes:

  - Added forked process for non interrupting io from zabbix. (@jonkelleyatrackspace)
  - Many other improvements (@jonkelleyatrackspace)

## 0.8.5-1 (Apr 29 2016)

Bugfixes:

  - Fixes to work better when singleton doesnt take, like on py2.6 (@jonkelleyatrackspace)
