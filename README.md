# OWASP Dependency Track Integration
## Usage

A BoM integration for [OWASP Dependency Track](https://dependencytrack.org/).  It
* produces a pom from 

### Example workflow for Python projects

```yaml
jobs:
  dependencies:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v1
      with:
        python-version: 3.8
    - name: Create BoM Python
      run: |
        pip install cyclonedx-bom
        cyclonedx-py
    - uses: geirem/bom-tracker@master
      env:
        TRACK_TOKEN: ${{ secrets.TRACK_TOKEN }}
        TRACK_INFO_PAGE: https://github.com/geirem/econokindle/security/advisories
        TRACK_HOST: https://track.example.net
```

### Example workflow for Java projects
Details TBD.  You need to run
```
mvn org.cyclonedx:cyclonedx-maven-plugin:1.6.4:makeAggregateBom
```
to create a BoM.  The rest is similar to Python.

## Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `bom.xml` (file)  | A BoM file on [CycloneDX](https://cyclonedx.org/) format.  Versions 1.0 and 1.1 are currently supported.   |
| `pom.xml` _(file, optional)_  | A Maven POM, to supply project coordinates.  If not present, the repo and build info is used.   |
| `TRACK_TOKEN` (env)  | Configured as a GitHub secret, the access token to Dependency Track.   |
| `TRACK_HOST` (env)  | The host name of your instance of Dependency Track.   |
| `TRACK_INFO_PAGE` _(env, optional)_  | A page to link to when breaking the build due to critical vulnerabilities.    |

## Outputs
Successful builds produce no output, but create a project, or update its BoM, in
Dependency Track.
