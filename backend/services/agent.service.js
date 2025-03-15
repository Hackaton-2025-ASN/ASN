// services/agentService.js
const {Agent} = require('../models');

const agentService = {
    // Create a new Agent
    async createAgent(agentData) {
        try {
            const agent = await Agent.create(agentData);
            return agent;
        } catch (error) {
            throw error;
        }
    },

    // Get all Agents
    async getAllAgents() {
        try {
            const agents = await Agent.findAll();
            return agents;
        } catch (error) {
            throw error;
        }
    },

    // Get Agent by ID
    async getAgentById(id) {
        try {
            const agent = await Agent.findByPk(id);
            return agent;
        } catch (error) {
            throw error;
        }
    },

    // Update an Agent
    async updateAgent(id, updateData) {
        try {
            const [rowsAffected, [updatedAgent]] = await Agent.update(updateData, {
                where: {id},
                returning: true, // Only works in Postgres; for MySQL, you can do a separate query.
            });

            // If no rows are affected, the ID doesn't exist
            if (rowsAffected === 0) {
                return null;
            }
            return updatedAgent;
        } catch (error) {
            throw error;
        }
    },

    // Delete an Agent
    async deleteAgent(id) {
        try {
            const rowsDeleted = await Agent.destroy({
                where: {id},
            });
            return rowsDeleted; // Number of rows deleted (0 if not found)
        } catch (error) {
            throw error;
        }
    },

    async followAgent(experiment_id, follower_id, followee_id) {
        try {
            const follower = await Agent.findByPk(experiment_id, follower_id);
            if (!follower) {
                return null;
            }
            const followee = await Agent.findByPk(experiment_id, followee_id);
            if (!followee) {
                return null;
            }
            follower.followingCount += 1;
            followee.followersCount += 1;
            await follower.save();
            await followee.save();
        } catch (error) {
            throw error;
        }
    }
};

module.exports = agentService;