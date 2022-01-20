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

#### Sample exercise

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

#### Sample inject_flow

```json
  "inject_flow": [
    {
      "description": "Initial inject of an incident email to start the exercise.",
      "inject_uuid": "19272db1-a7c4-4cb3-aa33-df775b8fec8c",
      "reporting_callback": [],
      "requirements": {},
      "sequence": {
        "completion_trigger": [
          "time_expiration",
          "completion"
        ],
        "followed_by": [
          "c104aa37-e394-43ce-b82b-a733d3745468"
        ],
        "trigger": [
          "startex"
        ]
      },
      "timing": {
        "triggered_at": null
      }
    },
    ]
```
### inject_payloads

- `name` is a string in UTF-8, naming the inject payload.
- `parameters` is a JSON object describing the `parameters` of the `type`.
- `type` is a string in UTF-8, describing the `type` as defined in the `type` vocabulary.
- `uuid` is a string in UTF-8, specifying the UUID (version 4) of the inject payload. This value MUST be fixed while referencing the same payload.

#### `type` vocabulary

|Type|Description|
|:---|:----------|
|`file`|A file inject described as a Base64 encoded string via the `content` key, or alternatively the path to a file.|
|`tcp_connection`|A TCP connection described by `parameters` such as `destination`, `port` and `source`.|

#### Sample inject_payloads

```json
  "inject_payloads": [
    {
      "name": "email-incident",
      "parameters": {
        "content": "RnJvbSBjc2lydEB0ZWxjby5sdQoKRGVhciB4eSwKCldlIGhhdmUgaGFkIGEgZmFpbGVkIHNwZWFycGhpc2hpbmcgYXR0ZW1wdCB0YXJnZXRpbmcgb3VyIENFTyByZWNlbnRseSB3aXRoIHRoZSBmb2xsb3dpbmcgZGV0YWlsczoKCk91ciBDRU8gcmVjZWl2ZWQgYW4gRS1tYWlsIG9uIDAzLzAyLzIwMjEgMTU6NTYgY29udGFpbmluZyBhIHBlcnNvbmFsaXNlZCBtZXNzYWdlIGFib3V0IGEgcmVwb3J0IGNhcmQgZm9yIHRoZWlyIGNoaWxkLiBUaGUgYXR0YWNrZXIgcHJldGVuZGVkIHRvIGJlIHdvcmtpbmcgZm9yIHRoZSBzY2hvb2wgb2YgdGhlIENFT+KAmXMgZGF1Z2h0ZXIsIHNlbmRpbmcgdGhlIG1haWwgZnJvbSBhIHNwb29mZWQgYWRkcmVzcyAoam9obi5kb2VAbHV4ZW1ib3VyZy5lZHUpLiBKb2huIERvZSBpcyBhIHRlYWNoZXIgb2YgdGhlIHN0dWRlbnQuIFRoZSBlbWFpbCB3YXMgcmVjZWl2ZWQgZnJvbSB0aHJvd2F3YXktZW1haWwtcHJvdmlkZXIuY29tICgxMzcuMjIxLjEwNi4xMDQpLiAKClRoZSBlLW1haWwgY29udGFpbmVkIGEgbWFsaWNpb3VzIGZpbGUgKGZpbmQgaXQgYXR0YWNoZWQpIHRoYXQgd291bGQgdHJ5IHRvIGRvd25sb2FkIGEgc2Vjb25kYXJ5IHBheWxvYWQgZnJvbSBodHRwczovL2V2aWxwcm92aWRlci5jb20vdGhpcy1pcy1ub3QtbWFsaWNpb3VzLmV4ZSAoYWxzbyBhdHRhY2hlZCwgcmVzb2x2ZXMgdG8gMjYwNzo1MzAwOjYwOmNkNTI6MzA0Yjo3NjBkOmRhNzpkNSkuIEl0IGxvb2tzIGxpa2UgdGhlIHNhbXBsZSBpcyB0cnlpbmcgdG8gZXhwbG9pdCBDVkUtMjAxNS01NDY1LiBBZnRlciBhIGJyaWVmIHRyaWFnZSwgdGhlIHNlY29uZGFyeSBwYXlsb2FkIGhhcyBhIGhhcmRjb2RlZCBDMiBhdCBodHRwczovL2Fub3RoZXIuZXZpbC5wcm92aWRlci5jb206NTc2NjYgKDExOC4yMTcuMTgyLjM2KSB0byB3aGljaCBpdCB0cmkKZXMgdG8gZXhmaWx0cmF0ZSBsb2NhbCBjcmVkZW50aWFscy4gVGhpcyBpcyBob3cgZmFyIHdlIGhhdmUgZ290dGVuIHNvIGZhci4gUGxlYXNlIGJlIG1pbmRmdWwgdGhhdCB0aGlzIGlzIGFuIG9uZ29pbmcgaW52ZXN0aWdhdGlvbiwgd2Ugd291bGQgbGlrZSB0byBhdm9pZCBpbmZvcm1pbmcgdGhlIGF0dGFja2VyIG9mIHRoZSBkZXRlY3Rpb24gYW5kIGtpbmRseSBhc2sgeW91IHRvIG9ubHkgdXNlIHRoZSBjb250YWluZWQgaW5mb3JtYXRpb24gdG8gcHJvdGVjdCB5b3VyIGNvbnN0aXR1ZW50cy4KCkJlc3QgcmVnYXJkcywKCg==",
        "content-type": "base64",
        "filename": "email.eml"
      },
      "type": "file",
      "uuid": "930c6f6b-f89d-456d-a59d-5cb89bdec0b1"
    },
```

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
|`email_to_participants`|Email to participant(s) as defined in the exercise|

#### `target_tool` vocabulary

|Target_tool|Description|
|:----------|:----------|
|`MISP`|MISP Threat Intelligence Platform|
|`Suricata`|Suricata NIDS|

#### Sample injects

```json
"injects": [
 {
      "action": "network_connection",
      "action_payload_resource_uuid": "9b519819-36cc-48b1-8418-43831f2d3a6a",
      "inject_evaluation": [
        {
          "parameters": [
            {
              "source-ip": {
                "comparison": "is",
                "values": [
                  "137.221.106.104"
                ]
              }
            }
          ],
          "result": "alert",
          "score_range": [
            0,
            50
          ]
        }
      ],
      "name": "malicious network flow",
      "target_tool": "Suricata",
      "uuid": "c104aa37-e394-43ce-b82b-a733d3745468"
    },
  ]
```

