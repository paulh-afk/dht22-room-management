const express = require('express');
const cors = require('cors');
const csv = require('csvtojson');
const path = require('path');
const { Locals, RelevesLocals } = require('./database');

const app = express();

app.use(cors());

const CSV_FILE_PATH = path.resolve('../releves.csv');

app.get('/releves', async (req, res, next) => {
  await csv()
    .fromFile(CSV_FILE_PATH)
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

      res.json({ status: 'OK', releves });
    })
    .catch(({ message }) => {
      res.json({ status: 'KO', message });
    });
});

app.get('/localname/:nom_local', (req, res, next) => {
  const { nom_local } = req.params;

  try {
    if (!nom_local) {
      throw Error('Le paramètre contenant le nom du local est attendu!');
    }
  } catch ({ message }) {
    res.json({ status: 'KO', message });
  }

  Locals.findOne({ where: { nom_local } })
    .then((local) => {
      if (!local) {
        throw Error("Aucun local pourtant ce nom n'a été trouvé!");
      }

      res.json({ status: 'OK', local });
    })
    .catch(({ message }) => res.json({ status: 'KO', message }));
});

app.listen(4000);
