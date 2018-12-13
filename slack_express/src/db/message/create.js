import knex from "../knex"

const create = ({ id, name, color, message }) => {
    return knex("message").insert({ id, name, color, message })
}

export default create
