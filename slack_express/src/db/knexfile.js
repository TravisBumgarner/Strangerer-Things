const config = require("../config")

const { host, user, password, database } = config.db

module.exports = {
    development: {
        client: "pg",
        version: "7.2",
        connection: {
            host,
            user,
            password,
            database
        },
        migrations: {
            directory: "./migrations"
        },
        seeds: {
            directory: "./seeds"
        }
    }
}
