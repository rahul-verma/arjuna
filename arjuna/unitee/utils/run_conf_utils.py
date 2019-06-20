from arjuna.lib.utils import sys_utils
from arjuna.lib.utils import etree_utils
from arjuna.unitee.types.containers import *
from arjuna.unitee.test.defs.fixture import *

ALLOWED_CONFIG_ATTRS = {'name', 'value'}
MANDATORY_CONFIG_ATTRS = {'name', 'value'}
ALLOWED_FIXTURE_ATTRS = {'type', 'module', 'func'}

ALLOWED_STAGE_ATTRS = {'name', 'threads'}

ALLOWED_GROUP_ATTRS = {'name', 'threads'}
MANDATORY_GROUP_ATTRS = {'name'}

ALLOWED_GCONF_ATTRS = {'name'}
MANDATORY_GCONF_ATTRS = ALLOWED_GCONF_ATTRS

ALLOWED_PATTERN_ATTRS = {'type', 'pattern'}
MANDATORY_PATTERN_ATTRS = ALLOWED_PATTERN_ATTRS

ALLOWED_RULE_ATTRS = {'if', 'in'}
MANDATORY_RULE_ATTRS = {'if'}

VALID_FIXTURES = {
    "session" : {"init_session", "end_session", "init_each_stage", "end_each_stage"},
    "stage" : {"init_stage", "end_stage", "init_each_group", "end_each_group"},
    "group" : {"init_group", "end_group", "init_each_module", "end_each_module"}
}

converter_map = {
    'int': int,
    'str': str,
    'float': float,
    'bool': bool
}

def display_err_and_exit(conf_type, conf_path, msg):
    from arjuna import ArjunaCore
    console = ArjunaCore.console
    console.display_error(msg + " Fix {} template file: {}".format(conf_type, conf_path))
    sys_utils.fexit()


def validate_config_xml_child(conf_type, session_path, config_node):
    if config_node.tag.lower() not in {'arjuna_option', 'user_option'}:
        display_err_and_exit(conf_type, session_path, ">>config<< element can only contain one or more children of type >>arjuna_option<< or >>user_option<<.")
    for k,v in config_node.attrib.items():
        if k.lower() not in ALLOWED_CONFIG_ATTRS:
            display_err_and_exit(conf_type, session_path, ">>{}<< element attributes can only be set as: {}.".format(config_node.tag, ALLOWED_CONFIG_ATTRS))
    if not MANDATORY_CONFIG_ATTRS.issubset(etree_utils.convert_attribs_to_cidict(config_node)):
        display_err_and_exit(conf_type, session_path, ">>{}<< element must define >>name<< and >>value<< attributes.")


def add_config_node_to_configuration(conf_type, config_container, config_node):
    config_attrs = CIStringDict(config_node.attrib)
    if config_node.tag.lower() == "arjuna_option":
        config_container.set_arjuna_option(config_attrs['name'], config_attrs['value'])
    else:
        config_container.set_user_option(config_attrs['name'], config_attrs['value'])


def validate_fixture_xml_child(conf_type, object_type, session_path, fixture_node):
    if fixture_node.tag.lower() != 'fixture':
        display_err_and_exit(conf_type, ">>fixtures<< element can only contain one or more children of type >>fixture<<.")
    for k,v in fixture_node.attrib.items():
        if k.lower() not in ALLOWED_FIXTURE_ATTRS:
            display_err_and_exit(conf_type, ">>fixtures<< attributes can only be set as: {}.".format(ALLOWED_FIXTURE_ATTRS))
    if not ALLOWED_FIXTURE_ATTRS.issubset(fixture_node.attrib):
        display_err_and_exit(conf_type, ">>fixtures<< element must define >>type<<, >>module<< and >>func<< attributes.")
    for k,v in fixture_node.attrib.items():
        if fixture_node.attrib['type'].lower() not in VALID_FIXTURES[object_type.lower()]:
            display_err_and_exit(
                conf_type,
                session_path,
                ">>fixtures<< element inside >>{}<< can only only contain one of these fixture types: {}".format(
                            object_type,
                            VALID_FIXTURES[object_type.lower()]
                )
            )

def add_fixture_node_to_fixdefs(fixture_defs, fixture_node):
    fixture_attrs = CIStringDict(fixture_node.attrib)

    ConfiguredFixtureHelper.configure_fixture(
        fixture_defs,
        fixture_attrs['type'].upper(),
        fixture_attrs['module'].strip(),
        fixture_attrs['func'].strip()
    )


def validate_stage_xml_child(conf_type, session_path, stage_node):
    if stage_node.tag.lower() != 'stage':
        display_err_and_exit(conf_type, session_path, ">>stages<< element can only contain one or more children of type >>stage<<.")
    for k,v in stage_node.attrib.items():
        if k.lower() not in ALLOWED_STAGE_ATTRS:
            display_err_and_exit(conf_type, session_path, ">>stage<< attributes can only be set as: {}.".format(ALLOWED_STAGE_ATTRS))


def validate_group_xml_child(conf_type, session_path, group_node):
    if group_node.tag.lower() != 'group':
        display_err_and_exit(conf_type, session_path, ">>groups<< element can only contain one or more children of type >>group<<.")
    for k,v in group_node.attrib.items():
        if k.lower() not in ALLOWED_GROUP_ATTRS:
            display_err_and_exit(conf_type, session_path, ">>group<< attributes can only be set as: {}.".format(ALLOWED_GROUP_ATTRS))
    if not MANDATORY_GROUP_ATTRS.issubset(etree_utils.convert_attribs_to_cidict(group_node)):
        display_err_and_exit(conf_type, session_path, ">>group<< element must define these attributes: {}".format(MANDATORY_GROUP_ATTRS))


def validate_gconf_xml_child(conf_type, groups_path, gconf_node):
    if gconf_node.tag.lower() != 'group':
        display_err_and_exit(conf_type, groups_path, ">>groups<< element can only contain one or more children of type >>group<<.")
    for k,v in gconf_node.attrib.items():
        if k.lower() not in ALLOWED_GCONF_ATTRS:
            display_err_and_exit(conf_type, groups_path, ">>group<< attributes can only be set as: {}.".format(ALLOWED_GCONF_ATTRS))
    if not MANDATORY_GCONF_ATTRS.issubset(etree_utils.convert_attribs_to_cidict(gconf_node)):
        display_err_and_exit(conf_type, groups_path, ">>group<< element must define these attributes: {}".format(MANDATORY_GCONF_ATTRS))

def validate_pattern_xml_child(conf_type, group_name, groups_path, pattern_node):
    for k, v in pattern_node.attrib.items():
        if k.lower() not in ALLOWED_PATTERN_ATTRS:
            display_err_and_exit(conf_type, groups_path,
                                 ">>patten<< attributes can only be set as: {}. Check group: {}".format(ALLOWED_PATTERN_ATTRS, group_name))
    if not MANDATORY_PATTERN_ATTRS.issubset(etree_utils.convert_attribs_to_cidict(pattern_node)):
        display_err_and_exit(conf_type, groups_path,
                             ">>pattern<< element must define these attributes: {}. Check group: {}".format(MANDATORY_PATTERN_ATTRS, group_name))

def validate_rule_xml_child(conf_type, group_name, groups_path, rule_node):
    for k, v in rule_node.attrib.items():
        if k.lower() not in ALLOWED_RULE_ATTRS:
            display_err_and_exit(conf_type, groups_path,
                                 ">>patten<< attributes can only be set as: {}. Check group: {}".format(ALLOWED_RULE_ATTRS, group_name))
    if not MANDATORY_RULE_ATTRS.issubset(etree_utils.convert_attribs_to_cidict(rule_node)):
        display_err_and_exit(conf_type, groups_path,
                             ">>pattern<< element must define these attributes: {}. Check group: {}".format(MANDATORY_RULE_ATTRS, group_name))