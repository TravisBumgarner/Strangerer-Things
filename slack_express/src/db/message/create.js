import knex from "../knex"

const create = ({ user_id, user_name, text }) => {
    return knex("message").insert({ user_id, user_name, text })
}

export default create
