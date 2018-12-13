import { message } from "../db"

const generateBody = async ({content, colors, user_id, user_name}) => {
    const result = await message.create({content, colors, user_id, user_name})
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
