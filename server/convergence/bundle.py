#-*- coding: utf-8 -*-
from __future__ import print_function


__author__ = 'Moxie Marlinspike'
__email__ = 'moxie@thoughtcrime.org'

__license__= '''
Copyright (c) 2010 Moxie Marlinspike <moxie@thoughtcrime.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA
'''


import sys, textwrap, json

regionCodes = ['AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW',
    'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT',
    'BO', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA',
    'CV', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD', 'CK',
    'CR', 'CI', 'HR', 'CU', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'EL',
    'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF', 'PF', 'TF',
    'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG',
    'GN', 'GW', 'GY', 'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR',
    'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KP',
    'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MO',
    'MK', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX',
    'FM', 'MD', 'MC', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL',
    'AN', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MP', 'NO', 'OM', 'PK', 'PW',
    'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA', 'RE', 'RO',
    'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA',
    'SN', 'RS', 'SC', 'SL', 'SG', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS', 'ES', 'LK',
    'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG',
    'TK', 'TO', 'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US',
    'UM', 'UY', 'UZ', 'VU', 'VE', 'VN', 'VG', 'US', 'VI', 'WF', 'EH', 'YE', 'ZM',
    'ZW']

def loadCertificate(path):
    return open(path).read()

def loopingPrompt(message):
    value = ''
    while value == '':
        value = raw_input(message).strip()

    return value

def promptForLogicalInfo():
    bundle = {'name' : '', 'hosts' : [], 'bundle_location' : '',
        'version' : 1, 'region' : ''}

    print('\n' + textwrap.fill(
        'A notary is a "logical" entity that represents an'
        ' arbitrary number of physical hosts. To create a'
        ' notary bundle, this script will prompt you for general'
        ' information about the logical notary entity, and then for'
        ' information about the physical notary hosts.', 78 ))

    print('\n\n' + textwrap.fill(
        'First, please enter the name of the entity managing this notary.'
        " For an individual, this would be an individual's"
        ' name (eg: John Smith). For an organization, this'
        " would be the organization's name (eg: Acme).", 78 ) + '\n')

    bundle['name'] = loopingPrompt('Notary name: ')

    print('\n\n' + textwrap.fill(
        'Next, please enter the complete URL for where this bundle will'
        ' be hosted (eg: https://ssl.thoughtcrime.org/thoughtcrime.notary). It must'
        ' be an https URL, and the file must have a ".notary"'
        ' extension. This location will be periodically checked by clients for'
        ' updates to your notary configuration.', 78 ) + '\n')

    bundle['bundle_location'] = loopingPrompt('Bundle location: ')

    while (not bundle['bundle_location'].startswith('https://'))\
            or (not bundle['bundle_location'].endswith('.notary')):
        print(textwrap.fill( 'Sorry, the bundle location must be'
            ' an HTTPS URL and have a ".notary" file extension.', 78 ))
        bundle['bundle_location'] = loopingPrompt('Bundle location: ')

    print('\n\n' + textwrap.fill(
        "Next we'll prompt you for a notary region. If all your physical hosts "
        "are located in one country, your notary region would be that country's"
        ' locale abbreviation. If your physical hosts are spread across multiple'
        ' countries and you wish for all of them to be in one logical bundle, simply'
        ' leave this prompt blank.', 78 ) + '\n')

    bundle['region'] = raw_input('Notary region: ').strip()

    while (not bundle['region'] in regionCodes) and (bundle['region'] != ''):
        print(
            textwrap.fill('Sorry, that is not a valid country code.  Must be one of: ', 78)
            + '\n' + textwrap.fill(', '.join(regionCodes), 78) + '\n' )
        bundle['region'] = raw_input('Notary region: ').strip()

    return bundle

def promptForPhysicalInfo(count):
    print('\n' + textwrap.fill(
        'Please enter the hostname for physical host #' + str(count) +
        ' (eg: notary' + str(count) + '.thoughtcrime.org), or leave empty'
        ' if there are no more hosts.', 78 ) + '\n')
    host = raw_input('Hostname: ').strip()

    if len(host.strip()) == 0: return None

    sslPort = int(loopingPrompt(textwrap.fill(host + ' SSL listen port (eg: 443):', 78) + ' '))
    httpPort = int(loopingPrompt(textwrap.fill(host + ' HTTP listen port (eg: 80):', 78) + ' '))
    certificatePath = loopingPrompt(
        textwrap.fill('Path to PEM encoded certificate for ' + host + ':', 78) + ' ' )
    certificate = loadCertificate(certificatePath)
    count += 1

    return {'host' : host, 'ssl_port' : sslPort, 'http_port' : httpPort, 'certificate' : certificate}

def promptForBundleInfo():
    count = 1
    bundle = promptForLogicalInfo()

    if (bundle['region'] == ''): del bundle['region']

    while True:
        host = promptForPhysicalInfo(count)

        if host is not None:
            bundle['hosts'].append(host)
        elif count == 1:
            print('\n' + textwrap.fill('Sorry, you must specify at least one physical host!') + '\n')
            continue
        else:
            break

        count += 1

    return bundle

def writeBundle(bundle, path):
    with open(path, 'w') as bundleFile:
        bundleFile.write(json.dumps(bundle))
    print('\n\nBundle saved in "{}"'.format(path))
