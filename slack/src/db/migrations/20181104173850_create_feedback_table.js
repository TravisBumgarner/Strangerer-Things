const TABLE_NAME = "message"

exports.up = function(knex, Promise) {
    return knex.schema.createTable(TABLE_NAME, table => {
        table.increments("message_id")
        table.text("user_id")
        table.text("user_name")
        table.text("colors")
        table.text("content")
        table.timestamp("created_at").defaultTo(knex.fn.now())
    })
}

exports.down = function(knex, Promise) {
    return knex.schema.dropTable(TABLE_NAME)
}
