#!/usr/bin/env python

from xmlnative.types import make_dictionary, List, Object, associate
from lxml import etree

# ---------- Dictionary Demo ----------

dtree = etree.fromstring("""
<Dict>
    <Entry>
        <Key>Foo</Key>
        <Value>Bar</Value>
    </Entry>
    <Entry>
        <Key>Foo2</Key>
        <Value>
            <Other>foo</Other>
        </Value>
    </Entry>
    <Entry>
        <Key><Invalid/></Key>
        <Value>Invalid dict entry</Value>
    </Entry>
</Dict>
""")


Dictionary = make_dictionary(element='Entry', key='Key', value='Value')
d = Dictionary(dtree)

# length
assert len(d) == 2, "Wrong length"

# lookup
assert d['Foo'] == 'Bar', "String lookup"
assert type(d['Foo2']) == etree._Element, "Wrong type"

# assignment
d['Goo'] = "hello"
assert d['Goo'] == "hello", "Set failed"

# contains()
assert 'Goo' in d, "Contains failed"

print(f'repr: {d}')


# ---------- List ----------

ltree = etree.fromstring("""
<List>
    <Item>Foo</Item>
    <Item>Foo</Item>
    <Item>Foo</Item>
</List>
""")

l = List(ltree)

assert len(l) == 3, "Wrong length"

# ---------- Object ----------

otree = etree.fromstring("""
<KnownObj>
    <Item1/>
    <Item2/>
    <Item3/>
</KnownObj>
""")

o = Object(otree)


# ---------- Automatic Associations ----------

tree = etree.fromstring("""
<Dict>
    <Entry>
        <Key>somekey</Key>
        <Value>somevalue</Value>
    </Entry>
    <Entry>
        <Key>anotherkey</Key>
        <Value>
            <List>
                <KnownObj>
                    <Attr1/>
                    <Attr2/>
                </KnownObj>
                <UnknownObj/>
                <UnknownObj/>
                <UnknownObj/>
            </List>
        </Value>
    </Entry>
</Dict>
""")

MyDict = make_dictionary(element='Entry', key='Key', value='Value')
associations = {
    'Dict': MyDict,
    'List': List,
    'KnownObj': Object,
}
result = associate(tree, associations)
print(result)
