import time
import copy
from lxml import etree

def append_elements(root, elements):
    for e in elements:
        root.append(copy.deepcopy(e))

write_metadata_record_identifier = False

ms_namespace_uri = "http://w3id.org/meta-share/meta-share/"
xsi_namespace_uri = "http://www.w3.org/2001/XMLSchema-instance"
xml_namespace_uri = "http://www.w3.org/XML/1998/namespace"
ms_prefix = "{%s}" % ms_namespace_uri
xsi_prefix = "{%s}" % xsi_namespace_uri
xsi_schemaLocation_qualified_name = etree.QName(xsi_namespace_uri, "schemaLocation")
xsi_schemaLocation = "http://w3id.org/meta-share/meta-share/ ../../../Schema/ELG-SHARE.xsd"

lang_en = {etree.QName(xml_namespace_uri, 'lang'): 'en'}

namespace_map = {None: ms_namespace_uri,
                 'xsi' : xsi_namespace_uri,
                 'xml': xml_namespace_uri}

def Element(name, text = None, **kwargs):
    if 'attribs' in kwargs:
        retval = etree.Element(name, kwargs['attribs'], nsmap = namespace_map)
    else:
        retval = etree.Element(name, nsmap = namespace_map)
    if text != None:
        retval.text = text
    return retval

def make_language(_id, **kwargs):
    language = Element("language")
    subtags = []
    if 'script' in kwargs:
        subtags.append(kwargs['script'])
        language.append(Element("scriptId", kwargs['script']))
    if 'region' in kwargs:
        subtags.append(kwargs['region'])
        language.append(Element("regionId", kwargs['region']))
    if 'variant' in kwargs:
        subtags.append(kwargs['variant'])
        language.append(Element("variantId", kwargs['variant']))
    tag = '-'.join([_id] + subtags)
    language.append(Element("languageId", _id))
    language.append(Element("languageTag", tag))
    return language

metadata = etree.Element("MetadataRecord",
                         { xsi_schemaLocation_qualified_name: xsi_schemaLocation },
                         nsmap = namespace_map)

if write_metadata_record_identifier:
    metadata.append(etree.Element("MetadataRecordIdentifier",
                                  { etree.QName(ms_namespace_uri, "MetadataRecordIdentifierScheme"): "http://w3id.org/meta-share/meta-share/elg" },
                                  nsmap = {None : ms_namespace_uri}))

creation_date = etree.SubElement(metadata, "metadataCreationDate")
creation_date.text = time.strftime("%Y-%m-%d")

responsible_person = [
    Element("actorType", "Person"),
    Element("surname", "Hardwick", attribs = lang_en),
    Element("givenName", "Sam", attribs = lang_en),
    Element("email", "sam.hardwick@iki.fi")
    ]

creator = etree.SubElement(metadata, "metadataCreator")
append_elements(creator, responsible_person)
curator = etree.SubElement(metadata, "metadataCurator")
append_elements(curator, responsible_person)

metadata.append(Element("compliesWith", "http://w3id.org/meta-share/meta-share/ELG-SHARE"))

described_entity = etree.SubElement(metadata, "DescribedEntity", nsmap = namespace_map)
language_resource = etree.SubElement(described_entity, "LanguageResource", nsmap = namespace_map)
language_resource.append(Element("resourceName", "OPUS-MT: Open neural machine translation", attribs = lang_en))
language_resource.append(Element("resourceShortName", "OPUS-MT", attribs = lang_en))
language_resource.append(Element("description", "Multilingual machine translation using neural networks.", attribs = lang_en))
language_resource.append(Element("version", "v1.0.0"))
additional_info = etree.SubElement(language_resource, "additionalInfo", nsmap = namespace_map)
additional_info.append(Element("landingPage", "https://github.com/Helsinki-NLP/Opus-MT"))
language_resource.append(Element("keyword", "machine translation", attribs = lang_en))
language_resource.append(Element("keyword", "translation", attribs = lang_en))
language_resource.append(Element("keyword", "multilingual", attribs = lang_en))

lr_subclass = etree.SubElement(language_resource, "LRSubclass", nsmap = namespace_map)
tool_service = etree.SubElement(lr_subclass, "ToolService", nsmap = namespace_map)
function = etree.SubElement(tool_service, "function", nsmap = namespace_map)
function.append(Element("LTClassRecommended", "http://w3id.org/meta-share/omtd-share/MachineTranslation"))
software_distribution = etree.SubElement(tool_service, "SoftwareDistribution", nsmap = namespace_map)
software_distribution.append(Element("SoftwareDistributionForm", "http://w3id.org/meta-share/meta-share/dockerImage"))
software_distribution.append(Element("dockerDownloadLocation", "MISSING"))
software_distribution.append(Element("executionLocation", "MISSING, Add here the REST endpoint at which the LT tool is exposed within the Docker image."))

licence_terms = etree.SubElement(software_distribution, "licenceTerms", nsmap = namespace_map)
licence_terms.append(Element("licenceTermsName", "MIT License", attribs = lang_en))
licence_terms.append(Element("licenceTermsURL", "https://spdx.org/licenses/MIT.html"))
licence_identifier = etree.Element("LicenceIdentifier",
                                   { etree.QName(ms_namespace_uri, "LicenceIdentifierScheme"): "http://w3id.org/meta-share/meta-share/SPDX" },
                                   nsmap = {'ms': ms_namespace_uri})
licence_identifier.text = "MIT"
licence_terms.append(licence_identifier)

tool_service.append(Element("languageDependent", "true"))

input_content_resource = etree.SubElement(tool_service, "inputContentResource")
input_content_resource.append(Element("processingResourceType", "http://w3id.org/meta-share/meta-share/userInputText"))
input_content_resource.append(make_language("fi", region = "FI"))
input_content_resource.append(make_language("sv", region = "FI"))
input_content_resource.append(make_language("sv", region = "SE"))
input_content_resource.append(Element("mediaType", "http://w3id.org/meta-share/meta-share/text"))
input_content_resource.append(Element("characterEncoding", "http://w3id.org/meta-share/meta-share/UTF-8"))

output_content_resource = etree.SubElement(tool_service, "outputContentResource")
output_content_resource.append(Element("processingResourceType", "http://w3id.org/meta-share/meta-share/userOutputText"))
output_content_resource.append(make_language("fi", region = "FI"))
output_content_resource.append(make_language("sv", region = "FI"))
output_content_resource.append(make_language("sv", region = "SE"))
output_content_resource.append(Element("mediaType", "http://w3id.org/meta-share/meta-share/text"))
output_content_resource.append(Element("characterEncoding", "http://w3id.org/meta-share/meta-share/UTF-8"))

tool_service.append(Element("evaluated", "false"))

print(str(etree.tostring(metadata, xml_declaration = True, encoding = 'utf-8', pretty_print = True), encoding = "utf-8"))
