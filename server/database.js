const { Sequelize, DataTypes } = require('sequelize');
const { getConfig } = require('./config');

const initializeDatabase = async () => {
  try {
    const config = await getConfig();

    const { host, port, user, password, database } = config.database;

    const sequelize = new Sequelize(database, user, password, {
      host,
      port,
      dialect: 'mysql',
    });

    await sequelize.authenticate();

    const Locals = sequelize.define(
      'locals',
      {
        id: {
          primaryKey: true,
          type: DataTypes.INTEGER,
        },
        nom_local: DataTypes.CHAR,
      },
      { timestamps: false },
    );

    const RelevesLocals = sequelize.define(
      'releves_locals',
      {
        id: {
          primaryKey: true,
          type: DataTypes.INTEGER,
        },
        id_local: DataTypes.INTEGER,
        temperature: DataTypes.DOUBLE,
        humidity: DataTypes.DOUBLE,
        horodatage: DataTypes.TIME,
      },
      { timestamps: false },
    );

    return { Locals, RelevesLocals };
  } catch (error) {
    throw Error('Erreur lors de la connexion à la base de données');
  }
};

module.exports = initializeDatabase;
