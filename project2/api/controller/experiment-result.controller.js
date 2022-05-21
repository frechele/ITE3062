const { ExperimentResult } = require('../database');
const { wrapWithErrorHander } = require('../util');

async function getAll(req, res) {
    const result = await ExperimentResult.findAll();
    res.status(200).json({ result });
}

async function insertOrUpdate(req, res) {
    await ExperimentResult.create(req.body);
    res.status(200).json({ result: 'success' });
}

module.exports = wrapWithErrorHander({
    getAll,
    insertOrUpdate,
});
