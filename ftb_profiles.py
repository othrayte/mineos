"""A python script to manage minecraft servers
   Designed for use with MineOS: http://minecraft.codeemo.com

   This file handles fetching of the modpack listing from the FTB hosts for creating an FTB profile
"""

__author__ = "Adrian Cowan"
__license__ = "GNU GPL v3.0"
__version__ = "0.6.0"
__email__ = "othrayte@gmail.com"

import xml.etree.ElementTree as ET
import urllib2
import cherrypy
import logging
from collections import OrderedDict

def update_ftb_modpack_info_cache():
    modpackXml = urllib2.urlopen("http://new.creeperrepo.net/FTB2/static/modpacks.xml").read()
    modpackRoot = ET.fromstring(modpackXml)
    for modpack in modpackRoot.iter('modpack'):
        if not 'repoVersion' in modpack.attrib:
            continue
        name = modpack.attrib['name']
        cherrypy.log(name, context='', severity=logging.ERROR, traceback=False)
        FTB_MODPACKS[name] = modpack.attrib
        FTB_PROFILES[name] = {
            'name': name,
            'type': 'archived_jar',
            'url': "http://new.creeperrepo.net/FTB2/modpacks"+"^"+modpack.attrib['dir']+"^"+modpack.attrib['repoVersion']+"^"+modpack.attrib['serverPack'],
            'save_as': modpack.attrib['dir']+"^"+modpack.attrib['serverPack'],
            'run_as': '*.jar',
            'ignore': '',
            'desc': modpack.attrib['description'],
            'version': modpack.attrib['version']
            }

FTB_MODPACKS = {}

FTB_PROFILES = OrderedDict()

update_ftb_modpack_info_cache()
