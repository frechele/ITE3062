const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
    return sequelize.define(
        'ExperimentResult',
        {
            id: {
                autoIncrement: true,
                type: DataTypes.INTEGER.UNSIGNED,
                allowNull: false,
                primaryKey: true,
            },
            confidence: {
                type: DataTypes.FLOAT,
                allowNull: false,
            },
            correct: {
                type: DataTypes.BOOLEAN,
                allowNull: false,
            },
            spendtime: {
                type: DataTypes.INTEGER.UNSIGNED,
                allowNull: false,
            },
        },
        {
            sequelize,
            tableName: 'ExperimentResult',
            indexes: [
                {
                    name: 'PRIMARY',
                    unique: true,
                    fields: [{ name: 'id' }],
                },
            ],
            timestamps: false,
        },
    )
}
