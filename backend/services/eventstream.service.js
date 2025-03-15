const db = require('../models');
const EventStream = db['EventStream'];
const eventStreamService = {};
const postService = require('./post.service');
const commentService = require('./comment.service');
const agentService = require('./agent.service');

eventStreamService.storeEvent = async ({ experiment_id, timestep, id, type, user_id, post_id, content, image, follower_id, followee_id }) => {
    try {
        const event = await EventStream.create({
            experiment_id: experiment_id,
            timestep: timestep,
            id: id,
            type: type,
            user_id: user_id,
            post_id: post_id,
            content: content,
            image: image,
            follower_id: follower_id,
            followee_id: followee_id
        });
        return event;
    } catch (error) {
        throw error;
    }
}


eventStreamService.applyEvent = async (event) => {
    const { experiment_id, timestep, id, type, user_id, post_id, content, image, follower_id, followee_id } = event;

    if (type === 1) {
        // Create a post
        await postService.createPost({ experiment_id, post_id, image, content, agent_id: user_id });
    }
    else if (type === 2) {
        // Comment on a post
        await commentService.create({ content, agent_id: user_id, post_id });
    }
    else if (type === 3) {
        // Like a post
        await postService.likePost({experiment_id, agent_id, post_id});
    }
    else if (type === 4) {
        // Dislike a post
        await postService.dislikePost({experiment_id, agent_id, post_id});
    }
    else if (type === 5) {
        // Follow another user
        await agentService.followAgent({experiment_id, follower_id, followee_id});
    }
    else {
        console.log('Unknown event type');
    }
}

module.exports = eventStreamService;
