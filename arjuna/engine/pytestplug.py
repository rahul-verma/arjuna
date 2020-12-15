import sys
import os
import pytest
import threading
import platform

from arjuna.engine.pytest import PytestHooks

from functools import partial

from arjuna.interface.cli.validation import *
from arjuna.interface.enums import TargetEnum


_ARJUNA_CLI_ARGS = {
    "target": ("--target", {
        "dest":"target", 
        "metavar":"target", 
        "choices":[i for i in TargetEnum.__members__],
        "type":ustr, 
        "help":'Choose what to run. Running all tests in project is the default.', 
        # "default":"mrun"
    }),

    "run.id": ("--run-id", {
        "dest":"run.id", 
        "metavar":"run_id", 
        # "type":partial(lname_check, "Run ID"), 
        "help": 'Alnum 3-30 length. Only lower case letters.', 
        # "default":"mrun"
    }),

    "report.formats": ('--report-formats', {
        "dest":"report.formats", 
        # "type":report_format, 
        "action":"append", 
        "choices":[i for i in ReportFormat.__members__], 
        "help":'Output/Report format. Can pass any number of these switches.'
     }), # "choices":['XML', 'HTML'], 

    "link.projects": ('--link-projects', {
        "dest":"link.projects", 
        "action":"append", 
        "help":'Linked Arjuna Test Project.',
    }),

    "static.rid": ('--update', {
        "dest":"static.rid", 
        "action":'store_true', 
        "help": 'Will result in overwriting of report files. Useful during script development.'
    }),

    "dry.run": ('--dry-run', {
        "dest":"dry.run", 
        "choices":[i for i in DryRunType.__members__], 
        # "type":dry_run_type, 
        "help":'Does a dry run. Tests are not executed. Behavior depends on the type passed as argument. SHOW_TESTS - enumerate tests. SHOW_PLAN - enumerates tests and fixtures. RUN_FIXTURES - Executes setup/teardown fixtures and emuerates tests.'
    }),

    "ref.conf": ('--ref-conf', {
        "dest":"ref.conf", 
        "metavar":"config_name", 
        # "type":str, 
        "help":"Reference Configuration object name for this run. Default is 'ref'"
    }),

    "ao": ('--arjuna-option', {
        "dest":"ao",
        "nargs":2,
        "action":'append',
        "metavar":('option', 'value'),
        "help":'Arjuna Option. Can pass any number of these switches.'
    }),

    "uo": ("--user-option", {
        "dest":"uo",
        "nargs":2,
        "action":'append',
        "metavar":('option', 'value'),
        "help":'User Option. Can pass any number of these switches.'
    }),

    'log.console.level': ('--display-log-level', {
        "dest":'log.console.level', 
        # "type":ustr, 
        "choices":[i for i in LoggingLevel.__members__],
        "help":"Minimum message level for display. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')", 
        # "default":LoggingLevel.INFO.name
    }),

    'log.file.level': ('--file-log-level', {
        "dest":'log.file.level', 
        # "type":ustr, 
        "choices":[i for i in LoggingLevel.__members__],
        "help":"Minimum message level for log file. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')", 
        # "default":LoggingLevel.DEBUG.name
    }),
}

def pytest_addoption(parser):
    group = parser.getgroup("arjuna", "Arjuna Test Automation Framework")
    for k,v in _ARJUNA_CLI_ARGS.items():
        group.addoption(v[0], **v[1])

_commands = {
    "PROJECT" : "run-project",
    "GROUP" : "run-group",
    "SELECTED" : "run-selected",
}

def pytest_cmdline_parse(pluginmanager, args):
    project_path = None
    for index, arg in enumerate(args):
        if arg.lower().startswith("--rootdir"):
            argparts = [p.strip() for p in arg.split("=")]
            if len(argparts) == 2:
                project_path = argparts[1]
            else:
                project_path = args[index + 1]
                if project_path.startswith("-"):
                    raise Exception("For rootdir switch you must provide a path.")
            break
    if project_path is None:
        project_path = os.getcwd()
    sys.path.append(project_path + "/..")
    sys.path.append(project_path + "/..")
    args.extend(['--rootdir', project_path])

    res_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../res"))
    pytest_ini_path = res_path + "/pytest.ini"
    css_path = res_path + "/arjuna.css"
    args.extend(["-c", pytest_ini_path, "--disable-warnings", "-rxX", "--css", css_path])

    if platform.system().casefold() == "Windows".casefold() :
        args.extend(["--capture", "no"])
    else:
        args.extend(["--no-print-logs", "--show-capture", "all"])

def pytest_configure(config):
    args = ["pytestplugin"]
    value = config.getoption("target")
    if not value: value = "project"
    args.append(_commands[value.upper()])
    args.append('-p')
    args.append(config.option.rootdir)
    for option in _ARJUNA_CLI_ARGS:
        if option == "target":
            continue
        value = config.getoption(option)
        if value:
            if _ARJUNA_CLI_ARGS[option][1].get('action', None) == 'append':
                for entry in value:
                    print(entry)
                    args.append(_ARJUNA_CLI_ARGS[option][0])
                    if type(entry) is list:
                        args.extend(str(i) for i in entry)
                    else:
                        args.apppend(str(entry))
            elif _ARJUNA_CLI_ARGS[option][1].get('action', None) in {'store_true', 'store_false'}:
                args.append(_ARJUNA_CLI_ARGS[option][0])
            else:
                args.append(_ARJUNA_CLI_ARGS[option][0])
                if type(value) is list:
                    args.extend([str(i)] for i in value)
                else:
                    args.append(str(value))
    # print(args)
    # print(" ".join(args))

    from arjuna.main import main
    main(*args, ext_engine=True)
    import os
    from arjuna import C
    os.chdir(C("project.root.dir"))
    # PytestHooks.add_env_data(config)

    # Ported from current Test Group concept.
    from arjuna import Arjuna
    from arjuna.tpi.constant import ArjunaOption
    Arjuna.register_group_params(name="mgroup", config=Arjuna.get_config(), thread_name=threading.currentThread().name)

    xml_path = os.path.join(Arjuna.get_config().value(ArjunaOption.REPORT_XML_DIR), "report.xml")
    html_path = os.path.join(Arjuna.get_config().value(ArjunaOption.REPORT_HTML_DIR), "report.html")
    report_formats = Arjuna.get_config().value(ArjunaOption.REPORT_FORMATS)

    from arjuna.engine.selection.selector import Selector
    selector = Selector()
    # if rules:
    #     for rule in rules['ir']:
    #         selector.include(rule)
    #     for rule in rules['er']:
    #         selector.exclude(rule)

    Arjuna.register_test_selector_for_group(selector)



def pytest_collection_modifyitems(items, config):
    from arjuna import Arjuna
    session = Arjuna.get_test_session()
    session.load_tests(dry_run=config.getoption("dry.run"), ref_conf_name=config.getoption("ref.conf"))
    PytestHooks.select_tests(items, config)

def pytest_generate_tests(metafunc):
    PytestHooks.configure_group_for_test(metafunc)

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    result = yield
    PytestHooks.prepare_result(result)
    PytestHooks.enhance_reports(item, result)


def pytest_html_report_title(report):
    PytestHooks.set_report_title(report)

def pytest_html_results_summary(prefix, summary, postfix):
    PytestHooks.inject_arjuna_js(prefix)