# Llaor api

This api aims to handle data of a cultural collecting project.
For the moment it's just composed by a dictionary.
To enter data to dictionary we use django admin with the `Definition` model.
A `Definition` is a definition of a `Meaning` for a certain `Word`.
The application treats that definitions to output `Word`s with their `Meaning`s.
Definition has more info than the output (collected in the input process) to be used on the future.

## Setup

### Local server

```bash
docker-compose up -d
```

### Tests

```bash
docker-compose run api pytest
docker-compose run api python manage.py test
```

## Documentation

### Words

#### `GET /words`

_Response:_
```json
[
    {
        "word": "abarset",
        "meanings": [
            {
                "scientific": "rhododendron ferrugineum",
                "type": "m",
                "description": "família de les ericàcies. Arbust d'alta muntanya, molt sensible a les glaçades",
                "extra_info": "",
                "synonym_words": [
                    "bardenal",
                    "neret"
                ],
                "related_words": [ ]
            },
            {
                "scientific": "rhododendron ferrugineum",
                "type": "",
                "description": "gabet, planta de flor vermella que es fa a la muntanya",
                "extra_info": "",
                "synonym_words": [
                    "bardenal",
                    "neret"
                ],
                "related_words": [ ]
            }
        ]
    },
    {
        "word": "abat",
        "meanings": [
            {
                "scientific": "",
                "type": "",
                "description": "païdor del porc, farcit amb carns de botifarra",
                "extra_info": "",
                "synonym_words": [
                    "bisbe",
                    "bisbot"
                ],
                "related_words": [ ]
            }
        ]
    },
]
```

#### `GET /words/<word>`

_Response:_
```json
{
    "word": "abarset",
    "meanings": [
        {
            "scientific": "rhododendron ferrugineum",
            "type": "m",
            "description": "família de les ericàcies. Arbust d'alta muntanya, molt sensible a les glaçades",
            "extra_info": "",
            "synonym_words": [
                "bardenal",
                "neret"
            ],
            "related_words": [ ]
        },
        {
            "scientific": "rhododendron ferrugineum",
            "type": "",
            "description": "gabet, planta de flor vermella que es fa a la muntanya",
            "extra_info": "",
            "synonym_words": [
                "bardenal",
                "neret"
            ],
            "related_words": [ ]
        }
    ]
}
```