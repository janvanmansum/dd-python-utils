# Harvest dataset metadata records via the OAI-PMH protocol
import argparse
import os

from datetime import datetime
from lxml import etree

import utils.config as CONFIG

from utils.common.dv_api import get_oai_records, get_oai_records_resume


def save_oai_records(xml_doc, counter, records_output_dir):
    # Improve the next
    # count number of records and print it
    #print(len(xml_doc.findall('.//{http://www.openarchives.org/OAI/2.0/}record')))

    xml_filename = 'recordset_' + str(counter) + '.xml'
    f = open(os.path.join(records_output_dir, xml_filename), "wb")
    # Note that we don't have the XML declaration
    f.write(etree.tostring(xml_doc, pretty_print=True))
    f.close()
    # Note: maybe extract the dataset specific parts and save as individual xml files?


def oai_harvest_command(server_url, output_dir, format, set=None):
    # create directory if needed
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    harvest_dirname = 'oai_harvest_' + format + '_' + timestamp_str
    records_output_dir = os.path.join(output_dir, harvest_dirname)
    os.makedirs(records_output_dir)

    print("Harvesting from: {} format: {} set: {}".format(server_url, format, set))
    print("Storing resutls in: {}".format(os.path.abspath(records_output_dir)))
    xml_doc = get_oai_records(server_url, format=format, set=set)

    counter = 0
    save_oai_records(xml_doc, counter, records_output_dir)

    # get the resumptionToken, sax would be more efficient than DOM here!
    # OAI-PMH/ListRecords/resumptionToken
    token = xml_doc.find('.//{http://www.openarchives.org/OAI/2.0/}resumptionToken')

    # The resumptionToken is empty (no text) when we have all the records
    while token is not None and token.text is not None:
        print("In recordset {}, Resumption token found: {}".format(counter, token.text))
        xml_doc = get_oai_records_resume(server_url, token.text)
        counter += 1
        save_oai_records(xml_doc, counter, records_output_dir)
        token = xml_doc.find('.//{http://www.openarchives.org/OAI/2.0/}resumptionToken')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Harvest dataset metadata records via the OAI-PMH protocol')
    parser.add_argument('-f', '--format', default='oai_dc', help='The format of the records to be harvested.')
    parser.add_argument('-s', '--set', default='', help='The recordset to be harvested.')
    args = parser.parse_args()

    oai_format = args.format  # Note that an important one we have in dataverse is 'oai_datacite'
    oai_set = None
    if args.set:
        oai_set = args.set

    server_url = CONFIG.SERVER_URL
    output_dir = CONFIG.OUTPUT_DIR

    oai_harvest_command(server_url, output_dir, format=oai_format, set=oai_set)
