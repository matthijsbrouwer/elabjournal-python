## Python package eLABJournal

Source Python package [elabjournal](https://pypi.org/project/elabjournal/)

Install with

```bash
pip install --upgrade elabjournal
```

See [jupyter notebooks](https://github.com/matthijsbrouwer/jupyter-elabjournal) for
a demonstration of functionality.

## Obtaining a REST API key

The first time an elabjournal object is created from your system, a REST API key has to be entered.

To obtain such a personal key

- login into http://www.elabjournal.com
- go to 'Apps & Connections'
- and click the 'Manage authentication' link

Enter a description (for example 'Jupyter') and generate the token. This key can be entered when a REST API key is asked for.

The key is stored by the elabjournal package in your systems keyring, and therefore the next time you create an elabjournal object, providing this key is not necessary. From the eLABJournal website, you can always revoke a REST API key if necessary. 

If you want to remove the key from your systems keyring, use

```python
elabjournal.reset_key()
```

## Example

Basic example, see [jupyter notebooks](https://github.com/matthijsbrouwer/jupyter-elabjournal) for
a better demonstration of functionality.

```python
>>> from elabjournal import elabjournal
>>> eLAB = elabjournal.api()
Welcome Matthijs Brouwer
Package 'elabjournal', version '0.0.16'
Connected to 'wur.elabjournal.com'
Your active group is 'Testgroup Matthijs' (8738)
>>> eLAB
eLABJournal API object - version 0.0.16 - authenticated as Matthijs Brouwer
|
|  Available methods, use help() on this object for more detailed information:
|
|  barcode(barcode)
|    Get object for the provided barcode.
|  create_sample(*args, **kwargs)
|    Create a sample.
|  create_sample_meta(*args, **kwargs)
|    Create the sample meta
|  delete_sample(*args, **kwargs)
|    Delete a sample.
|  delete_sample_meta(*args, **kwargs)
|    Delete the sample meta.
|  experiment(id)
|    Get experiment object with provided id.
|  experiments(*args, **kwargs)
|    Get object to access experiments.
|  group()
|    Get the active group.
|  groups(*args, **kwargs)
|    Get all groups that you have joined.
|  project(id)
|    Get project object with provided id .
|  projects(*args, **kwargs)
|    Get object to access projects.
|  sample(id)
|    Get sample object with provided id or get multiple sample objects with provided id.
|  sample_meta(sample_id, sample_meta_id)
|    Get sample meta object for provided sample_id and sample_meta_id.
|  sample_metas(id)
|    Get object to access sampleMetas for sample with provided id.
|  sample_or_serie(type, sample_id, sample_serie_id)
|    Get sample serie or serie object (based on provided type) with provided sample_id or sample_serie_id.
|  sample_serie(id)
|    Get sample serie object with provided id.
|  sample_series(*args, **kwargs)
|    Get object to access sample series.
|  sample_type(id)
|    Get sample type object for provided sample_type_id or sample object.
|  sample_type_meta(sample_type_id, sample_type_meta_id)
|    Get sample type meta object with provided sample_type_id and sample_type_meta_id.
|  sample_type_metas(id)
|    Get object to access sampleTypeMetas for sample with provided id.
|  sample_types(*args, **kwargs)
|    Get object to access sample types.
|  samples(*args, **kwargs)
|    Get object to access samples.
|  samples_and_series(*args, **kwargs)
|    Get object to access samples and series in aggregated list.
|  section(section_id)
|    Get section object with provided id.
|  set_group(id)
|    Set the active group to the provided id.
|  storage(id, **kwargs)
|    Get storage object with provided id.
|  storage_layer(id, **kwargs)
|    Get storage layer object with provided id.
|  storage_layers(*args, **kwargs)
|    Get object to access storageLayers.
|  storage_type(id)
|    Get storage type object with provided id.
|  storage_types(*args, **kwargs)
|    Get object to access storageTypes.
|  storages(*args, **kwargs)
|    Get object to access storages.
|  studies(*args, **kwargs)
|    Get object to access studies.
|  study(id, **kwargs)
|    Get study object with provided id.
|  update_sample(id, *args, **kwargs)
|    Update the sample with the provided id.
|  update_sample_meta(*args, **kwargs)
|    Update the sample meta.
|  user()
|    Get the current user.
|  version()
|    Get the version of the package.
|  visualize()
|    Show visualization.

>>> experiments = eLAB.experiments(sort="experimentID")
>>> experiments.all(fields=["name","studyID","projectID"])
                        name  studyID  projectID
experimentID                                    
373184        Testexperiment    74113      22534
389036            labjournal    74113      22534
417242               Arduino    74113      22534
>>> 
```
