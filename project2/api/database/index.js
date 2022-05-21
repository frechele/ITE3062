const Sequelize = require('sequelize');

const config = {
    host: process.env.HCI_MYSQL_HOST || '127.0.0.1',
    port: 3306,
    database: 'hci',
    user: 'db_admin',
    password: process.env.HCI_MYSQL_PASSWORD || 'p@ssW0rd',
};

const sequelize = new Sequelize(config.database, config.user, config.password, {
    host: config.host,
    dialect: 'mysql',
});

module.exports = {
    sequelize,
    ExperimentResult: require('./experiment-result.model')(sequelize),
};
