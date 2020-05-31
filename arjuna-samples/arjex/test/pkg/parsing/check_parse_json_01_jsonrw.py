from arjuna import *
from jsonpath_rw import jsonpath
from jsonpath_rw.parser import parse
from jsonpath_rw.jsonpath import *
from jsonpath_rw.lexer import JsonPathLexerError

# The test are taken from https://github.com/kennknowles/python-jsonpath-rw

def __test_cases(test_cases):
    # Note that just manually building an AST would avoid this dep and isolate the tests, but that would suck a bit
    # Also, we coerce iterables, etc, into the desired target type

    for string, data, target in test_cases:
        print('parse("%s").find(%s) =?= %s' % (string, data, target))
        #result = parse(string).find(data)
        result = Json.from_object(data).findall(string)
        print(result)
        assert [r for r in result] == target
        # if isinstance(target, list):
        #     assert [r.value for r in result] == target
        # elif isinstance(target, set):
        #     assert set([r.value for r in result]) == target
        # else:
        #     assert result.value == target

@test
def check_fields_value(request):
    jsonpath.auto_id_field = None
    __test_cases([ ('foo', {'foo': 'baz'}, ['baz']),
                        ('foo,baz', {'foo': 1, 'baz': 2}, [1, 2]),
                        ('@foo', {'@foo': 1}, [1]),
                        ('*', {'foo': 1, 'baz': 2}, [1, 2]) ])

    jsonpath.auto_id_field = 'id'
    __test_cases([ ('*', {'foo': 1, 'baz': 2}, [1, 2, '`this`']) ])


@test
def check_root_value(request):
    jsonpath.auto_id_field = None
    __test_cases([ 
        ('$', {'foo': 'baz'}, [{'foo':'baz'}]),
        ('foo.$', {'foo': 'baz'}, [{'foo':'baz'}]),
        ('foo.$.foo', {'foo': 'baz'}, ['baz']),
    ])


@test
def check_this_value(request):
    jsonpath.auto_id_field = None
    __test_cases([ 
        ('`this`', {'foo': 'baz'}, [{'foo':'baz'}]),
        ('foo.`this`', {'foo': 'baz'}, ['baz']),
        ('foo.`this`.baz', {'foo': {'baz': 3}}, [3]),
    ])


@test
def check_index_value(request):
    __test_cases([
        ('[0]', [42], [42]),
        ('[5]', [42], []),
        ('[2]', [34, 65, 29, 59], [29]),
        # ('[0]', None, [])
    ])


@test
def check_slice_value(request):
    __test_cases([('[*]', [1, 2, 3], [1, 2, 3]),
                        ('[*]', xrange(1, 4), [1, 2, 3]),
                        ('[1:]', [1, 2, 3, 4], [2, 3, 4]),
                        ('[:2]', [1, 2, 3, 4], [1, 2])])

    # Funky slice hacks
    __test_cases([
        ('[*]', 1, [1]), # This is a funky hack
        ('[0:]', 1, [1]), # This is a funky hack
        ('[*]', {'foo':1}, [{'foo': 1}]), # This is a funky hack
        ('[*].foo', {'foo':1}, [1]), # This is a funky hack
    ])


@test
def check_child_value(request):
    __test_cases([('foo.baz', {'foo': {'baz': 3}}, [3]),
                        ('foo.baz', {'foo': {'baz': [3]}}, [[3]]),
                        ('foo.baz.bizzle', {'foo': {'baz': {'bizzle': 5}}}, [5])])


@test
def check_descendants_value(request):
    __test_cases([ 
        ('foo..baz', {'foo': {'baz': 1, 'bing': {'baz': 2}}}, [1, 2] ),
        ('foo..baz', {'foo': [{'baz': 1}, {'baz': 2}]}, [1, 2] ), 
    ])


@test
def check_parent_value(request):
    __test_cases([('foo.baz.`parent`', {'foo': {'baz': 3}}, [{'baz': 3}]),
                        ('foo.`parent`.foo.baz.`parent`.baz.bizzle', {'foo': {'baz': {'bizzle': 5}}}, [5])])

#
# Check that the paths for the data are correct.
# FIXME: merge these tests with the above, since the inputs are the same anyhow
#

def __test_paths(test_cases):
    # Note that just manually building an AST would avoid this dep and isolate the tests, but that would suck a bit
    # Also, we coerce iterables, etc, into the desired target type

    for string, data, target in test_cases:
        print('parse("%s").find(%s).paths =?= %s' % (string, data, target))
        result = parse(string).find(data)
        if isinstance(target, list):
            assert [str(r.full_path) for r in result] == target
        elif isinstance(target, set):
            assert set([str(r.full_path) for r in result]) == target
        else:
            assert str(result.path) == target


@test
def check_fields_paths(request):
    jsonpath.auto_id_field = None
    __test_paths([ ('foo', {'foo': 'baz'}, ['foo']),
                        ('foo,baz', {'foo': 1, 'baz': 2}, ['foo', 'baz']),
                        ('*', {'foo': 1, 'baz': 2}, set(['foo', 'baz'])) ])

    jsonpath.auto_id_field = 'id'
    __test_paths([ ('*', {'foo': 1, 'baz': 2}, set(['foo', 'baz', 'id'])) ])


@test
def check_root_paths(request):
    jsonpath.auto_id_field = None
    __test_paths([ 
        ('$', {'foo': 'baz'}, ['$']),
        ('foo.$', {'foo': 'baz'}, ['$']),
        ('foo.$.foo', {'foo': 'baz'}, ['foo']),
    ])


@test
def check_this_paths(request):
    jsonpath.auto_id_field = None
    __test_paths([ 
        ('`this`', {'foo': 'baz'}, ['`this`']),
        ('foo.`this`', {'foo': 'baz'}, ['foo']),
        ('foo.`this`.baz', {'foo': {'baz': 3}}, ['foo.baz']),
    ])


@test
def check_index_paths(request):
    __test_paths([('[0]', [42], ['[0]']),
                        ('[2]', [34, 65, 29, 59], ['[2]'])])


@test
def check_slice_paths(request):
    __test_paths([ ('[*]', [1, 2, 3], ['[0]', '[1]', '[2]']),
                        ('[1:]', [1, 2, 3, 4], ['[1]', '[2]', '[3]']) ])


@test
def check_child_paths(request):
    __test_paths([('foo.baz', {'foo': {'baz': 3}}, ['foo.baz']),
                        ('foo.baz', {'foo': {'baz': [3]}}, ['foo.baz']),
                        ('foo.baz.bizzle', {'foo': {'baz': {'bizzle': 5}}}, ['foo.baz.bizzle'])])


@test
def check_descendants_paths(request):
    __test_paths([('foo..baz', {'foo': {'baz': 1, 'bing': {'baz': 2}}}, ['foo.baz', 'foo.bing.baz'] )])


#
# Check the "auto_id_field" feature
#

@test
def check_fields_auto_id(request):
    jsonpath.auto_id_field = "id"
    __test_cases([ ('foo.id', {'foo': 'baz'}, ['foo']),
                        ('foo.id', {'foo': {'id': 'baz'}}, ['baz']),
                        ('foo,baz.id', {'foo': 1, 'baz': 2}, ['foo', 'baz']),
                        ('*.id', 
                        {'foo':{'id': 1},
                            'baz': 2},
                            set(['1', 'baz'])) ])


@test
def check_root_auto_id(request):
    jsonpath.auto_id_field = 'id'
    __test_cases([ 
        ('$.id', {'foo': 'baz'}, ['$']), # This is a wonky case that is not that interesting
        ('foo.$.id', {'foo': 'baz', 'id': 'bizzle'}, ['bizzle']), 
        ('foo.$.baz.id', {'foo': 4, 'baz': 3}, ['baz']),
    ])


@test
def check_this_auto_id(request):
    jsonpath.auto_id_field = 'id'
    __test_cases([ 
        ('id', {'foo': 'baz'}, ['`this`']), # This is, again, a wonky case that is not that interesting
        ('foo.`this`.id', {'foo': 'baz'}, ['foo']),
        ('foo.`this`.baz.id', {'foo': {'baz': 3}}, ['foo.baz']),
    ])


@test
def check_index_auto_id(request):
    jsonpath.auto_id_field = "id"
    __test_cases([('[0].id', [42], ['[0]']),
                        ('[2].id', [34, 65, 29, 59], ['[2]'])])


@test
def check_slice_auto_id(request):
    jsonpath.auto_id_field = "id"
    __test_cases([ ('[*].id', [1, 2, 3], ['[0]', '[1]', '[2]']),
                        ('[1:].id', [1, 2, 3, 4], ['[1]', '[2]', '[3]']) ])


@test
def check_child_auto_id(request):
    jsonpath.auto_id_field = "id"
    __test_cases([('foo.baz.id', {'foo': {'baz': 3}}, ['foo.baz']),
                        ('foo.baz.id', {'foo': {'baz': [3]}}, ['foo.baz']),
                        ('foo.baz.id', {'foo': {'id': 'bizzle', 'baz': 3}}, ['bizzle.baz']),
                        ('foo.baz.id', {'foo': {'baz': {'id': 'hi'}}}, ['foo.hi']),
                        ('foo.baz.bizzle.id', {'foo': {'baz': {'bizzle': 5}}}, ['foo.baz.bizzle'])])


@test
def check_descendants_auto_id(request):
    jsonpath.auto_id_field = "id"
    __test_cases([('foo..baz.id', 
                        {'foo': {
                            'baz': 1, 
                            'bing': {
                                'baz': 2
                            }
                            } },
                            ['foo.baz', 
                            'foo.bing.baz'] )])
