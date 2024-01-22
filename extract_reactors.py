import re
import csv
import requests

from lxml import html


COLUMN_NAMES = [
    'Country',
    'Plant name',
    'Unit No.',
    'Type',
    'Model',
    'Status',
    'Capacity (MW)',
    'Begin building',
    'Commercial operation',
    'Closed',
]


KNOWN_STATUSES = {
    'Planned',
    'Operational',
    'Under construction',
    'Decommissioned',
    'Shut down',
    'Unfinished',
    'Finished; never entered service',
    'Cancelled',
    'Shut down/in decommissioning',
    'Dismantled',
    'Shut down/decommissioned',
    'Never built',
    'Unfinished; restart planned',
    'Inoperable',
    'Operation suspended(under review)',
    'Operation suspended',
    'Operation suspended(restart approved)',
    'Under construction(suspended)',
    'Destroyed',
    'Core melt',
    'Under commissioning',
}


RE_YEAR = re.compile(r'(?:(?:\d{1,2}\s)?[A-Z][a-z]{2}\s)?(\d{4})')
RE_PLANNED_YEAR = re.compile(r'\((\d{4})\)|\(\d{4}–(\d{4})\)')

def extract_year(s: str) -> str:
    if len(s) == 0:
        return s
    if m := re.match(RE_YEAR, s):
        assert m.group(1), f'Cannot extract year from "{s}"'
        return m.group(1)
    if m := re.match(RE_PLANNED_YEAR, s):
        return ''
    assert False, f'Cannot extract year from "{s}"'


def extract_row_text(element) -> str:
    return ''.join(element.xpath("text()|*[not(name()='sub') and not(name()='sup')]/text()")).rstrip(' \n')


def main():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_commercial_nuclear_reactors')
    tree = html.fromstring(resp.text)
    with open('reactors.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        
        writer.writerow(COLUMN_NAMES)

        headers = tree.xpath('//h2[span]')
        tables = tree.xpath("//table[contains(@class,'wikitable')]")
        for header, table in zip(headers, tables):
            country = header[0].text
            prev_station = None
            num_headers = None
            prev_block_number = None
            for element_row in table.xpath('./tbody/tr'):
                row = [extract_row_text(e) for e in element_row.xpath('td')]
                if len(row) == 0:
                    # Header row
                    assert len(element_row.xpath('th')) <= len(COLUMN_NAMES)
                    continue

                assert len(row) <= len(COLUMN_NAMES)
                s0 = row[3]
                s1 = row[4]
                assert s0 in KNOWN_STATUSES or s1 in KNOWN_STATUSES, f'Neither {s0} nor {s1} is a knows status'

                if row[4] in KNOWN_STATUSES:
                    prev_station = row[0]
                    row = [country] + row
                else:
                    row = [country, prev_station] + row

                for i in (7, 8, 9):
                    if i < len(row):
                        row[i] = extract_year(row[i])

                #print(row)
                row = ['' if s is None else s for s in row]
                row.extend('' for i in range(len(COLUMN_NAMES) - len(row)))

                writer.writerow(row[0:len(COLUMN_NAMES)])


if __name__ == "__main__":
    main()
