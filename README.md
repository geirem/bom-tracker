# OWASP Dependency Track Integration
## Usage

TODO

### Example workflow

```yaml
name: Application Build
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
#    - name: Create BoM Maven
#      run: |
#        mvn org.cyclonedx:cyclonedx-maven-plugin:1.6.4:makeAggregateBom
    - name: Create BoM Python
      run: |
        pip install cyclonedx-bom
        cyclonedx-py
    - uses: geirem/bom-tracker@master
      env:
        TRACK_TOKEN: ${{ secrets.TRACK_TOKEN }}
```

_The rest of this README is from the template.  TODO: fix this :)_


### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myInput`  | An example mandatory input    |
| `anotherInput` _(optional)_  | An example optional input    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myOutput`  | An example output (returns 'Hello world')    |

## Examples

> NOTE: People ❤️ cut and paste examples. Be generous with them!

### Using the optional input

This is how to use the optional input.

```yaml
with:
  myInput: world
  anotherInput: optional
```

### Using outputs

Show people how to use your outputs in another action.

```yaml
steps:
- uses: actions/checkout@master
- name: Run action
  id: create_bom
  uses:  geirem/bom-tracker@master

  # Put an example of your mandatory arguments here
  with:
    myInput: world

# Put an example of using your outputs here
- name: Check outputs
    run: |
    echo "Outputs - ${{ steps.myaction.outputs.myOutput }}"
```
