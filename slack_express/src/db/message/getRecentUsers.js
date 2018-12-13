import knex from "../knex"

const MINUTE = 60000
const MINUTES_BETWEEN_MESSAGES = 1

const getRecentUsers = async () => {
    const now = new Date()
    const minutes_ago = now.getTime() - MINUTE * MINUTES_BETWEEN_MESSAGES
    
    const recentUsers = await knex.select('user_id').from('message').where('created_at', '>=', minutes_ago)
    return recentUsers.map(r => r.user_id)
}

export default getRecentUsers
