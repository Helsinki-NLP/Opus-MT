import sys
import time
import copy
from lxml import etree
import argparse
# import iso639
from iso639 import Lang


argparser = argparse.ArgumentParser('Write ELG metadata and configuration information to local directory')
argparser.add_argument('--source-langs', action="store", required=True)
argparser.add_argument('--source-lang', action="store", required=True)
argparser.add_argument('--target-lang', action="store", required=True)
argparser.add_argument('--supported-source-lang', action="store")
argparser.add_argument('--source-region', action="store")
argparser.add_argument('--target-region', action="store")
argparser.add_argument('--resource-name', action="store", default="OPUS-MT")
argparser.add_argument('--image-name', action="store", required=True)
argparser.add_argument('--models-in-image', action="store", required=True)
argparser.add_argument('--ram-per-model', action="store", default=768)
argparser.add_argument('--version', action="store", default="1.0.0")
args = argparser.parse_args()
langpair = tuple(sorted((args.source_lang, args.target_lang)))

# Probably due to an ELG bug, information about the metadata apparently
# must not be present in the metadata for a tool, as opposed to a project
# or organization
tool_metadata = True

def get_git_user_info():
    '''Guess the maintainer's name and email from your git information'''
    import subprocess
    name = subprocess.Popen(["git", "config", "user.name"], stdout=subprocess.PIPE, encoding='utf-8').communicate()[0].strip()
    last_space = name.rindex(' ')
    firstname = name[:last_space]
    lastname = name[last_space+1:]
    email = subprocess.Popen(["git", "config", "user.email"], stdout=subprocess.PIPE, encoding='utf-8').communicate()[0].strip()
    return (firstname, lastname, email)

try:
    user_info = get_git_user_info()
    responsible_person_surname, responsible_person_given_name, responsible_person_email = user_info
    print(f'* Using your git user info for maintainer info {user_info}', file=sys.stderr)
except:
    responsible_person_surname = "Hardwick"
    responsible_person_given_name = "Sam"
    responsible_person_email = "sam.hardwick@iki.fi"
    print(f"* Couldn't read git user info, using default maintainer information", file=sys.stderr)

version = args.version
resource_name = args.resource_name
image_name = args.image_name
# docker_location = f"https://hub.docker.com/repository/docker/helsinkinlp/{image_name}"
docker_location = f"docker.io/helsinkinlp/{image_name}"
source_langcodes = args.source_langs
source_langcode = args.source_lang
source_region = args.source_region
target_langcode = args.target_lang
target_region = args.target_region
# source_lang = iso639.languages.get(part3=source_langcode)
# target_lang = iso639.languages.get(part3=target_langcode)
# source_langname = source_lang.name
# target_langname = target_lang.name
# source_langcode_short = source_langcode.split('_')[0]
# target_langcode_short = target_langcode.split('_')[0]
source_langname = Lang(source_langcode.split('_')[0]).name
target_langname = Lang(target_langcode.split('_')[0]).name

language_pair = f'{source_langcode}-{target_langcode}'

# add language pair to the resource name if it is different from
# the source and target languages (typically multilingual models)
if language_pair != f'{source_langcodes}-{target_langcode}':
    resource_name = f'{resource_name} ({language_pair})'


def append_elements(root, elements):
    for e in elements:
        root.append(copy.deepcopy(e))

ms_namespace_uri = "http://w3id.org/meta-share/meta-share/"
xsi_namespace_uri = "http://www.w3.org/2001/XMLSchema-instance"
xml_namespace_uri = "http://www.w3.org/XML/1998/namespace"
ms_prefix = "{%s}" % ms_namespace_uri
xsi_prefix = "{%s}" % xsi_namespace_uri
xsi_schemaLocation_qualified_name = etree.QName(xsi_namespace_uri, "schemaLocation")
xsi_schemaLocation = "http://w3id.org/meta-share/meta-share/ ../../../Schema/ELG-SHARE.xsd"

lang_en = {etree.QName(xml_namespace_uri, 'lang'): 'en'}

namespace_map = {'ms': ms_namespace_uri,
                 'xsi' : xsi_namespace_uri,
                 'xml': xml_namespace_uri}

def ms(tag): return ms_prefix + tag

def Element(name, text = None, **kwargs):
    if 'attribs' in kwargs:
        retval = etree.Element(name, kwargs['attribs'], nsmap = namespace_map)
    else:
        retval = etree.Element(name, nsmap = namespace_map)
    if text != None:
        retval.text = text
    return retval

def make_language(_id, **kwargs):
    if Lang(_id.split('_')[0]).pt1:
        _id = Lang(_id.split('_')[0]).pt1
    # if iso639.languages.get(part3=_id).part1:
    #     _id = iso639.languages.get(part3=_id).part1
    language = Element(ms("language"))
    subtags = []
    if 'script' in kwargs:
        subtags.append(kwargs['script'])
        language.append(Element(ms("scriptId"), kwargs['script']))
    if 'region' in kwargs and kwargs['region']:
        subtags.append(kwargs['region'])
        language.append(Element(ms("regionId"), kwargs['region']))
    if 'variant' in kwargs:
        subtags.append(kwargs['variant'])
        language.append(Element(ms("variantId"), kwargs['variant']))
    tag = '-'.join([_id] + subtags)
    language.append(Element(ms("languageTag"), tag))
    language.append(Element(ms("languageId"), _id))
    return language

metadata = etree.Element(ms("MetadataRecord"),
                         { xsi_schemaLocation_qualified_name: xsi_schemaLocation },
                         nsmap=namespace_map)

if not tool_metadata:
    metadata.append(etree.Element(ms("MetadataRecordIdentifier"),
                                  { etree.QName(ms_namespace_uri, "MetadataRecordIdentifierScheme"): "http://w3id.org/meta-share/meta-share/elg" },
                                  nsmap = namespace_map))
    responsible_person = [
    Element(ms("actorType"), "Person"),
    Element(ms("surname"), responsible_person_surname, attribs = lang_en),
    Element(ms("givenName"), responsible_person_given_name, attribs = lang_en),
    Element(ms("email"), responsible_person_email)
    ]

    creator = etree.SubElement(metadata, ms("metadataCreator"))
    append_elements(creator, responsible_person)
    curator = etree.SubElement(metadata, ms("metadataCurator"))
    append_elements(curator, responsible_person)
    
    metadata.append(Element(ms("compliesWith"), "http://w3id.org/meta-share/meta-share/ELG-SHARE"))

creation_date = etree.SubElement(metadata, ms("metadataCreationDate"))
creation_date.text = time.strftime("%Y-%m-%d")

described_entity = etree.SubElement(metadata, ms("DescribedEntity"), nsmap = namespace_map)
language_resource = etree.SubElement(described_entity, ms("LanguageResource"), nsmap = namespace_map)
language_resource.append(Element(ms("entityType"), "LanguageResource"))
language_resource.append(Element(ms("resourceName"), f"HelsinkiNLP - {resource_name}: {source_langname}-{target_langname} machine translation", attribs = lang_en, nsmap=namespace_map))
language_resource.append(Element(ms("resourceShortName"), f"{resource_name} {source_langcode}-{target_langcode}", attribs = lang_en))
language_resource.append(Element(ms("description"), "Multilingual machine translation using neural networks.", attribs = lang_en))
language_resource.append(Element(ms("logo"), "https://github.com/Helsinki-NLP/Opus-MT/raw/master/img/opus_mt.png"))

language_resource.append(Element(ms("version"), version))
additional_info = etree.SubElement(language_resource, ms("additionalInfo"), nsmap = namespace_map)
additional_info.append(Element(ms("landingPage"), "https://github.com/Helsinki-NLP/Opus-MT"))
language_resource.append(Element(ms("keyword"), "machine translation", attribs = lang_en))
language_resource.append(Element(ms("keyword"), "translation", attribs = lang_en))
language_resource.append(Element(ms("keyword"), "multilingual", attribs = lang_en))

resource_provider = etree.SubElement(language_resource, ms("resourceProvider"), nsmap = namespace_map)
resource_provider_organization = etree.SubElement(resource_provider, ms("Organization"), nsmap = namespace_map)
resource_provider_organization.append(Element(ms("actorType"), "Organization", nsmap=namespace_map))
resource_provider_organization.append(Element(ms("organizationName"), "University of Helsinki", attribs = lang_en, nsmap=namespace_map))
resource_provider_organization.append(Element(ms("website"), "http://www.helsinki.fi", nsmap=namespace_map))

resource_creator = etree.SubElement(language_resource, ms("resourceCreator"), nsmap = namespace_map)
resource_creator_organization = etree.SubElement(resource_creator, ms("Organization"), nsmap = namespace_map)
resource_creator_organization.append(Element(ms("actorType"), "Organization", nsmap=namespace_map))
resource_creator_organization.append(Element(ms("organizationName"), "Opus-MT Team", attribs = lang_en, nsmap=namespace_map))
resource_creator_organization.append(Element(ms("website"), "https://github.com/Helsinki-NLP/Opus-MT", nsmap=namespace_map))

funding_project = etree.SubElement(language_resource, ms("fundingProject"), nsmap = namespace_map)
funding_project.append(Element(ms("projectName"), "Open Translation Models, Tools and Services", attribs = lang_en, nsmap=namespace_map))
project_identifier = etree.Element(ms("ProjectIdentifier"),
                                   { etree.QName(ms_namespace_uri, "ProjectIdentifierScheme"): "http://w3id.org/meta-share/meta-share/other" },
                                   nsmap = {'ms': ms_namespace_uri})
project_identifier.text = "Opus-MT"
funding_project.append(project_identifier)
funding_project.append(Element(ms("website"), "https://github.com/Helsinki-NLP/Opus-MT", nsmap=namespace_map))

intended_application = etree.SubElement(language_resource, ms("intendedApplication"), nsmap=namespace_map)
intended_application.append(Element(ms("LTClassRecommended"), "http://w3id.org/meta-share/omtd-share/MachineTranslation"))

lr_subclass = etree.SubElement(language_resource, ms("LRSubclass"), nsmap = namespace_map)
tool_service = etree.SubElement(lr_subclass, ms("ToolService"), nsmap = namespace_map)
tool_service.append(Element(ms("lrType"), "ToolService"))
function = etree.SubElement(tool_service, ms("function"), nsmap = namespace_map)
function.append(Element(ms("LTClassRecommended"), "http://w3id.org/meta-share/omtd-share/MachineTranslation"))
software_distribution = etree.SubElement(tool_service, ms("SoftwareDistribution"), nsmap = namespace_map)
software_distribution.append(Element(ms("SoftwareDistributionForm"), "http://w3id.org/meta-share/meta-share/dockerImage"))
software_distribution.append(Element(ms("executionLocation"), f"http://localhost:8888/elg/translate/{source_langcode}/{target_langcode}"))
software_distribution.append(Element(ms("dockerDownloadLocation"), docker_location))
software_distribution.append(Element(ms("privateResource"), "false"))
software_distribution.append(Element(ms("additionalHWRequirements"), f"limits_memory: {str(int(args.models_in_image)*args.ram_per_model)}Mi"))

licence_terms = etree.SubElement(software_distribution, ms("licenceTerms"), nsmap = namespace_map)
# licence_terms.append(Element(ms("licenceTermsName"), "MIT License", attribs = lang_en))
# licence_terms.append(Element(ms("licenceTermsURL"), "https://spdx.org/licenses/MIT.html"))
licence_terms.append(Element(ms("licenceTermsName"), "CC BY 4.0", attribs = lang_en))
licence_terms.append(Element(ms("licenceTermsURL"), "https://creativecommons.org/licenses/by/4.0/"))
licence_terms.append(Element(ms("conditionOfUse"), "http://w3id.org/meta-share/meta-share/other"))
licence_identifier = etree.Element(ms("LicenceIdentifier"),
                                   { etree.QName(ms_namespace_uri, "LicenceIdentifierScheme"): "http://w3id.org/meta-share/meta-share/SPDX" },
                                   nsmap = {'ms': ms_namespace_uri})
licence_identifier.text = "CC-BY-4.0"
licence_terms.append(licence_identifier)

tool_service.append(Element(ms("languageDependent"), "true"))

input_content_resource = etree.SubElement(tool_service, ms("inputContentResource"))
input_content_resource.append(Element(ms("processingResourceType"), "http://w3id.org/meta-share/meta-share/userInputText"))
for s in source_langcodes.split('+'):
    try:
        input_content_resource.append(make_language(s, region = source_region))
    except:
        print("could not add language " + s)
input_content_resource.append(Element(ms("mediaType"), "http://w3id.org/meta-share/meta-share/text"))
input_content_resource.append(Element(ms("characterEncoding"), "http://w3id.org/meta-share/meta-share/UTF-8"))

output_content_resource = etree.SubElement(tool_service, ms("outputResource"))
output_content_resource.append(Element(ms("processingResourceType"), "http://w3id.org/meta-share/meta-share/outputText"))
output_content_resource.append(make_language(target_langcode, region = target_region))
output_content_resource.append(Element(ms("mediaType"), "http://w3id.org/meta-share/meta-share/text"))
output_content_resource.append(Element(ms("characterEncoding"), "http://w3id.org/meta-share/meta-share/UTF-8"))
tool_service.append(Element(ms("trl"), "http://w3id.org/meta-share/meta-share/trl5"))
tool_service.append(Element(ms("evaluated"), "false"))

with open(f"OPUS-MT-{source_langcode}-{target_langcode}.xml", "w") as xml_fobj:
    xml_fobj.write(str(etree.tostring(metadata, xml_declaration = False, doctype='<?xml version="1.0" encoding="UTF-8"?>', encoding = 'utf-8', pretty_print = True), encoding = "utf-8"))
