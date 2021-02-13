# xmlnative

Recursive mapping of XML to native python types.

## Usage

``` python
>>> from lxml import etree
>>> tree = etree.fromstring("""
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
>>> MyDict = make_dictionary(element='Entry', key='Key', value='Value')
>>> associations = {
        'Dict': MyDict,
        'List': List,
        'KnownObj': Object,
    }
>>> result = associate(tree, associations)
>>> print(result)
{'somekey': 'somevalue', 'anotherkey': [KnownObj, <Element UnknownObj at 0x7f161850de00>, <Element UnknownObj at 0x7f161850db40>, <Element UnknownObj at 0x7f16183e4680>]}
>>> print(result['somekey'])
somevalue
>>> print(result['anotherkey'])
[KnownObj, <Element UnknownObj at 0x7f16183208c0>, <Element UnknownObj at 0x7f1618320500>, <Element UnknownObj at 0x7f1618320440>
>>> print(result['anotherkey'][0].Attr1)
<Element Attr1 at 0x7f1618464240>
```

Full example available in `example.py`.

## Types

There are 3 basic types:

**List**

List type for lists of objects.  Child elements are accessible as regular list indices.

**Dictionary**

Mapping type for XML dictionaries.  Dictionary classes are generated with the `make_dictionary` function.  You must provide the tags for key/value elements and their containing element.  Key elements are assumed to be childless and their text contents unique.

**Object**

Generic type. Child elements are accessible by accessing the attribute corresponding to the element tag on the returned object.  The tags of each child are assumed to be unique.
