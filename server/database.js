const { Sequelize, DataTypes } = require('sequelize');

try {
  const sequelize = new Sequelize('gestionstock', 'Gestionnaire', 'Password123', {
    host: '172.20.10.6',
    dialect: 'mysql',
  });

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

  exports.Locals = Locals;
  exports.RelevesLocals = RelevesLocals;
} catch ({ message }) {
  console.error(message);
}
