const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
    const Post = sequelize.define('Post', {
        id: {
            type: DataTypes.INTEGER,
            autoIncrement: true,
            primaryKey: true,
            allowNull: false,
        },
        experiment_id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            allowNull: false,
        },
        title: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        image: {
            type: DataTypes.STRING,
            allowNull: true,
        },
        likeCount: {
            type: DataTypes.INTEGER,
            defaultValue: 0,
        },
        dislikeCount: {
            type: DataTypes.INTEGER,
            defaultValue: 0,
        }
    }, {
        timestamps: false
    });

    Post.associate = (db) => {
        Post.belongsTo(db['Agent'], { foreignKey: 'agentId', onDelete: 'CASCADE' });
        Post.hasOne(db['Comment'], { foreignKey: 'postId', onDelete: 'CASCADE' });
    };

    return Post;
};