const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
    const Agent = sequelize.define('Agent', {
        id: {
            type: DataTypes.UUID,
            defaultValue: DataTypes.UUIDV4,
            primaryKey: true,
        },
        name: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        image: {
            type: DataTypes.STRING,
            allowNull: true,
        },
        instructions: {
            type: DataTypes.TEXT,
            allowNull: true,
        },
        followerCount: {
            type: DataTypes.INTEGER,
            defaultValue: 0,
        },
        followingCount: {
            type: DataTypes.INTEGER,
            defaultValue: 0,
        }
    }, {
        timestamps: false
    });

    Agent.associate = (db) => {
        Agent.belongsTo(db['Experiment'], { foreignKey: 'experimentId', onDelete: 'CASCADE' });
        Agent.hasMany(db['Post'], { foreignKey: 'agentId', onDelete: 'CASCADE' });
        Agent.hasMany(db['Comment'], { foreignKey: 'agentId', onDelete: 'CASCADE' });
    };

    return Agent;
};