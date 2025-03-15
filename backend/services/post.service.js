const db = require('../models');
const Post = db['Post'];
const postService = {};

postService.createPost = async ({experiment_id, post_id, image, content, agent_id}) => {
    try {
        const post = Post.create({ experiment_id, post_id, image, content, agent_id });

        return post;
    } catch (error) {
        throw error;
    }
};

postService.likePost = async ({experiment_id, agent_id, post_id}) => {
    try {
        const post = await Post.findOne({ where: { experiment_id, agent_id, post_id } });

        if (!post) {
            throw new Error(`Post with ID ${post_id} not found.`);
        }

        post.likes += 1;
        await post.save();

        return post;
    } catch (error) {
        throw error;
    }
}

postService.dislikePost = async ({experiment_id, agent_id, post_id}) => {
    try {
        const post = await Post.findOne({ where: { experience_id, agent_id, post_id } });

        if (!post) {
            throw new Error(`Post with ID ${post_id} not found.`);
        }

        post.dislikes += 1;
        await post.save();

        return post;
    } catch (error) {
        throw error;
    }
}



module.exports = postService;
