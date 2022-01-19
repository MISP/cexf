# Common Exercise Format (CEXF) - format description 

This document describes the Common Exercise Format (CEXF) used to describe cyber exercises.

The JSON format includes the overall structure along with the semantic associated for each respective key.

The format is described to support other implementations which reuse the format and ensuring an interoperability with existing Common Exercise Format.

## Overal structure of the JSON file

The CEXF format is in the JSON format (RFC8259). An exercise is composed
of a single JSON object. The CEXF format is composed of four required keys:

- `exercise` is a JSON object containing all the meta-data related to the exercise.
- `inject_flow` is a JSON array containing the flow of the injects to perform for conducting the exercise.
- `inject_payloads` is a JSON array containing the payloads which can used in each inject.
- `injects` is a JSON array containing the injects description referenced in the `inject_flow`.

### exercise

- `description` is a string in UTF-8 describing the exercise.
- `expanded` is a string in UTF-8 descring the exercise in a more detailed way.
- `meta` is a JSON array containing the non-standard meta-data associated in key value pairs to the exercise. The format used is similar to the meta described in [MISP galaxy format](https://www.misp-standard.org/rfc/misp-standard-galaxy-format.html#name-meta). 
- `name` is a string in UTF-8 naming the exercise.  
- `namespace` is a string in UTF-8 to categorize the exercise.
- `tags` is a JSON array containing the tags associated to the exercise. The tags format is the triple tag format used in [MISP taxonomies](https://www.misp-standard.org/rfc/misp-standard-taxonomy-format.html).
- `total_duration` is a string in UTF-8 expressing the total duration of the exercise in seconds
- `uuid` is a string in UTF-8 specifying the UUID version 4 of the exercise. This value MUST be fixed while referencing the same exercise.
- `valid_until` is an optional string in UTF-8 which describe the validity of an exercise.
- `version` is a string in UTF-8 expressed in a positive monotonic value to specify the version number of this exercise.

```json
  "exercise": {
    "description": "Simple Spear Phishing e-mail example, mimicing a fraud case",
    "expanded": "# Simple Spear Phishing e-mail example, mimicing a fraud case",
    "meta": {
      "author": "MISP Project",
      "level": "beginner"
    },
    "name": "Phishing e-mail",
    "namespace": "phishing",
    "tags": [
      "exercise:software-scope=\"misp\"",
      "state:production"
    ],
    "total_duration": "7200",
    "uuid": "75d7460-af9d-4098-8ad1-754457076b32",
    "valid_until": "20310611",
    "version": "20210611"
  },
```

### inject_flow

### inject_payloads

### injects

