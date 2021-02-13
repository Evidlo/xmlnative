#!/usr/bin/env python

from lxml import etree
from lxml.etree import _Element
from lxml.builder import E
from collections.abc import MutableMapping, MutableSequence

def associate(element, associations):
    if associations is not None and element.tag in associations:
        return associations[element.tag](element, associations)
    else:
        return element


class XMLNative(object):

    def __init__(self, e, associations=None):
        self.e = e
        self.associations = associations


class Object(XMLNative):

    def __repr__(self):
        return self.e.tag

    def __getattr__(self, attr):
        return associate(self.e.find(attr), self.associations)

    # FIXME: use __dict__ instead?
    def __dir__(self):
        children = self.e.getchildren()
        return {e.tag:e for e in children}


def make_dictionary(*, element, key, value):

    return type(
        'Dictionary',
        (Dictionary,),
        {
            'element': element,
            'key': key,
            'value': value
        }
    )


class Dictionary(MutableMapping, XMLNative):

    def _cast(self, e):
        """Cast value tag contents into string or list of children"""
        children = e.getchildren()
        if len(children) >= 2:
            return [associate(c, self.associations) for c in children]
        elif len(children) == 1:
            return associate(children[0], self.associations)
        else:
            return e.text

    def _getelement(self, key):
        xpath = f'{self.element}/{self.key}[text()="{key}"]/..'
        elements = self.e.xpath(xpath)
        if len(elements) >= 2:
            raise Exception("Key not unique")
        if len(elements) != 1:
            raise KeyError
        return elements[0]

    def __getitem__(self, key):
        element = self._getelement(key)
        return self._cast(element.find(self.value))

    def __setitem__(self, key, value):
        self.__delitem__(key)
        self.e.append(
            getattr(E, self.element)(
                getattr(E, self.key)(key),
                getattr(E, self.value)(value)
            )
        )

    def __delitem__(self, key):
        try:
            results = self._getelement(key)
        except KeyError:
            pass
        else:
            if results is not None:
                self.e.remove(results)

    def __contains__(self, key):
        try:
            self._getelement(key)
        except KeyError:
            return False

        return True

    def __iter__(self):
        # only get keys with no children
        xpath = f'{self.element}/{self.key}[not(*)]'
        # Get .text from each key element
        for key in self.e.xpath(xpath):
            yield key.text

    def __len__(self):
        # only get keys with no children
        xpath = f'{self.element}/{self.key}[not(*)]'
        return len(self.e.xpath(xpath))

    def __repr__(self):
        # only get elements whose keys have no children
        xpath = f'{self.element}/{self.key}[not(*)]/..'
        d = {}
        for element in self.e.xpath(xpath):
            k = element.find(self.key).text
            v = self._cast(element.find(self.value))
            d[k] = v
        return str(d)


class List(MutableSequence, XMLNative):

    def __iter__(self):
        return self.e.__iter__()

    def __getitem__(self, key):
        return associate(self.e.__getitem__(key), self.associations)

    def __setitem__(self, key, item):
        return self.e.__setitem__(key, item)

    def __delitem__(self, item):
        return self.e.__delitem__(item)

    def __len__(self):
        return self.e.__len__()

    def __contains__(self, item):
        return self.e.__contains__(item)

    def insert(self, index, item):
        return self.e.insert(index, item)

    def __repr__(self):
        l = []
        for child in self.e.getchildren():
            l.append(associate(child, self.associations))

        return str(l)
