# The test are based on tests for jsonpath-rw-ext in https://github.com/sileht/python-jsonpath-rw-ext

from __future__ import unicode_literals, print_function, absolute_import, division, generators, nested_scopes
from arjuna import *

scenarios = [
    ('sorted_list', dict(string='objects.`sorted`',
                            data={'objects': ['alpha', 'gamma', 'beta']},
                            target=[['alpha', 'beta', 'gamma']])),
    ('sorted_list_indexed', dict(string='objects.`sorted`[1]',
                                    data={'objects': [
                                        'alpha', 'gamma', 'beta']},
                                    target=['beta'])),
    ('sorted_dict', dict(string='objects.`sorted`',
                            data={'objects': {'cow': 'moo', 'horse': 'neigh',
                                            'cat': 'meow'}},
                            target=[['cat', 'cow', 'horse']])),
    ('sorted_dict_indexed', dict(string='objects.`sorted`[0]',
                                    data={'objects': {'cow': 'moo',
                                                    'horse': 'neigh',
                                                    'cat': 'meow'}},
                                    target=['cat'])),

    ('len_list', dict(string='objects.`len`',
                        data={'objects': ['alpha', 'gamma', 'beta']},
                        target=[3])),
    ('len_dict', dict(string='objects.`len`',
                        data={'objects': {'cow': 'moo', 'cat': 'neigh'}},
                        target=[2])),
    ('len_str', dict(string='objects[0].`len`',
                        data={'objects': ['alpha', 'gamma']},
                        target=[5])),

    ('filter_exists_syntax1', dict(string='objects[?cow]',
                                    data={'objects': [{'cow': 'moo'},
                                                        {'cat': 'neigh'}]},
                                    target=[{'cow': 'moo'}])),
    ('filter_exists_syntax2', dict(string='objects[?@.cow]',
                                    data={'objects': [{'cow': 'moo'},
                                                        {'cat': 'neigh'}]},
                                    target=[{'cow': 'moo'}])),
    ('filter_exists_syntax3', dict(string='objects[?(@.cow)]',
                                    data={'objects': [{'cow': 'moo'},
                                                        {'cat': 'neigh'}]},
                                    target=[{'cow': 'moo'}])),
    ('filter_exists_syntax4', dict(string='objects[?(@."cow!?cat")]',
                                    data={'objects': [{'cow!?cat': 'moo'},
                                                        {'cat': 'neigh'}]},
                                    target=[{'cow!?cat': 'moo'}])),
    ('filter_eq1', dict(string='objects[?cow="moo"]',
                        data={'objects': [{'cow': 'moo'},
                                            {'cow': 'neigh'},
                                            {'cat': 'neigh'}]},
                        target=[{'cow': 'moo'}])),
    ('filter_eq2', dict(string='objects[?(@.["cow"]="moo")]',
                        data={'objects': [{'cow': 'moo'},
                                            {'cow': 'neigh'},
                                            {'cat': 'neigh'}]},
                        target=[{'cow': 'moo'}])),
    ('filter_eq3', dict(string='objects[?cow=="moo"]',
                        data={'objects': [{'cow': 'moo'},
                                            {'cow': 'neigh'},
                                            {'cat': 'neigh'}]},
                        target=[{'cow': 'moo'}])),
    ('filter_eq4', dict(string='objects[?id==154]',
                        data={'objects': [{'id': 154},
                                            {'id': 155},
                                            {'id': None}]},
                        target=[{'id': 154}])),
    ('filter_gt', dict(string='objects[?cow>5]',
                        data={'objects': [{'cow': 8},
                                            {'cow': 7},
                                            {'cow': 5},
                                            {'cow': 'neigh'}]},
                        target=[{'cow': 8}, {'cow': 7}])),
    ('filter_and', dict(string='objects[?cow>5&cat=2]',
                        data={'objects': [{'cow': 8, 'cat': 2},
                                            {'cow': 7, 'cat': 2},
                                            {'cow': 2, 'cat': 2},
                                            {'cow': 5, 'cat': 3},
                                            {'cow': 8, 'cat': 3}]},
                        target=[{'cow': 8, 'cat': 2},
                                {'cow': 7, 'cat': 2}])),
    ('filter_float_gt', dict(
        string='objects[?confidence>=0.5].prediction',
        data={
            'objects': [
                {'confidence': 0.42,
                    'prediction': 'Good'},
                {'confidence': 0.58,
                    'prediction': 'Bad'},
            ]
        },
        target=['Bad']
    )),
    ('filter_regex', dict(
        string='objects[?prediction ~ ".*d$"].confidence',
        data={
            'objects': [
                {'confidence': 0.42,
                    'prediction': 'Good'},
                {'confidence': 0.48,
                    'prediction': 'Average'},
                {'confidence': 0.58,
                    'prediction': 'Bad'},
            ]
        },
        target=[0.42, 0.58]
    )),
    ('sort1', dict(string='objects[/cow]',
                    data={'objects': [{'cat': 1, 'cow': 2},
                                        {'cat': 2, 'cow': 1},
                                        {'cat': 3, 'cow': 3}]},
                    target=[[{'cat': 2, 'cow': 1},
                            {'cat': 1, 'cow': 2},
                            {'cat': 3, 'cow': 3}]])),
    ('sort1_indexed', dict(string='objects[/cow][0].cat',
                            data={'objects': [{'cat': 1, 'cow': 2},
                                                {'cat': 2, 'cow': 1},
                                                {'cat': 3, 'cow': 3}]},
                            target=[2])),
    ('sort2', dict(string='objects[\cat]',
                    data={'objects': [{'cat': 2}, {'cat': 1}, {'cat': 3}]},
                    target=[[{'cat': 3}, {'cat': 2}, {'cat': 1}]])),
    ('sort2_indexed', dict(string='objects[\cat][-1].cat',
                            data={'objects': [{'cat': 2}, {'cat': 1},
                                                {'cat': 3}]},
                            target=[1])),
    ('sort3', dict(string='objects[/cow,\cat]',
                    data={'objects': [{'cat': 1, 'cow': 2},
                                        {'cat': 2, 'cow': 1},
                                        {'cat': 3, 'cow': 1},
                                        {'cat': 3, 'cow': 3}]},
                    target=[[{'cat': 3, 'cow': 1},
                            {'cat': 2, 'cow': 1},
                            {'cat': 1, 'cow': 2},
                            {'cat': 3, 'cow': 3}]])),
    ('sort3_indexed', dict(string='objects[/cow,\cat][0].cat',
                            data={'objects': [{'cat': 1, 'cow': 2},
                                                {'cat': 2, 'cow': 1},
                                                {'cat': 3, 'cow': 1},
                                                {'cat': 3, 'cow': 3}]},
                            target=[3])),
    ('sort4', dict(string='objects[/cat.cow]',
                    data={'objects': [{'cat': {'dog': 1, 'cow': 2}},
                                        {'cat': {'dog': 2, 'cow': 1}},
                                        {'cat': {'dog': 3, 'cow': 3}}]},
                    target=[[{'cat': {'dog': 2, 'cow': 1}},
                            {'cat': {'dog': 1, 'cow': 2}},
                            {'cat': {'dog': 3, 'cow': 3}}]])),
    ('sort4_indexed', dict(string='objects[/cat.cow][0].cat.dog',
                            data={'objects': [{'cat': {'dog': 1,
                                                        'cow': 2}},
                                                {'cat': {'dog': 2,
                                                        'cow': 1}},
                                                {'cat': {'dog': 3,
                                                        'cow': 3}}]},
                            target=[2])),
    ('sort5_twofields', dict(string='objects[/cat.(cow,bow)]',
                                data={'objects':
                                    [{'cat': {'dog': 1, 'bow': 3}},
                                    {'cat': {'dog': 2, 'cow': 1}},
                                    {'cat': {'dog': 2, 'bow': 2}},
                                    {'cat': {'dog': 3, 'cow': 2}}]},
                                target=[[{'cat': {'dog': 2, 'cow': 1}},
                                        {'cat': {'dog': 2, 'bow': 2}},
                                        {'cat': {'dog': 3, 'cow': 2}},
                                        {'cat': {'dog': 1, 'bow': 3}}]])),

    ('sort5_indexed', dict(string='objects[/cat.(cow,bow)][0].cat.dog',
                            data={'objects':
                                    [{'cat': {'dog': 1, 'bow': 3}},
                                    {'cat': {'dog': 2, 'cow': 1}},
                                    {'cat': {'dog': 2, 'bow': 2}},
                                    {'cat': {'dog': 3, 'cow': 2}}]},
                            target=[2])),
    ('arithmetic_number_only', dict(string='3 * 3', data={},
                                    target=[9])),

    ('arithmetic_mul1', dict(string='$.foo * 10', data={'foo': 4},
                                target=[40])),
    ('arithmetic_mul2', dict(string='10 * $.foo', data={'foo': 4},
                                target=[40])),
    ('arithmetic_mul3', dict(string='$.foo * 10', data={'foo': 4},
                                target=[40])),
    ('arithmetic_mul4', dict(string='$.foo * 3', data={'foo': 'f'},
                                target=['fff'])),
    ('arithmetic_mul5', dict(string='foo * 3', data={'foo': 'f'},
                                target=['foofoofoo'])),
    ('arithmetic_mul6', dict(string='($.foo * 10 * $.foo) + 2',
                                data={'foo': 4}, target=[162])),
    ('arithmetic_mul7', dict(string='$.foo * 10 * $.foo + 2',
                                data={'foo': 4}, target=[240])),

    ('arithmetic_str0', dict(string='foo + bar',
                                data={'foo': 'name', "bar": "node"},
                                target=["foobar"])),
    ('arithmetic_str1', dict(string='foo + "_" + bar',
                                data={'foo': 'name', "bar": "node"},
                                target=["foo_bar"])),
    ('arithmetic_str2', dict(string='$.foo + "_" + $.bar',
                                data={'foo': 'name', "bar": "node"},
                                target=["name_node"])),
    ('arithmetic_str3', dict(string='$.foo + $.bar',
                                data={'foo': 'name', "bar": "node"},
                                target=["namenode"])),
    ('arithmetic_str4', dict(string='foo.cow + bar.cow',
                                data={'foo': {'cow': 'name'},
                                    "bar": {'cow': "node"}},
                                target=["namenode"])),

    ('arithmetic_list1', dict(string='$.objects[*].cow * 2',
                                data={'objects': [{'cow': 1},
                                                {'cow': 2},
                                                {'cow': 3}]},
                                target=[2, 4, 6])),

    ('arithmetic_list2', dict(string='$.objects[*].cow * $.objects[*].cow',
                                data={'objects': [{'cow': 1},
                                                {'cow': 2},
                                                {'cow': 3}]},
                                target=[1, 4, 9])),

    ('arithmetic_list_err1', dict(
        string='$.objects[*].cow * $.objects2[*].cow',
        data={'objects': [{'cow': 1}, {'cow': 2}, {'cow': 3}],
                'objects2': [{'cow': 5}]},
        target=[])),

    ('arithmetic_err1', dict(string='$.objects * "foo"',
                                data={'objects': []}, target=[])),
    ('arithmetic_err2', dict(string='"bar" * "foo"', data={}, target=[])),

    ('real_life_example1', dict(
        string="payload.metrics[?(@.name='cpu.frequency')].value * 100",
        data={'payload': {'metrics': [
            {'timestamp': '2013-07-29T06:51:34.472416',
                'name': 'cpu.frequency',
                'value': 1600,
                'source': 'libvirt.LibvirtDriver'},
            {'timestamp': '2013-07-29T06:51:34.472416',
                'name': 'cpu.user.time',
                'value': 17421440000000,
                'source': 'libvirt.LibvirtDriver'}]}},
        target=[160000])),

    ('real_life_example2', dict(
        string="payload.(id|(resource.id))",
        data={'payload': {'id': 'foobar'}},
        target=['foobar'])),
    ('real_life_example3', dict(
        string="payload.id|(resource.id)",
        data={'payload': {'resource':
                            {'id': 'foobar'}}},
        target=['foobar'])),
    ('real_life_example4', dict(
        string="payload.id|(resource.id)",
        data={'payload': {'id': 'yes',
                            'resource': {'id': 'foobar'}}},
        target=['yes', 'foobar'])),

    ('sub1', dict(
        string="payload.`sub(/(foo\\\\d+)\\\\+(\\\\d+bar)/, \\\\2-\\\\1)`",
        data={'payload': "foo5+3bar"},
        target=["3bar-foo5"]
    )),
    ('sub2', dict(
        string='payload.`sub(/foo\\\\+bar/, repl)`',
        data={'payload': "foo+bar"},
        target=["repl"]
    )),

    ('split1', dict(
        string='payload.`split(-, 2, -1)`',
        data={'payload': "foo-bar-cat-bow"},
        target=["cat"]
    )),
    ('split2', dict(
        string='payload.`split(-, 2, 2)`',
        data={'payload': "foo-bar-cat-bow"},
        target=["cat-bow"]
    )),

    ('bug-#2-correct', dict(
        string='foo[?(@.baz==1)]',
        data={'foo': [{'baz': 1}, {'baz': 2}]},
        target=[{'baz': 1}],
    )),

    ('bug-#2-wrong', dict(
        string='foo[*][?(@.baz==1)]',
        data={'foo': [{'baz': 1}, {'baz': 2}]},
        target=[],
    )),

    ('boolean-filter-true', dict(
        string='foo[?flag = true].color',
        data={'foo': [{"color": "blue", "flag": True},
                        {"color": "green", "flag": False}]},
        target=['blue']
    )),

    ('boolean-filter-false', dict(
        string='foo[?flag = false].color',
        data={'foo': [{"color": "blue", "flag": True},
                        {"color": "green", "flag": False}]},
        target=['green']
    )),

    ('boolean-filter-other-datatypes-involved', dict(
        string='foo[?flag = true].color',
        data={'foo': [{"color": "blue", "flag": True},
                        {"color": "green", "flag": 2},
                        {"color": "red", "flag": "hi"}]},
        target=['blue']
    )),

    ('boolean-filter-string-true-string-literal', dict(
        string='foo[?flag = "true"].color',
        data={'foo': [{"color": "blue", "flag": True},
                        {"color": "green", "flag": "true"}]},
        target=['green']
    )),
]

@test
def check_fields_value_jsonext(request):
    Json.reset_auto_id_key()
    for scenario in scenarios:
        print(scenario[0])
        data = scenario[1]
        print('parse("%s").find(%s) =?= %s' % (data['string'], data['data'], data['target']))
        result = Json.from_object(data['data'], allow_any=True).findall(data['string'])
        print(result)
        assert result == data['target']