const express = require('express');
const bodyParser = require('body-parser');
const { sequelize } = require('./database');
const experimentResultController = require('./controller/experiment-result.controller');

async function launchServer() {
    const app = express();
    app.use(bodyParser.json());

    app.get('/', (req, res) => {
        res.json({ message: 'HCI project2 api server' });
    });

    app.get('/experiment-result', experimentResultController.getAll);
    app.post('/experiment-result', experimentResultController.insertOrUpdate);

    try {
        await sequelize.sync();
        console.log('Database is ready');
    } catch (error) {
        console.log('Unable to connect to the database:');
        console.log(error);
        process.exit(1);
    }

    const port = process.env.PORT || 8080;
    app.listen(port, () => {
        console.log(`Server is running on port ${port}.`);
    });
}

launchServer();
