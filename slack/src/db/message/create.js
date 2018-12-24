import knex from "../knex"

const create = ({ user_id, user_name, colors, content }) => {
    console.log(user_id, user_name, colors, content )
    return knex("message").insert({ user_id, user_name, colors, content })
}

export default create
