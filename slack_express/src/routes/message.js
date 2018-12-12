import { message } from "../db"

const generateBody = async ({ user_id, user_name, text }) => {
    const result = await message.create({ user_id, user_name, text })
    return {
        attachments: [
            {
                fields: [
                    {
                        title: "Message Received!",
                        value: "Thank you!"
                    }
                ]
            }
        ]
    }
}

export default generateBody
