#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_services
----------------------------------

Tests for `teamsupport.services` module.
"""
import unittest

from lxml import etree

from teamsupport.services import XMLHTTPServiceClient
from tests import PatchedSessionTests


class PatchedSessionXMLTests(PatchedSessionTests):
    def assertEqualXML(self, first, second, msg=None):
        self.assertEqual(etree.tostring(first), etree.tostring(second), msg)


class TestBaseXMLClient(PatchedSessionXMLTests):

    def setUp(self):
        super(TestBaseXMLClient, self).setUp()
        self.client = XMLHTTPServiceClient(url='https://localhost/')

    def test_parse_xml_response_returns_element(self):
        self.response.content = '<Tickets></Tickets>'
        result = self.client.parse_xml_response(self.response)
        self.assertEqualXML(result, etree.Element('Tickets'))

    def test_send_as_xml_properly_formats_request(self):
        request_params = {
            'cdata': {'Field2URL': "<a href='https://localhost/test'>test<a>"},
            'data': {'Field1': 'Test field'},
            'root': 'OuterField',
            'send_as_xml': True
        }
        request_params = self.client._format_xml_request(request_params)
        root_element = etree.Element('OuterField')
        sub_element = etree.SubElement(root_element, 'Field1')
        sub_element.text = 'Test field'
        sub_element = etree.SubElement(root_element, 'Field2URL')
        sub_element.text = etree.CDATA(
            "<a href='https://localhost/test'>test<a>")
        xml_string = etree.tostring(
            root_element, encoding='utf-8', xml_declaration=True,
            pretty_print=True)

        self.assertEqual(request_params['data'], xml_string)
        self.assertEqual(
            request_params['headers']['Content-Type'], 'application/xml')

    def test_send_as_xml_properly_formats_xml(self):
        request_element = etree.Element('OuterField')
        sub_element = etree.SubElement(request_element, 'Field1')
        sub_element.text = 'Test field'
        request_params = {
            'data': request_element,
            'send_as_xml': True
        }
        request_params = self.client._format_xml_request(request_params)

        root_element = etree.Element('OuterField')
        sub_element = etree.SubElement(root_element, 'Field1')
        sub_element.text = 'Test field'
        xml_string = etree.tostring(
            root_element, encoding='utf-8', xml_declaration=True,
            pretty_print=True)

        self.assertEqual(request_params['data'], xml_string)
        self.assertEqual(
            request_params['headers']['Content-Type'], 'application/xml')

    def tearDown(self):
        super(TestBaseXMLClient, self).tearDown()

if __name__ == '__main__':
    unittest.main()
