# Common Exercise Format (CEXF)

Common Exercise Format is a proposed format to describe cyber exercise including the exercise metadata, inject flow, the inject and the associated validations/scoring.

# Why structuring exercises in a common format such as CEXF?

- To ensure that an exercise contains all the required elements;
- To validate exercise definitions, in particular potential issues such as the missing or incorrect elements;
- To automate the planning and injects;
- To trace the evolution of an exercise (via diff ang git);
- To allow external contributions by using a common format;

# CEXF Format description

- [Common Exercise Format (CEXF) - format description](https://github.com/MISP/cexf/blob/main/format-description.md)

# CEXF Platform

- An [open source platform](https://github.com/MISP/cexf/tree/main/platform) to run exercises in CEXF format.

# How to contribute and create an exercise

- Create a new git repository with the JSON CEXF.
- Create JSON file(s) to describe your exercise(s). You can have a look at [Common Exercise Format (CEXF) - format description](https://github.com/MISP/cexf/blob/main/format-description.md) or the [sample directory](https://github.com/MISP/cexf/tree/main/samples) for examples.
- Propose a pull-request to have your exercise listed on this repository.

## Common Exercise format - Sample


```json
{
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
    {
      "description": "Inject related to network acticity.",
      "inject_uuid": "c104aa37-e394-43ce-b82b-a733d3745468",
      "reporting_callback": [],
      "requirements": {
        "inject_uuid": "19272db1-a7c4-4cb3-aa33-df775b8fec8c",
        "resolution_requirement": "Publishing"
      },
      "sequence": {
        "completion_trigger": [
          "time_expiration",
          "completion"
        ],
        "trigger": "inject-resolution"
      },
      "timing": {
        "triggered_at": null
      }
    }
  ],
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
    {
      "name": "inject-network-connectivity",
      "parameters": {
        "destination": "player_network_mail_server",
        "port": "25",
        "source": "137.221.106.104"
      },
      "type": "tcp_connection",
      "uuid": "9b519819-36cc-48b1-8418-43831f2d3a6a"
    }
  ],
  "injects": [
    {
      "action": "email_to_participants",
      "action_payload_resource_uuid": "930c6f6b-f89d-456d-a59d-5cb89bdec0b1",
      "inject_evaluation": [
        {
          "parameters": [
            {
              "Event.info": {
                "comparison": "contains",
                "values": [
                  "phishing",
                  "CEO"
                ]
              }
            }
          ],
          "result": "MISP event creation",
          "score_range": [
            0,
            10
          ]
        },
        {
          "parameters": [
            {
              "Event.attribute": {
                "comparison": "equals",
                "values": [
                  {
                    "type": [
                      "email-src",
                      "email"
                    ],
                    "value": "john.doe@luxembourg.edu"
                  },
                  {
                    "type": "domain",
                    "value": "throwaway-email-provider.com"
                  },
                  {
                    "type": [
                      "ip-src",
                      "ip-dst"
                    ],
                    "value": "137.221.106.104"
                  },
                  {
                    "type": [
                      "vulnerability"
                    ],
                    "value": "CVE-2015-5465"
                  }
                ]
              }
            }
          ],
          "result": "MISP attribute capture",
          "score_range": [
            0,
            40
          ]
        },
        {
          "parameters": [
            {
              "Event.Object": {
                "comparison": "count",
                "values": [
                  ">3"
                ]
              }
            }
          ],
          "result": "MISP object use",
          "score_range": [
            0,
            30
          ]
        },
        {
          "parameters": {
            "OR": [
              {
                "Event.EventTag.Tag.{n}.Tag.name": {
                  "comparison": "contains",
                  "values": [
                    "T1566"
                  ]
                }
              },
              {
                "Event.Attribute.{n}.AttributeTag.{n}.Tag.name": {
                  "comparison": "contains",
                  "values": [
                    "T1566"
                  ]
                }
              }
            ]
          },
          "result": "Mitre ATT&CK use",
          "score_range": [
            0,
            10
          ]
        },
        {
          "parameters": [
            {
              "Event.published": {
                "comparison": "is",
                "values": [
                  1
                ]
              }
            }
          ],
          "result": "Publishing",
          "score_range": [
            0,
            10
          ]
        }
      ],
      "name": "received e-mail from csirt@telco.lu",
      "target_tool": "MISP",
      "uuid": "19272db1-a7c4-4cb3-aa33-df775b8fec8c"
    },
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
    }
  ]
}
```
# License

~~~~
 Copyright (c) 2021-2022 Alexandre Dulaunoy - a@foo.be
 Copyright (c) 2021-2022 CIRCL - Computer Incident Response Center Luxembourg
 Copyright (c) 2021-2022 Andras Iklody
 Copyright (c) 2021-2022 Koen Van Impe

 Redistribution and use in source and binary forms, with or without modification,
 are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
 OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 OF THE POSSIBILITY OF SUCH DAMAGE.
~~~~

# Sponsors

The project is supported by

- ["Connecting Europe Facility – Cybersecurity Digital Service Infrastructure Maintenance and Evolution of Core Service Platform Cooperation Mechanism for CSIRTs – MeliCERTes Facility” (SMART 2018/1024)"](https://digital-strategy.ec.europa.eu/en/news/open-platforms-collaborate-cyber-threats) which is an open platforms to collaborate on cyber threats.
- MISP Project
- CIRCL - Computer Incident Response Center Luxembourg
