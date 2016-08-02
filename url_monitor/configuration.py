#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import socket

import yaml

import logging.handlers
import commons

from url_monitor import package as packagemacro

class ConfigObject(object):
    """ This class makes YAML configuration
    available as python datastructure. """

    def __init__(self):
        self.config = None
        self.checks = None
        self.constant_syslog_port = 514

    def load_yaml_file(self, config=None):
        """

        :param config:
        :return:
        """
        if config == None:
            config = "/etc/url_monitor.yaml"

        with open(config, 'r') as stream:
            try:
                self.config = (yaml.load(stream))
                return self.config
            except yaml.YAMLError as exc:
                print(exc)

    def load(self):
        """ This is the main config load function to pull in
            configurations to convienent and common namespace. """
        return {'checks': self._load_checks(),
                'config': self._load_config(),
                'identity_providers': self._load_config_identity_providers()}

    def _load_checks(self, withIdentityProvider=None):
        """ Loads the checks for work to be run.
            Default loads all checks, withIdentityProvider option will limit checks
            returned by identity provider (useful for smart async request grouping)  """
        loaded_checks = []

        if withIdentityProvider:
            # Useful if doing grouping async requests with a shared identityprovider
            #  and then spawning async call
            for checkdata in self._load_test_set_list():
                if checkdata['data']['identity_provider'].lower() == withIdentityProvider.lower():
                    # loaded_checks.append({'data': checkdata['data']})
                    loaded_checks.append(checkdata)

        else:
            loaded_checks = self._load_test_set_list()

        return loaded_checks

    def _load_config(self):
        """ Return base config key """
        return self.config['config']

    def _load_config_identity_providers(self):
        """ This fetches out a list of identity providers kwarg configs from main config """
        providers = {}
        for provider_config_alias, v in self._load_config()['identity_providers'].iteritems():
            # Add each provider and config to dictionary from yaml file.
            providers[provider_config_alias] = v
        # Return a list of the config
        return providers

        """ Loads a list of the checks """

    def _uniq(self, seq):
        """ Returns a unique list when a list of
         non unique items are put in """
        set = {}
        map(set.__setitem__, seq, [])
        return set.keys()

    def get_datatypes_list(self):
        """ Used by the discover command to identify a list of valid datatypes """
        exception_string = (
            "Error: Missing {error} under testSet item {test_set}, "
            "discover cannot run."
        )

        possible_datatypes = []
        for testSet in self._load_checks():
            checkname = testSet['key']
            try:
                uri = testSet['data']['uri']
            except KeyError as err:
                error = exception_string.format(
                    error=err,
                    test_set=testSet['key']
                )
                raise Exception("KeyError: " + str(err) + str(error))

            try:
                testSet['data']['testElements']
            except KeyError as err:
                error = exception_string.format(
                    error=err,
                    test_set=testSet['key']
                )
                raise Exception("KeyError: " + str(err) + str(error))

            for element in testSet['data']['testElements']:  # For every test element
                try:
                    datatypes = element['datatype'].split(',')
                except KeyError as err:
                    error = exception_string.format(
                        error=err,
                        test_set=testSet['key']
                    )
                    raise Exception("KeyError: " + str(err) + str(error))
                for datatype in datatypes:
                    possible_datatypes.append(datatype)

        return str(self._uniq(possible_datatypes))

    def get_log_level(self, debug_level=None):
        """ Allow user-configurable log-leveling """
        try:
            if debug_level == None:
                debug_level = self.config['config']['logging']['level']
        except KeyError as err:
            print("Error: Missing " + str(err) +
                  " in config under config: loglevel.\nTry config: loglevel: Exceptions")
            print("1")
            exit(1)
        if (debug_level.lower().startswith('err') or debug_level.lower().startswith('exc')):
            return logging.ERROR
        elif debug_level.lower().startswith('crit'):
            return logging.CRITICAL
        elif debug_level.lower().startswith('warn'):
            return logging.WARNING
        elif debug_level.lower().startswith('info'):
            return logging.INFO
        elif debug_level.lower().startswith('debu'):
            return logging.DEBUG
        else:
            return logging.ERROR

    def get_logger(self, loglevel):
        """ Returns a logger instance, used throughout codebase.
            This will set up a logger using syslog or file logging (or both)
            depending on the setting used in configuration.

            This supports two types of logging options
            One by file:
              logging:
                level: debug
                outputs: file
                logfile: /var/log/url_monitor.log
                logformat: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

            One by syslog:
              logging:
                level: debug
                outputs: syslog
                syslog:
                    server: 127.0.0.1:514
                    socket: tcp
                logformat: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

            You can also enable both by setting outputs with commas.
        """
        try:  # Basic config lint
            self.config['config']['logging']['outputs']
            self.config['config']['logging']['level']
            self.config['config']['logging']['logformat']
        except KeyError, err:
            error =  """KeyError missing {err} structure under config property. Ensure `config: {err}:` is defined. Can't continue.""".format(
                err=err)
            logging.exception(error)
            exit(1)

        self.logger = logging.getLogger(packagemacro)
        loglevel = self.get_log_level(loglevel)
        formatter = logging.Formatter(
            self.config['config']['logging']['logformat'])

        log_outputs = self.config['config']['logging']['outputs'].split(',')

        if "file" in log_outputs:
            # Add handler for file outputs
            try:  # Quick validation
                filehandler = logging.FileHandler(
                    self.config['config']['logging']['logfile'])
            except KeyError, err:
                error =  """KeyError missing {err} structure under config property. Ensure `config: {err}:` is defined. Can't continue.""".format(
                    err=err)
                exit(1)
            filehandler.setLevel(loglevel)
            self.logger.addHandler(filehandler)
            filehandler.setFormatter(formatter)

        if "syslog" in log_outputs:
            # Add handler for syslog outputs

            try:  # Quick validation
                self.config['config']['logging']['syslog']
                self.config['config']['logging']['syslog']['server']
                self.config['config']['logging']['syslog']['socket']
            except KeyError, err:
                error =  """KeyError missing {err} structure under config property. Ensure `config: {err}:` is defined. Can't continue.""".format(
                    err=err)
                logging.exception(error)
                exit(1)
            sysloghost = commons.get_hostport_tuple(dport=self.constant_syslog_port, dhost=self.config[
                'config']['logging']['syslog']['server'])

            socktype = self.config['config']['logging']['syslog']['socket']
            if socktype == "tcp":
                socktype = socket.SOCK_STREAM
            else:
                socktype = socket.SOCK_DGRAM

            try:
                sysloghandler = logging.handlers.SysLogHandler(
                    address=sysloghost, socktype=socktype)
                sysloghandler.setLevel(loglevel)
                self.logger.addHandler(sysloghandler)
                sysloghandler.setFormatter(formatter)
            except socket.error, err:
                error =  """Syslog error with socket.write() on host {h}:{p} {err}""".format(
                    err=err, h=sysloghost[0], p=sysloghost[1])
                logging.exception(error)

        logging.basicConfig(level=loglevel)
        self.logger.info("Logger initialized.")
        return self.logger

    def pre_flight_check(self):
        """ Trys loading all the config objects for zabbix conf. This can be expanded to do
            all syntax checking in this config class, instead of in the program logic as it is
            mostly right now.

            It is a check class. This should NOT be used for program references.
            (Doesnt use logger for exceptions as it pre-dates logger instanciation.)
            """
        # Ensure base config elements exist.
        try:
            self.config['config']
        except KeyError, err:
            error =  """KeyError configs missing `zabbix: {err}` structure. Can't continue.""".format(
                err=err)
            logging.exception(error)
            exit(1)

        try:
            self.config['config']['zabbix']
        except KeyError, err:
            error =  """KeyError configs missing `zabbix: {err}` structure. Can't continue.""".format(
                err=err)
            logging.exception(error)
            exit(1)

        try:
            self.config['config']['zabbix']['host']
            self.config['config']['zabbix']['send_timeout']
            self.config['config']['zabbix']['item_key_format']
        except KeyError, err:
            error =  """KeyError configs missing `config: zabbix: {err}:` structure. Can't continue.""".format(
                err=err)
            logging.exception(error)
            exit(1)

        try:
            self.config['config']['request_timeout']
        except KeyError, err:
            error =  """KeyError configs missing `config: config: {err}:` structure. (Default timeout missing) Can't continue.""".format(
                err=err)
            logging.exception(error)
            exit(1)

        # Ensure identity items exist
        try:
            self.config['config']['identity_providers']
        except KeyError, err:
            error =  """KeyError configs missing `config: config: {err}:` structure. (Identity Providers) Can't continue.""".format(
                err=err)
            logging.exception(error)
            exit(1)

        try:
            for provider in self._load_config_identity_providers():
                provider
        except AttributeError, err:
            error =  """KeyError configs missing {err} structure in `config: identity_providers`. Can't continue.""".format(
                err=err)
            logging.exception(error)
            exit(1)

        for provider in self._load_config_identity_providers():
            provider
            for module, kwargs in self.config['config']['identity_providers'][provider].iteritems():
                module.split('/')
                for kwarg in kwargs:
                    kwarg

        self.logger.info("Pre-flight config test OK")

    def _load_test_set_list(self):
        """ Used to prepare format of data for the checker functions
        out of the configuration file.
        Here is a sample of return output.
        [
            { ...... 
            },
            { ......
            },
            {
                "data": {
                    "testElements": [
                        {
                            "datatype": "string", 
                            "jsonvalue": "status", 
                            "unit_of_measure": "events", 
                            "key": "zabbix_key", 
                            "metricname": "test"
                        }, 
                    ], 
                    "ok_http_code": 200, 
                    "response_type": "json", 
                    "identity_provider": "None", 
                    "keyname": null, 
                    "uri": "https://localhost"
                }, 
                "key": "keyname"
            }
        ]
        """
        self.checks = []

        for testSet in self.config['testSet']:
            for key, v in testSet.iteritems():
                if v == None:
                    self.checks.append({'key': key, 'data': testSet})

        return self.checks

if __name__ == "__main__":
    x = ConfigObject()
    x.load_yaml_file(config=None)
    a = x._load_checks()
    print(a)
    print(x.get_datatypes_list())
