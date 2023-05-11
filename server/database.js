const { Sequelize, DataTypes } = require('sequelize');

const sequelize = new Sequelize('gestionstock', 'Gestionnaire', 'Password123', {
  host: '172.16.40.16',
  dialect: 'mysql',
});

const Locals = sequelize.define(
  'locals',
  { id: DataTypes.INTEGER, nom_local: DataTypes.CHAR },
  { timestamps: false },
);

const RelevesLocals = sequelize.define(
  'releves_locals',
  {
    id: DataTypes.INTEGER,
    id_local: DataTypes.INTEGER,
    temperature: DataTypes.DOUBLE,
    humidity: DataTypes.DOUBLE,
    horodatage: DataTypes.TIME,
  },
  { timestamps: false },
);

exports.Locals = Locals;
exports.RelevesLocals = RelevesLocals;
