const fs = require('fs/promises');
const yaml = require('yaml');

const configFilePath = '../config.yaml';

const getConfig = () => {
  return fs.readFile(configFilePath).then((value) => {
    const content = value.toString();
    return yaml.parse(content);
  });
};

const updateConfig = (config) => {
  fs.writeFile(configFilePath, yaml.stringify(config));
};

exports.getConfig = getConfig;
exports.updateConfig = updateConfig;
