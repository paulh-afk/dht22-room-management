const express = require('express');
const cors = require('cors');
const path = require('path');
const csv = require('csvtojson');
const app = express();

app.use(cors());

const CSV_FILE_PATH = path.join(__dirname, 'csv_file.csv');

app.get('/releves', async (req, res, next) => {
  await csv()
    .fromFile(CSV_FILE_PATH)
    .then((releves) => {
      try {
        releves.map((releve, index) => {
          const temperature = Number(releve['temperature']);
          const humidite = Number(releve['humidite']);
          const horodatage = releve['horodatage'];

          // TODO
          // |!| a filtrer niveau du script Python

          // temperature, humidite -> type check
          if (isNaN(temperature)) {
            throw new Error(
              'La température enregistrée à la ligne ' +
                (index + 2).toString() +
                " n'est pas valide!",
            );
          }

          if (isNaN(humidite)) {
            throw new Error(
              "L'humidite enregistrée à la ligne " + (index + 2).toString() + " n'est pas valide!",
            );
          }

          if (horodatage.length !== 19 || isNaN(Date.parse(horodatage))) {
            throw new Error("L'horodatage n'est pas valide!");
          }
        });
      } catch ({ message }) {
        res.json({ status: 'KO', message });
      }

      res.json({ status: 'OK', releves });
    })
    .catch(({ message }) => {
      res.json({ status: 'KO', message });
    });
});

app.listen(4000);
