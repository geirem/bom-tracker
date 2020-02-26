## SECURITY NOTES


#### XML Parsing
The action uses [`lib.etree.ElementTree`](https://docs.python.org/3.8/library/xml.etree.elementtree.html#module-xml.etree.ElementTree) to parse the provided BoM.  This parser is vulnerable
to some [XML attacks](https://docs.python.org/3.8/library/xml.html#xml-vulnerabilities), if used improperly.

The BoM (on [CycloneDX format](https://cyclonedx.org/)) is produced by the previous
step in the same job, and can only be used to stage DoS attacks on the running job. So
we consider these vulnerabilities acceptable.
