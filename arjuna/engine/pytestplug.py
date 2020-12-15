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

    "report.formats": ('--report-format', {
        "dest":"report.formats", 
        # "type":report_format, 
        "action":"append", 
        "choices":[i for i in ReportFormat.__members__], 
        "help":'Output/Report format. Can pass any number of these switches.',
        "default": ['XML', 'HTML']
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
        "type":ustr, 
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

    'ipack': ('--ipack', {
        "dest":"ipack", 
        "action":"append", 
        "metavar":"package_name_or_regex", 
        "default":None, 
        "help":'Name/regex pattern for including test packages. Can pass any number of these switches.'
    }),

    'epack': ('--epack', {
        "dest":"epack", 
        "action":"append", 
        "metavar":"package_name_or_regex", 
        "default":None, 
        "help":'Name/regex pattern for excluding test packages. Can pass any number of these switches.'
    }),

    'imod': ('--imod', {
        "dest":"imod", 
        "action":"append", 
        "metavar":"module_name_or_regex", 
        "default":None, 
        "help":'Name/regex pattern for including test modules. Can pass any number of these switches.'
    }),

    'emod': ('--emod', {
        "dest":"emod", 
        "action":"append", 
        "metavar":"module_name_or_regex", 
        "default":None, 
        "help":'Name/regex pattern for excluding test modules. Can pass any number of these switches.'
    }),

    'itest': ('--itest', {
        "dest":"itest", 
        "action":"append", 
        "metavar":"test_name_or_regex", 
        "default":None, 
        "help":'Name/regex pattern for including test functions. Can pass any number of these switches.'
    }),

    'etest': ('--etest', {
        "dest":"etest", 
        "action":"append", 
        "metavar":"test_name_or_regex", 
        "default":None, 
        "help":'Name/regex pattern for excluding test functions. Can pass any number of these switches.'
    }),

    'irule': ('--irule', {
        "dest":"irule", 
        "action":"append", 
        "metavar":"rule", 
        "default":None, 
        "help":'Include test functions that match the rule. Can pass any number of these switches. Test Function is included if any of the inclusion rules matches.'
    }),

    'erule': ('--erule', {
        "dest":"erule", 
        "action":"append", 
        "metavar":"rule", 
        "default":None, 
        "help":'Exclude test functions that match the rule. Can pass any number of these switches. Test Function is excluded if any of the exclusion rules matches. Evaluated before any inclusion rules.'
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


RAW_ARGS = ["pytest"]
CONVERTED_ARGS = ["pytest", "-p", "arjuna"]

def pytest_cmdline_parse(pluginmanager, args):
    if '--help' in args or '-h' in args:
        return
    RAW_ARGS.extend(args)
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
        CONVERTED_ARGS.extend(['--rootdir', project_path])
    sys.path.append(project_path + "/..")
    args.extend(['--rootdir', project_path])

    res_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../res"))
    pytest_ini_path = res_path + "/pytest.ini"
    css_path = res_path + "/arjuna.css"
    more_args = ["-c", pytest_ini_path, "--disable-warnings", "-rxX", "--css", css_path]
    args.extend(more_args)
    CONVERTED_ARGS.extend(more_args)

    platform_args = None
    if platform.system().casefold() == "Windows".casefold() :
        platform_args = ["--capture", "no"]
    else:
        platform_args = ["--no-print-logs", "--show-capture", "all"]
    args.extend(platform_args)
    CONVERTED_ARGS.extend(platform_args)    

    dry_run_raw = None
    for index, arg in enumerate(args):
        if arg.lower().startswith("--dry-run"):
            argparts = [p.strip() for p in arg.split("=")]
            if len(argparts) == 2:
                dry_run_raw = argparts[1]
            else:
                dry_run_raw = args[index + 1]
                if dry_run_raw.startswith("-"):
                    raise Exception("For --dry-run switch you must provide a dry run type.")
            break

    if dry_run_raw is not None:
        from arjuna.core.constant import DryRunType
        try:
            dry_run = DryRunType[dry_run_raw.upper()]
        except Exception as e:
            print(e)
            raise Exception("Invalid dry run type. Should be one of show_tests/show_plan/create_res")

        print("!!!!!! This is a DRY RUN !!!!!!!")
        if dry_run == DryRunType.SHOW_TESTS:
            print("Dry Run Type: SHOW TESTS")
            print("You can see the test functions which will be executed as per settings of your command.")
            darg = "--collect-only"
        elif dry_run == DryRunType.SHOW_PLAN:
            print("Dry Run Type: SHOW PLAN")
            print("You can see the test functions as well as the fixtures which will be executed as per settings of your command.")
            darg = "--setup-plan"
        elif dry_run == DryRunType.CREATE_RES:
            print("Dry Run Type: CREATE RESOURCES")
            print("All resources will be created as per your current command. You can see the test functions which will be executed as per settings of your command.")
            darg = "--setup-only"

        args.extend([darg])
        CONVERTED_ARGS.extend([darg]) 

    # args.extend(['--report-format', 'HTML', '--report-format', 'XML'])

    global pytestargs
    pytestargs = args

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if config.getoption("help"):
        return

    args = ["arjuna"]
    value = config.getoption("target")
    if not value: 
        value = "project"
        CONVERTED_ARGS.extend(["--target", value])
    args.append(_commands[value.upper()])
    args.append('-p')
    args.append(config.option.rootdir)
    rule_dict = dict()
    for option in _ARJUNA_CLI_ARGS:
        value = config.getoption(option)
        if option == "target":
            CONVERTED_ARGS.extend(["--" + option, value.lower()])
            continue
        if option.lower() in {'ipack', 'epack', 'imod', 'emod', 'itest', 'etest', 'irule', 'erule'}:
            rule_dict[option.lower()] = value
            if value:
                for v in value:
                    CONVERTED_ARGS.extend(["--" + option, v])
            continue
        if value:
            if _ARJUNA_CLI_ARGS[option][1].get('action', None) == 'append':
                for entry in value:
                    print(entry)
                    args.append(_ARJUNA_CLI_ARGS[option][0])
                    if type(entry) is list:
                        args.extend(str(i) for i in entry)
                    else:
                        args.append(str(entry))
            elif _ARJUNA_CLI_ARGS[option][1].get('action', None) in {'store_true', 'store_false'}:
                args.append(_ARJUNA_CLI_ARGS[option][0])
            else:
                args.append(_ARJUNA_CLI_ARGS[option][0])
                if type(value) is list:
                    args.extend([str(i)] for i in value)
                else:
                    args.append(str(value))
    print(args)
    print(" ".join(args))

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

    # From current CLI (run-selected logic)
    from arjuna.engine.session.group import TestGroup
    print(rule_dict)
    i_e_rules = TestGroup.create_rule_strs(rule_dict)
    print(i_e_rules)
    rules = {'ir': [], 'er': []}
    rules['ir'].extend(i_e_rules['ir'])
    rules['er'].extend(i_e_rules['er'])
    irule_strs = config.getoption('irule')
    if irule_strs:
        rules['ir'].extend(irule_strs)
    erule_strs = config.getoption('erule')
    if erule_strs:
        rules['er'].extend(erule_strs)

    from arjuna.engine.selection.selector import Selector
    selector = Selector()
    if rules:
        for rule in rules['ir']:
            selector.include(rule)
        for rule in rules['er']:
            selector.exclude(rule)

    Arjuna.register_test_selector_for_group(selector)

    xml_path = os.path.join(Arjuna.get_config().value(ArjunaOption.REPORT_XML_DIR), "report.xml")
    html_path = os.path.join(Arjuna.get_config().value(ArjunaOption.REPORT_HTML_DIR), "report.html")
    report_formats = Arjuna.get_config().value(ArjunaOption.REPORT_FORMATS)

    if ReportFormat.XML in report_formats:
        config.option.junit_xml = xml_path

    if ReportFormat.HTML in report_formats:
        config.option.htmlpath = html_path
        config.option.self_contained_html = True

    Arjuna._set_command(" ".join(RAW_ARGS))
    Arjuna.register_pytest_command_for_group(" ".join(CONVERTED_ARGS))

    PytestHooks.add_env_data(config)

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