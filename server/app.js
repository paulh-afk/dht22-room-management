const express = require('express');
const cors = require('cors');
const csv = require('csvtojson');
const path = require('path');
const initializeDatabase = require('./database');
const { getConfig, updateConfig } = require('./config');

const app = express();

app.use(cors());
app.use(express.json());

app.get('/releves', (req, res, next) => {
  const csvFilePath = path.resolve('../releves.csv');

  csv()
    .fromFile(csvFilePath)
    .then((releves) => {
      releves.map((releve, index) => {
        const temperature = Number(releve['temperature']);
        const humidite = Number(releve['humidite']);
        const horodatage = releve['horodatage'];

        if (isNaN(temperature)) {
          throw Error(
            'La température enregistrée à la ligne ' +
              (index + 2).toString() +
              " n'est pas valide!",
          );
        }

        if (isNaN(humidite)) {
          throw Error(
            "L'humidite enregistrée à la ligne " + (index + 2).toString() + " n'est pas valide!",
          );
        }

        if (horodatage.length !== 19 || isNaN(Date.parse(horodatage))) {
          throw Error("L'horodatage n'est pas valide!");
        }
      });

      res.json({ ok: true, releves });
    })
    .catch(({ message }) => {
      res.json({ ok: false, message });
    });
});

app.get('/config', (req, res, next) => {
  getConfig()
    .then((config) => {
      res.json(config);
    })
    .catch(({ message }) => {
      res.json({ ok: false, message });
    });
});

app.post('/updateconfig', (req, res, next) => {
  const body = req.body;
  let bodyKey;
  let bodyValue;

  try {
    if (Object.keys(body).length !== 1) {
      throw Error('Un seul paramètre peut être envoyé');
    }

    bodyKey = Object.keys(body)[0];
    bodyValue = Object.values(body)[0];

    if (bodyKey.split('.').length !== 2) {
      throw Error(`La clé "${bodyKey}" n'a pas le bon format`);
    }
  } catch ({ message }) {
    res.status(400).json({ ok: false, message });
    return;
  }

  const keysIncluded = [
    [
      'settings',
      [
        'id_local',
        'seuil_temperature_min',
        'seuil_temperature_max',
        'seuil_humidite_min',
        'seuil_humidite_max',
        'compteur',
        'interval_secondes',
      ],
    ],
    ['database', ['host', 'port', 'user', 'password', 'database']],
    ['email', ['sender', 'password', 'destinations', 'server_addr', 'server_port']],
  ];

  let check = false;
  const bodyKeySplited = bodyKey.split('.');

  for (let keyIncluded of keysIncluded) {
    const categorie = keyIncluded[0];
    const properties = keyIncluded[1];

    for (let property of properties) {
      if (bodyKeySplited[0] === categorie && bodyKeySplited[1] === property) {
        check = true;
        break;
      }
    }

    if (check) {
      break;
    }
  }

  try {
    if (!check) {
      throw Error('Les données envoyés ne sont pas valide');
    }
  } catch ({ message }) {
    res.status(400).json({ ok: false, message });
    return;
  }

  getConfig()
    .then((config) => {
      const [categ, proper] = bodyKey.split('.');
      config[categ][proper] = bodyValue;

      updateConfig(config);
    })
    .catch(({ message }) => {
      res.json({ ok: false, message });
      return;
    });

  res.status(200).json({ ok: true });
});

app.get('/localname/:id_local', async (req, res, next) => {
  const { id_local } = req.params;

  try {
    if (!id_local) {
      throw Error("Le paramètre contenant l'identifiant est attendu");
    }
  } catch ({ message }) {
    res.json({ ok: false, message });
    return;
  }

  try {
    const { Locals } = await initializeDatabase();

    Locals.findOne({ where: { id: id_local } }).then((local) => {
      if (!local) {
        throw Error("Aucun local portant ce nom n'a été trouvé");
      }

      res.json({ ok: true, local });
    });
  } catch ({ message }) {
    res.json({ ok: false, message });
  }
});

app.listen(4000);
