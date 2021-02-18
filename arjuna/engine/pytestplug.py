import sys
import os
import pytest
import threading
import platform
import pkg_resources

from arjuna.engine.pytest import PytestHooks

from functools import partial

from arjuna.interface.cli.validation import *
from arjuna.interface.enums import TargetEnum
from arjuna.core.error import *
from arjuna.tpi.error import *
from arjuna.tpi.parser.yaml import Yaml


_ARJUNA_CLI_ARGS = {
    "project": ("--project", {
        "dest":"project", 
        "metavar":"project_root_dir", 
        "type": project_dir,
        "help":'Valid absolute path of an existing Arjuna test project. If not provided pytest rootdir value is considered. If that is not provided, current working directory is considered.'
    }),

    "run.id": ("--rid", {
        "dest":"run.id", 
        "metavar":"run_id", 
        # "type":partial(lname_check, "Run ID"), 
        "help": 'Alnum 3-30 length. Only lower case letters.', 
        # "default":"mrun"
    }),

    "report.formats": ('--otype', {
        "dest":"report.formats", 
        "type":report_format, 
        "action":"append", 
        "choices":[i for i in ReportFormat.__members__], 
        "help":'Output/Report format. Can pass any number of these switches.',
        # "default": ['XML', 'HTML']
     }), # "choices":['XML', 'HTML'], 

    "link.projects": ('--link', {
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

    "ref.conf": ('--rconf', {
        "dest":"ref.conf", 
        "metavar":"config_name", 
        # "type":str, 
        "help":"Run/Reference Configuration object name for this run. Default is 'ref'",
    }),

    "ao": ('--ao', {
        "dest":"ao",
        "nargs":2,
        "action":'append',
        "metavar":('option', 'value'),
        "help":'Arjuna Option. Can pass any number of these switches.'
    }),

    "uo": ("--uo", {
        "dest":"uo",
        "nargs":2,
        "action":'append',
        "metavar":('option', 'value'),
        "help":'User Option. Can pass any number of these switches.'
    }),

    'log.console.level': ('--display-level', {
        "dest":'log.console.level', 
        "type":ustr, 
        "choices":[i for i in LoggingLevel.__members__],
        "help":"Minimum message level for display. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')", 
        # "default":LoggingLevel.INFO.name
    }),

    'log.file.level': ('--logger-level', {
        "dest":'log.file.level', 
        "type":ustr, 
        "choices":[i for i in LoggingLevel.__members__],
        "help":"Minimum message level for log file. (choose from 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL')", 
        # "default":LoggingLevel.DEBUG.name
    }),

    "group": ("--group", {
        "dest": "group", 
        "metavar": "group_name", 
        "type": partial(lname_check, "Group Name"), 
        "help": 'Name of a defined group in test groups configuration file in <Project Root>/config/groups.yaml file.',
        "default": "mgroup"
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

def convert_to_absolute(p):
    if p.startswith("./test") or p.startswith(".\\test"):
        return os.path.join(pytest_root_dir + p[1:])
    else:
        return p

def pytest_addoption(parser):
    from arjuna.tpi.parser.text import _TextResource
    reader = _TextResource("header.txt")
    print(reader.read().format(version=pkg_resources.require("arjuna")[0].version))
    reader.close()

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

def _determine_project_root_dir(args):
    def process_rootdir_or_project(index, arg, oargs):
        argparts = [p.strip() for p in arg.split("=")]
        if len(argparts) == 2:
            project_path = argparts[1]
            oargs[index] = "__REMOVE__"
        else:
            project_path = args[index + 1]
            if project_path.startswith("-"):
                raise Exception("For rootdir switch you must provide a path.")

            oargs[index] = "__REMOVE__"
            oargs[index + 1] = "__REMOVE__"
        return project_path

    project_path = None
    root_dir = None

    from copy import deepcopy
    targs = deepcopy(args)

    for index, arg in enumerate(targs):
        if arg.lower().startswith("--rootdir"):
            root_dir = process_rootdir_or_project(index, arg, args)
        elif arg.lower().startswith("--project"):
            project_path = process_rootdir_or_project(index, arg, args)

    if project_path is None:
        pytest_root_dir = os.getcwd()
    elif project_path is not None:
        if project_path == ".":
            pytest_root_dir = os.getcwd()
        else:
            pytest_root_dir = project_path
    elif root_dir is not None:
        pytest_root_dir = root_dir

    if not os.path.isabs(pytest_root_dir):
        pytest_root_dir = os.path.join(os.getcwd(), pytest_root_dir)

    CONVERTED_ARGS.extend(['--project', pytest_root_dir])

    args[:] = [e for e in args if e != "__REMOVE__"]

    args[:] = [convert_to_absolute(e) for e in args]
    sys.path.append(pytest_root_dir + "/..")
    args.extend(['--rootdir=' + pytest_root_dir])
    args.extend(['-c', pytest_root_dir + "/pytest.ini"])

    conf_file = os.path.join(pytest_root_dir, "test/conftest.py")
    if os.path.exists(conf_file):
        os.remove(conf_file)


    return pytest_root_dir

def _add_pytest_addl_args(args):
    res_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../res"))
    # pytest_ini_path = res_path + "/pytest.ini"
    css_path = res_path + "/arjuna.css"
    more_args = ["--disable-warnings", "-rxX", "--css", css_path, "--log-level", "FATAL"] #"-c", pytest_ini_path, 
    args.extend(more_args)
    CONVERTED_ARGS.extend(more_args)

    platform_args = None
    if platform.system().casefold() == "Windows".casefold() :
        platform_args = ["--capture", "no"]
    else:
        platform_args = ["--show-capture", "all"] #, "--no-print-logs"]
    args.extend(platform_args)
    CONVERTED_ARGS.extend(platform_args)    

def _handle_dry_run_option(args):
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


# def pytest_cmdline_parse(pluginmanager, args):
@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(early_config, parser, args):
    # print(early_config.known_args_namespace)
    # sys.exit()
    if '--help' in args or '-h' in args:
        return
    RAW_ARGS.extend([arg.find(" ") == -1 and arg or f'"{arg}"' for arg in args])
    pytest_root_dir = _determine_project_root_dir(args)

    res_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../res"))
    # pytest_ini_path = res_path + "/pytest.ini"
    css_path = res_path + "/arjuna.css"
    import pathlib
    # early_config.inifile = pathlib.Path(pytest_ini_path)

    _add_pytest_addl_args(args)
    _handle_dry_run_option(args)
    global pytestargs
    pytestargs = args

_ONLY_CMD = {"project", "run.id", "static.rid", "link.projects", "dry.run", "ref.conf", "group"}

def _load_argdict_rule_dict(config):
    rule_dict = dict()
    arg_dict = {}
    for option in _ARJUNA_CLI_ARGS:
        value = config.getoption(option)
        if option.lower() in _ONLY_CMD:
            continue
        if option.lower() in {'ipack', 'epack', 'imod', 'emod', 'itest', 'etest', 'irule', 'erule'}:
            rule_dict[option.lower()] = value
            if value:
                for v in value:
                    if option.lower() in {"irule", "erule"}:
                        CONVERTED_ARGS.extend(["--" + option, f'"{v}"'])    
                    else:
                        CONVERTED_ARGS.extend(["--" + option, v])
            continue
        if value:
            arg_dict[option] = value
    return arg_dict, rule_dict

def _init_arjuna(config, arg_dict):
    from arjuna import Arjuna
    from arjuna.configure.cli import CliArgsConfig
    cliconfig = CliArgsConfig(arg_dict)

    linked_projects = config.getoption("link.projects")
    if linked_projects is not None:
        out = []
        for lp in linked_projects:
            if not os.path.isabs(lp):
                out.append(os.path.join(os.getcwd(), lp))
            else:
                out.append(lp)
        linked_projects = out
    Arjuna.init(
        config.option.rootdir, 
        run_id=config.getoption("run.id"), 
        static_rid=config.getoption("static.rid"), 
        linked_projects=linked_projects, 
        arjuna_options=cliconfig.arjuna_options, 
        user_options=cliconfig.user_options
    )

    from arjuna import C
    os.chdir(C("project.root.dir"))

class TestGroup:

    def __init__(self, *, name="mgroup", rconf_name="ref"):
        from arjuna import Arjuna
        from arjuna.tpi.constant import ArjunaOption
        Arjuna.register_group_params(name=name, config=Arjuna.get_config(rconf_name), thread_name=threading.currentThread().name)    

    def __create_rule_strs(self, include_exclude_dict):
        pickers_rulestr = {
            'ipack': "package *= {}",
            'epack': "package *= {}",
            'imod': "module *= {}",
            'emod': "module *= {}",
            'itest': "name *= {}",
            'etest': "name *= {}",
        }

        rules = {'ir': [], 'er': []}

        for picker in pickers_rulestr:
            names = include_exclude_dict.pop(picker)
            if names:
                for name in names:
                    if picker.startswith('i'):
                        rules['ir'].append(pickers_rulestr[picker].format(name))
                    else:
                        rules['er'].append(pickers_rulestr[picker].format(name))

        for k,v in include_exclude_dict.items():
            if not v: continue
            if k == "irule":
                rules['ir'].extend(v)
            elif k == "erule":
                rules['er'].extend(v)

        return rules

    def _load_tests(self, rule_dict):
        i_e_rules = self.__create_rule_strs(rule_dict)
        rules = {'ir': [], 'er': []}
        rules['ir'].extend(i_e_rules['ir'])
        rules['er'].extend(i_e_rules['er'])

        from arjuna.engine.selection.selector import Selector
        selector = Selector()
        if rules:
            for rule in rules['ir']:
                selector.include(rule)
            for rule in rules['er']:
                selector.exclude(rule)

        from arjuna import Arjuna
        Arjuna.register_test_selector_for_group(selector)

    @classmethod
    def from_pickers(cls, *, rconf_name=None, rules={}):
        if rconf_name is None: rconf_name = "ref"
        group = TestGroup(rconf_name=rconf_name)
        group._load_tests(rules)
        return group

    @classmethod
    def __get_group_yaml(cls, name):
        from arjuna import C
        gfile = C(ArjunaOption.CONF_GROUPS_LOCAL_FILE)
        if not os.path.isfile(gfile):
            gfile = C(ArjunaOption.CONF_GROUPS_FILE)                
        try:
            gyaml = Yaml.from_file(gfile, allow_any=True)
        except FileNotFoundError:
            raise TestGroupsFileNotFoundError(file_path=gfile)
           
        try:
            return gyaml.get_section(name)
        except YamlUndefinedSectionError as e:
            raise UndefinedTestGroupError(name=name, file_path=gfile)

    @classmethod
    def from_def(cls, name, *, rconf_name=None, rules={}):
        group_yaml = cls.__get_group_yaml(name)
        from arjuna import Arjuna
        for gmd_name in group_yaml.section_names:
            rules = {
                'ipack': None,
                'epack': None,
                'imod': None,
                'emod': None,
                'itest': None,
                'etest': None,
                'irule' : None,
                'erule': None
            }
            gmd_name = gmd_name.lower()
            if gmd_name == "conf":
                rconf_name = group_yaml["conf"]
            elif gmd_name in rules:
                rules[gmd_name] = group_yaml[gmd_name]

        if rconf_name is None:
            rconf_name = "ref"
        group = TestGroup(name=name, rconf_name=rconf_name)
        group._load_tests(rules)
        return group

def _configure_pytest_reports(config):
    from arjuna import Arjuna
    xml_path = os.path.join(Arjuna.get_config().value(ArjunaOption.REPORT_XML_DIR), "report.xml")
    html_path = os.path.join(Arjuna.get_config().value(ArjunaOption.REPORT_HTML_DIR), "report.html")
    report_formats = Arjuna.get_config().value(ArjunaOption.REPORT_FORMATS)

    if ReportFormat.XML in report_formats:
        if not config.option.xmlpath:
            config.option.xmlpath = xml_path
            CONVERTED_ARGS.extend(["--junit-xml", xml_path])

    if ReportFormat.HTML in report_formats:
        config.option.htmlpath = html_path
        config.option.self_contained_html = True
        CONVERTED_ARGS.extend(["--html", html_path])
        CONVERTED_ARGS.extend(["--self-contained-html"])

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if config.getoption("help"):
        return

    arg_dict, rule_dict = _load_argdict_rule_dict(config)
    _init_arjuna(config, arg_dict)
    gname = config.getoption("group").lower()
    if gname == "mgroup":
        group = TestGroup.from_pickers(rconf_name=config.getoption("ref.conf"), rules=rule_dict)
    else:
        if rule_dict:
            raise Exception("When you provide a group name, you can provide test selectors/rules in Command line. You have provided group name as >>{}<< and also provided selectors/rules: {}".format(gname, {k:v for k,v in rule_dict.items() if v}))
        group = TestGroup.from_def(gname, rconf_name=config.getoption("ref.conf"))

    _configure_pytest_reports(config)

    from arjuna import Arjuna
    Arjuna._set_command(" ".join(RAW_ARGS))
    Arjuna.register_pytest_command_for_group(" ".join(CONVERTED_ARGS))

    PytestHooks.add_env_data(config)

def pytest_collection_modifyitems(items, config):
    # from arjuna import Arjuna
    # session = Arjuna.get_test_session()
    # session.load_tests(dry_run=config.getoption("dry.run"), ref_conf_name=config.getoption("ref.conf"))
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