import { message } from "../db"

const generateBody = async ({ user_id, user_name, text }) => {
    const result = await message.create({ user_id, user_name, text })
    return {
        attachments: [
            {
                fields: [
                    {
                        title: "Strangerer Things have happend!",
                        value: `<@${user_id}>, thanks for your message! It'll display shortly.`
                    }
                ]
            }
        ]
    }
}

export default generateBody
