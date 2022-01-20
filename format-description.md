# Common Exercise Format (CEXF) - format description 

This document describes the Common Exercise Format (CEXF), used to describe and automate cyber exercises.

The JSON format includes the overall structure, along with the semantics associated with each respective key.

The purpose of the format's description is the support of other implementations reusing it and ensuring interoperability with existing tools implementing the Common Exercise Format.

## Authors

- Alexandre Dulaunoy, Computer Incident Response Center Luxembourg
- Andras Iklody, Computer Incident Response Center Luxembourg

## Overal structure of the JSON file

The CEXF format is expressed via the JSON format (RFC8259). An exercise is composed
of a single JSON object, with the CEXF format being composed of four required keys:

- `exercise` is a JSON object containing all the meta-data related to the exercise.
- `inject_flow` is a JSON array containing the flow of the injects to be performed during the execution of the exercise.
- `inject_payloads` is a JSON array containing the payloads which can be used in each individual inject.
- `injects` is a JSON array containing the injects' descriptions referenced via the `inject_flow` key.

### exercise

- `description` is a string in UTF-8, meant as a short description of the exercise.
- `expanded` is a string in UTF-8 describing the exercise in more detail.
- `meta` is a JSON array containing a list of non-standardised meta-data, using key-value pairs, to further describe the exercise. The format used is similar to the meta format described in the [MISP galaxy format](https://www.misp-standard.org/rfc/misp-standard-galaxy-format.html#name-meta). 
- `name` is a string in UTF-8, naming the exercise given exercise.
- `namespace` is a string in UTF-8, categorising the exercise.
- `tags` is a JSON array containing the tags associated with the exercise. The tags format is the triple tag format used in [MISP taxonomies](https://www.misp-standard.org/rfc/misp-standard-taxonomy-format.html).
- `total_duration` is a string in UTF-8, expressing the total duration of the exercise in seconds
- `uuid` is a string in UTF-8, specifying the UUID (version 4) of the exercise. This value MUST be fixed while referencing the same exercise.
- `valid_until` is an optional string in UTF-8, describing the validity of an exercise.
- `version` is a string in UTF-8, expressed using a positive monotonic value, to specify the version number of this exercise.

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

- `description` is a string in UTF-8, meant as a short description for the given flow step of the exercise.
- `inject_uuid` is a string in UTF-8, referencing the UUID (version 4) of the inject to be used for the given step.
- `reporting_callback` is an OPTIONAL JSON array containg a callback to be executed upon completion of the inject.
- `requirements` is an optional JSON object containing two fields: `inject_uuid` and `resolution_requirement`, describig both the UUID (version 4) and the resolution requirement of previous inject flow elements, upon whose completion the execution of the given inject flow step depends.
- `sequence` is an optional JSON object containing the sequence definition, such as the `completion_trigger`, `followed_by` and `trigger`. `followed_by` describes the next inject to be executed after the given flow step. `Trigger` is a set of `trigger` from the `trigger` vocabulary.
- `timing` is an optional JSON object, containing the timing definition as of when the execution of given step is to be triggered. `triggered_at` is expressed at in seconds, indicating when the given step will be executed.

#### `trigger` vocabulary

|Trigger|Description|
|:------|:----------|
|`startex`|Special trigger to define the beginning of an exercise|

### inject_payloads

- `name` is a string in UTF-8, naming the inject payload.
- `parameters` is a JSON object describing the `parameters` of the `type.
- `type` is a string in UTF-8, describing the `type` as defined in the `type` vocabulary.
- `uuid` is a string in UTF-8, specifying the UUID (version 4) of the inject payload. This value MUST be fixed while referencing the same payload.

#### `type` vocabulary

|Type|Description|
|:---|:----------|
|`file`|A file inject described as a Base64 string in `content` or a file location.|
|`tcp_connection`|A TCP connection described with `parameters` such as `destination`, `port` and `source`.|

### injects

- `action` is a string in UTF-8, describing the `action` as defined in the `action` vocabulary.
- `action_payload_resource_uuid` is a a string in UTF-8, specifying the UUID (version 4) of the inject payload to use.
- `inject_evaluation` is a JSON object describing the `inject_evaluation` for the specify `target_tool`. This evaluation is a JSON object depending of the `target_tool` parameters to check.
- `name` is a string in UTF-8, naming the inject.
- `target_tool` is a string in UTF-8, describing the `target_tool` as defined in the `target_tool` vocabulary.
- `uuid` is a string in UTF-8, specifying the UUID (version 4) of the inject. This value MUST be fixed while referencing the same inject.

#### `action` vocabulary

|Action|Description|
|:-----|:----------|
|`network_connection`|Create a network connection|
|`email_to_participants`|Email to participant defined in the exercise|

#### `target_tool` vocabulary

|Target_tool|Description|
|:----------|:----------|
|`MISP`|MISP Threat Intelligence Platform|
|`Suricata`|Suricata NIDS|
