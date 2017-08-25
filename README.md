Table of Contents
=================

  * [Table of Contents](#table-of-contents)
  * [url_monitor](#url_monitor)
    * [Simple Installation](#simple-installation)
        * [Requirements](#requirements)
        * [Redhat install](#redhat-install)
        * [On other platforms](#on-other-platforms)
        * [Setup](#setup)
          * [Configuration](#configuration)
          * [Scheduling](#scheduling)
          * [Zabbix Template](#zabbix-template)
          * [Zabbix Triggers](#zabbix-triggers)
    * [<i></i> Basic Command Options](#-basic-command-options)
    * [<i></i>  Simple Plugin Usage on the CLI](#--simple-plugin-usage-on-the-cli)
      * [Running a check](#running-a-check)
      * [Return low level discovery items](#return-low-level-discovery-items)
    * [<i></i> Basic Configuration Options](#-basic-configuration-options)
      * [<i></i>Pidfile](#pidfile)
      * [<i></i>Skip Checks When](#skip-checks-when)
      * [<i></i>Network settings](#network-settings)
      * [<i></i>Log level](#log-level)
      * [<i></i>Auth/Identity Providers](#authidentity-providers)
      * [<i></i>Example of of an API testSet configuration](#example-of-of-an-api-testset-configuration)
          * [Test Elements](#test-elements)
      * [<i></i>Zabbix host config](#zabbix-host-config)
          * [item_key_format details](#item_key_format-details)
          * [checksummary_key_format details](#checksummary_key_format-details)
    * [<i></i>Complete Example](#complete-example)
      * [<i></i>Configure a webcheck in URL_monitor](#configure-a-webcheck-in-url_monitor)
      * [<i></i>Configure Zabbix UI](#configure-zabbix-ui)
        * [<i></i>Create Zabbix url_monitor template](#create-zabbix-url_monitor-template)
        * [<i></i>Configure low-level discovery in Zabbix UI](#configure-low-level-discovery-in-zabbix-ui)
        * [<i></i>Configure Item Prototypes in Zabbix UI](#configure-item-prototypes-in-zabbix-ui)
        * [<i></i>Configure basic triggers in Zabbix UI](#configure-basic-triggers-in-zabbix-ui)
        * [<i></i>Create host item in Zabbix](#create-host-item-in-zabbix)
    * [<i></i>Licenses](#licenses)
    * [<i></i>Issues](#issues)
    * [<i></i>Development](#development)
    * [<i></i>Authors](#authors)



url_monitor
==========

This is a Zabbix plugin that creates items in Zabbix based off elements returned from an API.
Isomg JSON paths from an API the Zabbix items can be used for monitoring the status of a REST resource. It supports multiple requests auth backends including oauth, basicauth, or your own custom requests auth  plugins. This plugin also reports metrics as items using the Zabbix_sender method supporting custom item key formats.

Simple Installation
------------------

#### Requirements
Python 2.7 or greater (2.6.6 or greater with spec file)
python-daemon does not work with py 2.6.6 in pip.

#### Redhat install
`make rpms` (on a redhat platform) and then install the generated artifact on your target system. 

#### On other platforms 
`python setup.py install`

#### Setup

##### Configuration
Copy url_monitor.yaml to /etc/url_monitor.yaml and change to your requriements. Consult the
'Basic Configuration Options' below if you don't understand an option.

##### Scheduling
This Zabbix plugin is externally scheduled (due to the blocking nature of web requests)

**Cron Settings**

Create a file `/etc/cron.d/zabbix_url_monitor` with the following settings:

    # .---------------- minute (0 - 59)
    # |  .------------- hour (0 - 23)
    # |  |  .---------- day of month (1 - 31)
    # |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
    # |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
    # |  |  |  |  |
    # *  *  *  *  * user-name command to be executed
    */5 * * * * zabbix /usr/bin/url_monitor check --loglevel warning

##### Zabbix Template
You will need to import the Zabbix template in order to make the low-level discovery testSet items you have described in your configuration file.

##### Zabbix Triggers
Trigger creation through low level discovery is to be implemented (but is not currently.) These triggers will have to be manually created at this time.

<i class="icon-keyboard"></i> Basic Command Options
------------------
  usage: url_monitor [--help] [-h] [-V] [--key [KEY]] [--datatype [DATATYPE]] [-c CONFIG]
                COMMAND
  
  positional arguments:
    COMMAND

    optional commands:
      check
      discover
  
  optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit
    --key [KEY], -k [KEY]
                          Optional with `check` command. Can be used to run
                          checks on a limited subset of item headings under
                          testSet from the yaml config.
    --datatype [DATATYPE], -t [DATATYPE]
                          Required with `discover` command. This filters objects
                          from the config that have a particular datatype. This
                          data is used by low level discovery in Zabbix.
      -c [CONFIG], --config [CONFIG]
                            Specify custom config file, system default
                            /etc/url_monitor.yaml
      --loglevel [LOGLEVEL] Specify custom loglevel override. Available options
                            [debug, info, warn, critical, error, exceptions]

<i class="icon-keyboard"></i>  Simple Plugin Usage on the CLI
------------------
### Running a check
These two commands are used by the plugin  commands that the plugin uses for value transmission to Zabbix.

``$ url_monitor check`` Will run through all tests, collect the metrics and send a Zabbix item for each. Any checks with an error will return a failed check and exit of 1 for Zabbix.

``$ url_monitor check --key testSet_Name``
Will run a paticular test in the testSet. Useful for testing or custom setups.

To see what typical output could look like [see this section.](#configure-a-webcheck-in-url_monitor)

--- 

### Return low level discovery items
Low level discovery is used with the discover option.

``$ url_monitor discover --type strings``
This will look in the config for all testSet items that have the datatype strings set, and will expose the low level discovery format for Zabbix to create the items.

Running ``$ url_monitor discover`` will tell you which datatypes are available.

<i class="icon-file"></i> Basic Configuration Options
------------------

###  <i class="icon-book"></i>Pidfile

Every configuration should have a unique pidfile defined. This is especially
important if you use multiple configuration files with the --config option to
allow multiple concurrent executions.

NOTE: Pidfiles are saved under /var/lib/zabbixsrv/<filename> by default if a full
path is not supplied for saving the pid.

    config:
      pidfile: /var/lib/zabbixsrv/uuid78104271-39a1-4b33-a3bf-32658172238f.pid

---
###  <i class="icon-book"></i>Skip Checks When

In enterprise environments, you may have a Zabbix node in hot-standby. This would be a node with zabbix systems turned off and ready in a recovery situation. (It would connect to a replicated HA db backend) If you run this plugin locally on both zabbix servers, you may need a reason to bypass running checks.

You can check if plugin should skip execution based on puppet facts, shell script outputs, or the assignment of an environment variable.

The checks below can be defined independently or all at once. Conditions can be defined at once or single.

**Skip on Puppet Fact (using facter)**

NOTE: The `script` value is optional, facter under $PATH is default.

    config:
      skip_run_when:
        puppet_facter:
          script: /usr/local/bin/facter
          fact: zabbix_ha_state
          value: slave

This example skips execution if puppet-facter value for `zabbix_ha_state` returns 'slave'.

**Skip on Shell Script Result**

    config:
      skip_run_when:
        shell:
          script: /opt/ha_status.sh
          stdout: datacenter_standby
          code: 1

This will execute /opt/ha_status.sh and if the output is `datacenter_standby` or if the exit code is 1, the plugin will skip checks. 

NOTE: You can define `stdout` and `code` conditions together or independently. Execution skips if either condtions evaluate.
NOTE: The script feature cannot take arguements, this must be a path to a program or script with zero arguement values.

**Skip on Environment Variable**

    config:
      skip_run_when:
        environment:
          variable: ZABBIX_HA_STATE
          value: hot_spare

This example skips execution if parent shell environment variable `ZABBIX_HA_STATE` is `hot_spare`.

---
###  <i class="icon-book"></i>Network settings

These define some settings for the requests HTTP library used to power the checks.
The requests_timeout value must be a decimal/whole value in seconds.
The requests_verify_ssl value must be true/false or a path to a SSL cert chain.

    config:
      request_timeout: 30
      request_verify_ssl: true

---
###  <i class="icon-book"></i>Log level

Available loglevels are `debug`, `info`, `warn`, `critical`, `error`, `exceptions`.
The outputs field can take a comma seperated list or single item of file,syslog.
If you are using syslog, you will need to define the syslog server and socket as shown below. (The server field can have an alternate port specified in host:port syntax.)
If you are using file, you will need to define logfile outputs below.
Multiple outputs can be active at once.
The logformat can be changed as needed (confirming to python-logging conventions)

    config:
      logging:
        level: exceptions
        outputs: file,syslog
        logfile: /var/log/url_monitor.log
        syslog:
          server: 127.0.0.1
          socket: udp
        logformat: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

--- 
### <i class="icon-book"></i>Auth/Identity Providers
If your API or resource requires authentication you're going to want to configure an identity provider. Identity providers are defined in the main config. The first key name is the alias for the identity provider, then the second key defines the actual requests auth provider to use for your identity. The third set of keys defines the kwargs to pass to that identity provider.

This can be a built-in `requests.auth` provider as exemplified below or an external python module you've written or found to be an importable requests auth provider (as exemplified by requests_py_module/className. The module_kwargs_1 are arguements passed to the imported module. The KWARGS if not quoted strings can be python objects, like `bools`,`dict`,`list` etc. passed directly to your module.

PRO TIP: If you want to use the same identity provider, you can call it multiple times and only have to use a different aliase, such as the case of exampleCustomProvider. exampleCustomProvider could be duplicated as NEWexampleCustomProvider with the same keys beneath it.

    config:
      identity_providers:
        "exampleCustomProvider":
            "requests_py_module/className":
                module_kwarg_1: ""
                module_kwarg_2: ""
                module_kwarg_3: ""
        "winNT https://github.com/requests/requests-ntlm provider":
            "requests_ntlm/HttpNtlmAuth":
                username: "domain\\nt_admin"
                username: "password"
        "raxAuthProvider":
            "requests_openstack_identity/openIdentity":
                base_url: ""
                username: ""
                password: ""
        "basicProvider":
            "HTTPBasicAuth":
                username: "testuser"
                password: "staging"
        "digestProvider":
            "HTTPDigestAuth":
                username: "testuser"
                password: "staging"
        "openauthProvider":
            "oauthv1":
                oauthv1-application-key: "appkey"
                oauthv1-application-secret: "passw0rd"
                oauthv1-oauth_token: "token"
                oauthv1-token_secet: "secret"

---

### <i class="icon-book"></i>Example of of an API testSet configuration

    testSet:
      "my_cool_api":
        uri: https://my_private_api/health?json
        response_type: json
        identity_provider: basicProvider
        ok_http_code: 200
        transform_keys:
          - from: SUCCESS
            to: 1
          - from: ERROR
            to: 0
        testElements:
          - key: jdbc.pgsql
            jsonvalue: ./psqlstatus
            datatype: string
            metricname: PostgresStatus
            unit_of_measure: "events"
          - key: job.failureCount
            jsonvalue: ./jobFailure
            datatype: integer
            metricname: jobFailure
            unit_of_measure: "events"



.

`"my_cool_api":` is the profile name, not really important.

> **Config Key Reference:**
>
> **`uri`** is the resource with the JSON elements you wish to test.
> 
> **`identity_provider`** is a provider that you have defined in the above **identity provieers** section of this README. **NOTE** You can use `none` as a provider and no authentication will be made for requests.
> 
> **`ok_http_code`** is a single value, or a comma delimeted list of http code(s) that are acceptable for this check to work. The check will fail with exception output which can be caught by Zabbix as failing checks. **NOTE** You can use `any` value or in a list and valid codes from RFC 2616 will be included.
>
> **`response_type`** is always `json` until we add a different module for xml.
>
> **`request_verify_ssl`** can be either true/false or a path to a valid SSL cert trust file for validating certificates on checks. This will override the global setting (if present).
>
> **`transform_keys`** is a list of dictionaries containing a mapping for string transformations.  If the result from the api matches one of the mappings, the corresponding value will be sent to zabbix instead of the original value.  This is required if using the threshold functionality with string values returned by an api because of a limitation of LLD in zabbix (string based macros are not usable in trigger expressions).

##### Test Elements

Test elements are where the actual API response is parsed and check data is formulated.

- All items under **testElements** can also be referenced in the key name `item_key_format` configuration option to be used as item keys in Zabbix.
- All items under **testElements** will be sent as a low level discovery key/value to make the items available in item prototypes.

> **Config Key Reference:**
>
> **`key`** this is the key of your object
> 
> **`jsonvalue`** this is the path in json to your object
> 
>**`datatype`** this is one item, or a comma delimited list of item(s) to create item datatype(s) for. 
>
>**`metricname`** this is used in `item_key_format` to format the metric name.
>
>**`response_type`** is always json until XML support can be added.

--- 

### <i class="icon-book"></i>Zabbix host config
This controls where your Zabbix metrics are sent for collection.

> **Config Key Reference:**
>
> **`host`** is the name of the host in zabbix used to store metrics.
>
> **`server`** is your Zabbix host:port. If you leave out a : port designator the default 10051 will be assumed.

    config:
      zabbix:
        host: api.net
        server: localhost:10051
        item_key_format: "url_monitor[{datatype}, {metricname}, {uri}]" 
        checksummary_key_format: "url_monitor[EXECUTION_STATUS]"

##### item_key_format details

The `item_key_format` is the key format that should match your item prototype syntax in Zabbix UI.

Template substitution of variables are supported by the `{` and `}` characters, variables can be any key name you have defined within your `testElements` (see testSet configuration above) or can be one of the following built-ins.

> **Built-in Formatting Substitutes**
>
> **`{datatype}`** - Which is inherantly derived frm the datatype(s) defined in your testSet: testElements configuration. Probably a `string`, `counter` or `integer`
> 
> **`{uri}`** - The URI of test to be conducted which may be useful to pass to Zabbix also inherantly derived frm the uri defined in your testSet configuration
>
> **`{originhost}`** - The domain name of the API you are running a check on.
>
> **`{api_response}`** - The value of the HTTP response
>
> **`{request_statuscode}`** - The value of the HTTP status

##### checksummary_key_format details

At the end of all checks run in a configuration, a final Zabbix item is updated called EXECUTION status. The item key is defined as `checksummary_key_format`. You can monitor this key under your Zabbix host to determine if any checks have failed during the script execution.

<i class="icon-file"></i>Complete Example
------------------
###<i class="icon-book"></i>Configure a webcheck in URL_monitor
Assume you have a web service at localhost serving a status page like this JSON blob below

  $ curl http://localhost:8888/status
  {"elements": [0, 1, 2], "api_status": {"mongo": "failed", "schedulerErrorCounts": 1461869481}}

You could write the following test expressions in your configuration to create Zabbix items out of pieces of information in your API response.


    item_key_format: "url_monitor[{datatype}, {metricname}, {uri}]"

testSet:
  "exampleAPI":
    uri: http://localhost:8888/status
      response_type: json
      identity_provider: none
      ok_http_code: 200,204
      request_verify_ssl: true
      testElements:
        - key: keyname
          jsonvalue: ./api_status/mongo
          datatype: string
          metricname: "api_status_for_mongo"
          unit_of_measure: "boolean"
        - key: keyname2
          jsonvalue: ./api_status/schedulerErrorCounts
          datatype: integer
          metricname: "schedulerErrorCounts"
          unit_of_measure: "boolean"
        - key: keyname3
          jsonvalue: ./elements[1]
          datatype: integer
          metricname: "thing"
          unit_of_measure: "boolean"


Then when you run the check you will see the following output (in debug mode)
  
  $ python url_monitor/main.py check -k exampleAPI --loglevel debug
  INFO:requests.packages.urllib3.connectionpool:Starting new HTTP connection (1): localhost
  DEBUG:requests.packages.urllib3.connectionpool:"GET /status HTTP/1.1" 200 94
  DEBUG:root:Zabbix host localhost port 10051
  DEBUG:zbxsender:Sent payload: ZBXD�{
    "request":"sender data",
    "data":[
      {
        "host":"url_monitor",
        "key":"url_monitor[string, api_status_for_mongo, http://localhost:8888/status]",
        "value":"failed",
        "clock":1461869579.57},
      {
        "host":"url_monitor",
        "key":"url_monitor[integer, schedulerErrorCounts, http://localhost:8888/status]",
        "value":1461869579,
        "clock":1461869579.57},
      {
        "host":"url_monitor",
        "key":"url_monitor[integer, thing, http://localhost:8888/status]",
        "value":0,
        "clock":1461869579.57}]
  }
  DEBUG:zbxsender:Got response from Zabbix: {u'info': u'processed: 3; failed: 0; total: 3; seconds spent: 0.000064', u'response': u'success'}
  INFO:zbxsender:processed: 3; failed: 0; total: 3; seconds spent: 0.000064


--- 

### <i class="icon-book"></i>Configure Zabbix UI

#### <i class="icon-book"></i>Create Zabbix url_monitor template
Click `Configuration -> Templates` 

Click  `Create new template`


> **New Template Reference:**
>
> **`template_name`** can be `url_monitor`

Click `save`

---


#### <i class="icon-book"></i>Configure low-level discovery in Zabbix UI
Find the template you just created.

Click on `Discovery Rules`

Click on `Create discovery rule`


> **New Discovery Rule Reference:**
>
> **`name`** in this example `string` but you will want a discovery rule for each data-type you want Zabbix to support.
> 
> **`type`** External check goes here. This is an external plugin.
> 
> **`key`** This is your external command.
> 
>   Put `url_monitor[discover, -t, string]` here
>   This configures a discovery rule for generating item prototypes.
> 
> **`update interval`**(sec) Your choice.
> 
> **`Keep lost resources period (in days)`** we set to 1.
> 

Click `save`

--- 

#### <i class="icon-book"></i>Configure Item Prototypes in Zabbix UI
Click on `Item prototypes` for the string discovery you just created.

Click `create item prototype`

> **New Item Prototype Reference:**
>
> **`name`** this is the name it will have in the items page, handy descriptive item.
> 
> You can use `integer-{#CHECKNAME}`
> 
> **`type`** Zabbix Trapper
> 
> **`key`** This is the string format that your item keys will have to come in as, we use common fields from the url_monitor.yaml for elements. 
> 
> You can use `url_monitor[string, {#METRICNAME}, {#RESOURCE_URI}]`
>
> **`enabled`** should be true

Click `save`

--- 

#### <i class="icon-book"></i>Configure basic triggers in Zabbix UI


Click on `Item triggers` for the string discovery you just created.

Click `create trigger prototype`

> **New Trigger Reference:**
>
> **`name`** You can use
> 
>      string trigger for url_monitor[string, {#METRICNAME}, {#RESOURCE_URI}]
>       
> **`expression`** Can be
> 
>     {url_monitor:url_monitor[string, {#METRICNAME}, {#RESOURCE_URI}].str(success)}#0

Click `save`

--- 

#### <i class="icon-book"></i>Create host item in Zabbix

Go to `Configuration` -> `Hosts` 

Click `Create host`

> **New Host Reference:**
>
> **`host name`** Create a host called `url_monitor`
> 

Click `Templates`
> **New Host Reference:**
> 
>    Link new templates  `url_monitor`
> 
>    This will link to the template and should generate your triggers and item prototypes automatically.

Click `save`

--- 

<i class="icon-umbrella"></i>Licenses
------------------
Copyright 2016 Rackspace US, Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

--- 

Other licensing applies:

| Project              | License                              |
| :------------------- | -----------------------------------: |
| Python               | Python Software Foundation License   |
| argparse             | Python Software Foundation License   | 
| textwrap             | Python Software Foundation License   | 
| logging              | by Vinay Sajip. All Rights Reserved  |
| requests             | Apache 2 License                     |
| PyYaml               | MIT                                  |
| zbxsend              | BSD                                  |
| **url_monitor**      | Apache 2 License                     |

<i class="icon-bug"></i>Issues
------------------
Please report any bugs or requests that you have using the GitHub issue tracker!

<i class="icon-keyboard"></i>Development
------------------
Install these following tools for a development environment.

Redhat:

        yum groupinstall "development tools"`
        yum install python-devel`

<i class="icon-heart"></i>Authors
------------------
* Jonathan Kelley
* Nick Bales
